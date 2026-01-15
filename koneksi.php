<?php
    // Use 127.0.0.1 for better compatibility with CI/CD environments
    $host     = '127.0.0.1';
    $user     = 'root'; 
    $password = 'n3wp4ssw0rd';                  
    $db       = 'quiz_pengupil';

    $con = mysqli_connect($host, $user, $password, $db);
    if (!$con) { 
        die("Connection failed: " . mysqli_connect_error());    
    }
?>