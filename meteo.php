<?php

ini_set('error_reporting', E_ALL);
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);

echo 'kuku2'; 

header("Content-Type: text/html; charset=koi-8");
include "db_inc.php";
//$Unitronics="=64$1222.5$56.6$55.0";
$Unitronics=$_GET['name'];
//$strock="=251023$123.4$022.6$35$12";

echo "Есть связь с сервером: ip_10.3.2.19";

$a=strpos($Unitronics, "$");
$a1=strpos($Unitronics, "$", $a+1);
$a2=strpos($Unitronics, "$", $a1+2);
$Number_cpu = (int)(substr($Unitronics, 1, 2)); 
$Weight=(float)(substr($Unitronics, $a+1, 6));
$Cooling_t=(float)(substr($Unitronics, $a1+1, 4));
 $Chocolate_t = (float)(substr($Unitronics, $a2+1, 4));
 $flag = "Ok";
 
 if($Weight>500000)
 {
	$query ="SELECT Weight FROM `Unitronics`  WHERE Number_plc = '$Number_cpu' ORDER by id DESC LIMIT 1"; 
	$result = mysql_query($query) or die("Ошибка2" . mysql_error($link));
	if($result)
	{ 
		while ($row = mysql_fetch_row($result))
		{
			$Weight = (float)($row[0]); 
			$flag = "Weight";
		}
	}
 }
 if($Cooling_t>1300)
 {
	$query ="SELECT Cooling_t FROM `Unitronics`  WHERE Number_plc = '$Number_cpu' ORDER by id DESC LIMIT 1"; 
	$result = mysql_query($query) or die("Ошибка2" . mysql_error($link));
	if($result)
	{ 
		while ($row = mysql_fetch_row($result))
		{
			$Cooling_t = (float)($row[0]); 
			$flag = "Cooling_t";
		}
	}
 }
 if($Chocolate_t>1300)
 {
	$query ="SELECT Chocolate_t FROM `Unitronics`  WHERE Number_plc = '$Number_cpu' ORDER by id DESC LIMIT 1"; 
	$result = mysql_query($query) or die("Ошибка2" . mysql_error($link));
	if($result)
	{ 
		while ($row = mysql_fetch_row($result))
		{
			$Chocolate_t = (float)($row[0]); 
			$flag = "Chocolate_t";
		}
	}
 }

$query= "INSERT INTO `Unitronics2` ( Date,
                                    Number_plc,
                                    Weight,
                                    Cooling_t, 
                                    Сhocolate_t, 
                                    flag)
         VALUES (convert(now(), Datetime),
                                    '$Number_cpu', 
                                    '$Weight',
                                    '$Cooling_t', 
                                    '$Chocolate_t', 
                                    '$flag');"; 
                                    
     echo "$query"."<br>";                                
                                    
$result = mysqli_query($link,$query) or die("Query failed : " . mysqli_error($link));	
	   echo "$result"."<br>"; 	
    mysqli_close($link);


];




