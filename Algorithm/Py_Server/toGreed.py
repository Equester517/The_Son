import cv2
import numpy as np
import math


def contour(image):
    # 사진 사이즈 조정

    a = 0

    def Resizing(img):
        width = 500
        ratio = width / img.shape[1]  # width * 사진 너비 = 비율
        height = int(ratio * img.shape[0])  # 비율 * 사진 높이
        # 비율 유지한 채로 이미지 Resize
        resize = cv2.resize(img, dsize=(width, height), interpolation=cv2.INTER_AREA)
        print(resize.shape)

        return resize

    # 창 이름 설정

    # cv2.namedWindow('image')

    # 이미지 파일 읽기
    base = cv2.imread(image, cv2.IMREAD_COLOR)
    rotImg = cv2.rotate(base, cv2.ROTATE_90_CLOCKWISE)

    # 이미지 사이즈 조정

    img = Resizing(rotImg)

    # 이미지 hsv 색 변경

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 피부색 범위 검출

    img_hsv = cv2.fastNlMeansDenoisingColored(img_hsv, None, 10, 10, 7, 21)  # 노이즈제거

    lower = np.array([0, 50, 80], dtype="uint8")  # 최소 범위
    upper = np.array([70, 255, 255], dtype="uint8")  # 최대 범위

    img_hand = cv2.inRange(img_hsv, lower, upper)  # 범위 내 이미지 추출

    # 손 가장자리 외각선 찾기

    contours, hierarchy = cv2.findContours(img_hand, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    max = 0

    maxctr = None
    for cnt in contours:

        area = cv2.contourArea(cnt)

        if (max < area):
            max = area

            maxctr = cnt  # 손 가장자리 배열

    # 흰색으로 손 내부 다시 칠하기

    mask = np.zeros(img.shape).astype(img.dtype)

    color = [255, 255, 255]

    img_hand = cv2.fillPoly(mask, [maxctr], color)

    # 손 외각선 그리기

    cv2.drawContours(img_hand, [maxctr], 0, (0, 0, 255), 3)

    # 중심점
    img_gray = cv2.cvtColor(img_hand, cv2.COLOR_BGR2GRAY)
    img_dist = cv2.fillPoly(mask, [maxctr], color)
    dist = cv2.distanceTransform(img_gray, cv2.DIST_L2, 5)
    dist_max = np.argmax(dist)
    # contour_max=np.argmax(contours)
    maxY, maxX = divmod(dist_max, 500)
    # conY,conX=divmod(contour_max,400)
    result = cv2.normalize(dist, None, 255, 0, cv2.NORM_MINMAX, cv2.CV_8UC1)
    cv2.circle(img_hand, (maxX, maxY), 3, (0, 0, 255), -1)
    #cv2.imwrite('contour.png', img_hand)
    # 손목찾기
    corners = cv2.goodFeaturesToTrack(img_gray, 500, 0.01, 8)
    rightX = 600
    rightY = maxY
    leftY = maxY
    leftX = 0
    while a < 50:
        for i in corners:
            x, y = i.ravel()
            if y > maxY:
                if rightY - y < 0 and rightY - y > -20 and x > maxX and rightX > x:
                    rightX = x
                    rightY = y
        a = a + 1
    a = 0
    while a < 50:
        for i in corners:
            x, y = i.ravel()
            if y > maxY:
                if leftY - y < 0 and leftY - y > -30 and x < maxX and leftY < rightY + 5:
                    leftX = x
                    leftY = y
        a = a + 1
    cv2.imwrite('contour2.png', img_hand)
    # 손끝 중심
    corners = cv2.goodFeaturesToTrack(img_gray, 10, 0.01, 10)
    for i in corners:
        x, y = i.ravel()
        if y > maxY:
            if rightY - y < 0 and x > maxX:
                rhandX = x
                rhandY = y
    for i in corners:
        x, y = i.ravel()
        if y > maxY:
            if rightY - y < 0 and x < maxX:
                lhandX = x
                lhandY = y

    # 손끝 중심

    #exitX = int((rhandX + lhandX) / 2)
    #exitY = int((rhandY + lhandY) / 2)
    # 손목 중심
    wristX = int((rightX + leftX) / 2)
    wristY = int((rightY + leftY) / 2)


    #cv2.circle(img_hand, (rightX, rightY), 3, (255, 0, 0), -1)
    #cv2.circle(img_hand, (leftX, leftY), 3, (255, 0, 0), -1)
    #cv2.circle(img_hand, (rhandX, rhandY), 3, (0, 255, 0), -1)
    #cv2.circle(img_hand, (lhandX, lhandY), 3, (0, 255, 0), -1)
    #cv2.circle(img_hand, (wristX, wristY), 3, (0, 0, 255), -1)
    #cv2.circle(img_hand, (exitX, exitY), 3, (0, 0, 255), -1)

    print('손 중심점:', (maxX, maxY))
    print('손목 중심점:', (wristX, wristY))
    #print('손끝 중심점:', (rightX, rightY))

    x1 = maxX - wristX
    y1 = maxY - wristY
    x2 = rightX - wristX
    y2 = rightY - wristY
    angle = math.atan2(y1 * x2 - x1 * y2, x1 * x2 + y1 * y2) * 180 / math.pi
    angle = abs(angle)
    if angle > 90:
        angle = angle-90
    else:
        angle=90-angle
    angle = round(angle)
    print('각도:', angle)

    # 이미지 보여주기
    cv2.imwrite('contour.png', img_hand)
    cv2.imwrite('hsv2.png', img_hsv)
    '''
    cv2.imshow('gray', img_dist)
    cv2.imshow('main', img_hand)
    cv2.imshow('distance', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''

    return img_hand, angle