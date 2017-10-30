var command = "";
var command_new = "";

function sendCommand(command) {
    xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST", "update-db.php", true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send("cmd=" + command);
}

function startButton() {
    command = "";
    sendCommand("y");
}

function stopButton() {
    command = "";
    sendCommand("x");
}

function moveJoystick(data) {
    //console.log(data);
    var deg = data.angle.degree;
    if (data.force <= 0.3) {
        command_new = "";
    }
    else if (75 <= deg && deg < 105) {
        // up
        command_new = "w";
    }
    else if (105 <= deg && deg < 180) {
        // up left
        command_new = "wa";
    }
    else if (0 <= deg && deg < 75) {
        // up right
        command_new = "wd";
    }
    else if (225 <= deg && deg < 315) {
        // down
        command_new = "s";
    }
    else if (180 <= deg && deg < 225) {
        // down left
        command_new = "sa";
    }
    else if (315 <= deg && deg < 360) {
        // down right
        command_new = "sd";
    }
    if (command_new != command) {
        command = command_new;
        sendCommand(command);
    }
}

function endJoystick() {
    command = "";
    sendCommand(command);
}

function onKeyDownEvent(e) {
    e = e || window.event;
    if ((e.keyCode == '87') && (command.indexOf('w') == -1)) {
        // up arrow
        command += "w";
        sendCommand(command);
    }
    else if ((e.keyCode == '83') && (command.indexOf('s') == -1)) {
        // down arrow
        command += "s";
        sendCommand(command);
    }
    else if ((e.keyCode == '65') && (command.indexOf('a') == -1)) {
       // left arrow
       command += "a";
       sendCommand(command);
    }
    else if ((e.keyCode == '68') && (command.indexOf('d') == -1)) {
       // right arrow
       command += "d";
       sendCommand(command);
    }
    else if (e.keyCode == '89') {
       // y
       command = "";
       sendCommand("y");
    }
    else if (e.keyCode == '88') {
       // x
       command = "";
       sendCommand("x");
    }
    else if (e.keyCode == '82') {
       // r
       command = "";
       sendCommand("r");
    }
}

function onKeyUpEvent(e) {
    e = e || window.event;
    if (e.keyCode == '87') {
        // up arrow
        command = command.replace('w', '');
    }
    else if (e.keyCode == '83') {
        // down arrow
        command = command.replace('s', '');
    }
    else if (e.keyCode == '65') {
       // left arrow
       command = command.replace('a', '');
    }
    else if (e.keyCode == '68') {
       // right arrow
       command = command.replace('d', '');
    }
    sendCommand(command);
}
