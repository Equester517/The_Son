<?php 
    $con = mysqli_connect("localhost", "root", "", "theson");
    mysqli_query($con,'SET NAMES utf8');

//안드로이드에서 HashMap array로 보낸 변수를 받는다 

 $sql = "select * from mouse1"; 
 $rs= mysqli_query($con, $sql);   
$result = array();
//// insert문이 성공하면 result가 1 (true)임. 안드로이드에서 "가입을 축하합니다" 표시됨.

while($row = mysqli_fetch_array($rs)){
	$arrayMiddle = array("mouse_name" => $row[0], "mouse_length" => $row[1], "mouse_width" => $row[2], "mouse_height" => $row[3], "mouse_weight" => $row[4], "mouse_wire" => $row[5], "mouse_picture" => $row[6], "mouse_site" => $row[7]);
	array_push($result, $arrayMiddle);
}
    echo json_encode(array("result"=>$result));  // 'mouse_name"을 result통해 전송
mysqli_close($con);

?>