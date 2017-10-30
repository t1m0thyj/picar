<?php
session_start();
if (!isset($_SESSION["pw"]) || !isset($_POST["cmd"])){
    die("Direct access not permitted");
}
$conn = new mysqli("localhost", "picar_user", $_SESSION["pw"], "picar_db");
$conn->query("UPDATE PiCar SET Value='" . $_POST["cmd"] . "' WHERE Name='Command'");
$conn->close();
?>
