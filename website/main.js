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
    var deg = data.angle.degree;
    if (data.force <= 0.3) {
        command_new = "";
    }
    else if (15 <= deg && deg < 75) {
        // up right
        command_new = "wd";
    }
    else if (75 <= deg && deg < 105) {
        // up
        command_new = "w";
    }
    else if (105 <= deg && deg < 165) {
        // up left
        command_new = "wa";
    }
    else if (165 <= deg && deg < 195) {
        // left
        command_new = "a";
    }
    else if (195 <= deg && deg < 255) {
        // down left
        command_new = "sa";
    }
    else if (255 <= deg && deg < 285) {
        // down
        command_new = "s";
    }
    else if (285 <= deg && deg < 345) {
        // down right
        command_new = "sd";
    }
    else if (345 <= deg < 360 || 0 <= deg < 15) {
        // right
        command_new = "d";
    }
    if (command_new !== "") {
        command_new += "," + Math.min(100, Math.round(data.force * 100));
    }
    if (command_new !== command) {
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
    command_new = command;
    if (e.keyCode == '87' || e.keyCode == '38') {
        // up arrow
        if (command.indexOf('w') == -1) {
            command += "w";
        }
        command_new = command;
    }
    else if (e.keyCode == '83' || e.keyCode == '40') {
        // down arrow
        if (command.indexOf('s') == -1) {
            command += "s";
        }
        command_new = command;
    }
    else if (e.keyCode == '65' || e.keyCode == '37') {
        // left arrow
        if (command.indexOf('a') == -1) {
            command += "a";
        }
        command_new = command;
    }
    else if (e.keyCode == '68' || e.keyCode == '39') {
        // right arrow
        if (command.indexOf('d') == -1) {
            command += "d";
        }
        command_new = command;
    }
    else if (e.keyCode == '89') {
        // y
        command = "";
        command_new = "y";
    }
    else if (e.keyCode == '88') {
        // x
        command = "";
        command_new = "x";
    }
    else if (e.keyCode == '82') {
        // r
        command = "";
        command_new = "r";
    }
    if (e.shiftKey) {
        command_new += ",66";
    }
    if (command_new !== "") {
        sendCommand(command_new);
    }
}

function onKeyUpEvent(e) {
    e = e || window.event;
    if (e.keyCode == '87' || e.keyCode == '38') {
        // up arrow
        command = command.replace('w', '');
    }
    else if (e.keyCode == '83' || e.keyCode == '40') {
        // down arrow
        command = command.replace('s', '');
    }
    else if (e.keyCode == '65' || e.keyCode == '37') {
        // left arrow
        command = command.replace('a', '');
    }
    else if (e.keyCode == '68' || e.keyCode == '39') {
        // right arrow
        command = command.replace('d', '');
    }
    sendCommand(command);
}
