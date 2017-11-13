<?php
session_name("picar");
session_start();
if (!isset($_SESSION["pw"]) || !isset($_POST["cmd"])){
    die("Direct access not permitted");
}
$conn = new mysqli("localhost", "lintx10h_public", $_SESSION["pw"], "lintx10h_picar");
$conn->query("UPDATE PiCar SET Value='" . $_POST["cmd"] . "' WHERE Name='Command'");
$conn->close();
?>
