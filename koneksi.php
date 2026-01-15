<?php
    $host     = 'localhost';
    $user     = 'root'; 
    $password = 'n3wp4ssw0rd';                  
    $db       = 'quiz_pengupil';

    $con = mysqli_connect($host, $user, $password, $db);
    if (!$con) { 
        die("Connection failed: " . mysqli_connect_error());    
    }
?>