<?php session_start(); ?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Pi Car Control Panel</title>
    <link rel="stylesheet" href="/custom.css">
</head>
<body>
    <h2 id="header">Pi Car Control Panel</h2>

    <?php
    if (!empty($_POST)) {
        $conn = new mysqli("localhost", "picar_user", $_POST["pw"], "picar_db");
    
        if (mysqli_connect_errno()) {
            session_destroy();
            echo '<p style="color:red;">Login failed</p>';
        }
        else {
            $_SESSION["pw"] = $_POST["pw"];
            $conn->query("UPDATE PiCar SET Value='' WHERE Name='Command'");
            $result = $conn->query("SELECT Value FROM PiCar WHERE Name='IP'");
            $_SESSION["ip"] = $result->fetch_assoc()["Value"];
        }
    
        if ($conn) {
            $conn->close();
        }
    }
    ?>
    <?php if (!isset($_SESSION["pw"])) : ?>
    <h4>Log In</h4>
    <form action="<?php echo htmlspecialchars($_SERVER['PHP_SELF']); ?>" method="post">
        <p>Enter password: <input type="password" name="pw"></p>
        <input type="submit" value="Log In">
    </form>
    <?php else : ?>
    <p>
        <button type="button" onclick="startButton()">Start</button>
        <button type="button" onclick="stopButton()">Stop</button>
        <a id="logout" href="/logout.php">Log Out</a>
    </p>

    <div id="camera-container">
        <div id="camera-iframe">
            <iframe id="camera" src="//<?php echo $_SESSION["ip"]; ?>/html/min.php" width="854" height="480"></iframe>
        </div>
    </div>

    <div id="joystick"></div>

    <div class="hide-mobile">
        <p><b>Keyboard Controls:</b> Y - Start, W - Forwards, A - Left, S - Backwards, D - Right, X - Stop, R - Autopilot</p>
        <p><b>IP Address:</b> <?php echo $_SESSION["ip"]; ?></p>
    </div>

    <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/nipplejs/0.6.7/nipplejs.min.js"></script>
    <script type="text/javascript" src="/main.js"></script>
    <script type="text/javascript">
    var joystick = nipplejs.create({
        zone: document.getElementById("joystick"),
        mode: "static",
        color: "blue",
        position: {left: "50%", top: "50%"},
        size: 200
    });
    joystick.on('move', function(evt, data) {
        moveJoystick(data);
      }).on('end', function(evt, data) {
        endJoystick();
      });
    
    document.onkeydown = onKeyDownEvent;
    document.onkeyup = onKeyUpEvent;
    </script>
    <?php endif; ?>
</body>
</html>
