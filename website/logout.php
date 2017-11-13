<?php
session_name("picar");
session_start();
$_SESSION = array();
session_destroy();

header("Location: /picar");
?>
