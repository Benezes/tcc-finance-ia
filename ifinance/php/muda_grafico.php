<?php

session_start();

if($_SESSION['grafico'] == 0){
	 $_SESSION['grafico'] = 1;
}else{
	$_SESSION['grafico'] = 0;
}


header('Location:../index.php')

?>