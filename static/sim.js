function rotationplot(form) {
    form.elements["rap"] = "456";
    document.getElementById("rotplot").src = 'rotation/' + form.elements["rotation"].value
    return false;
}
function runsim(form) {
    rap = document.getElementById("stats").elements["rap"].value;
    document.getElementById("rotplot").src = 'dpsplot'
    return false;
}

function findValue(fullstr, searchpart) {
    var pos = fullstr.indexOf(searchpart);
    var part = fullstr.substr(pos, 50);
    var matches = part.match(/(\d+)/);
    if (matches) {
        var value = matches[0];
    } else {
        var value = 0;
    }
    return value;
}

function changeBow() {
    var val = document.getElementById('weapon').value;
    if (val === 'custom') {
        document.getElementById("stats").elements["rspd"].readOnly = false;
        document.getElementById("stats").elements["rdps"].readOnly = false;
    } else {
        document.getElementById("stats").elements["rspd"].readOnly = true;
        document.getElementById("stats").elements["rdps"].readOnly = true;
    }
    if (val === 'Slavemaker') {
        document.getElementById("stats").elements["rspd"].value = 3.2;
        document.getElementById("stats").elements["rdps"].value = 67.5;
    } else if (val === 'Sunfury') {
        document.getElementById("stats").elements["rspd"].value = 2.9;
        document.getElementById("stats").elements["rdps"].value = 83.3;
    } else if (val === 'Wrathtide') {
        document.getElementById("stats").elements["rspd"].value = 3.0;
        document.getElementById("stats").elements["rdps"].value = 75.5;
    }
}

function changeTwohander() {
    var val = document.getElementById('twohander').value;
    if (val === 'custom') {
        document.getElementById("stats").elements["mspd"].readOnly = false;
        document.getElementById("stats").elements["mdps"].readOnly = false;
    } else {
        document.getElementById("stats").elements["mspd"].readOnly = true;
        document.getElementById("stats").elements["mdps"].readOnly = true;
    }
    if (val === 'Mooncleaver') {
        document.getElementById("stats").elements["mspd"].value = 3.7;
        document.getElementById("stats").elements["mdps"].value = 118.6;
    } else if (val === 'Crescent') {
        document.getElementById("stats").elements["mspd"].value = 3.7;
        document.getElementById("stats").elements["mdps"].value = 109.6;
    } else if (val === 'Legacy') {
        document.getElementById("stats").elements["mspd"].value = 3.5;
        document.getElementById("stats").elements["mdps"].value = 114;
    }
}

function showImport() {
    document.getElementById("import").style.visibility = "visible";
    document.getElementById("import-submit").style.visibility = "visible";
    return false;
}

function seventyimport(form) {
    input = document.getElementById("import").elements["in"].value;
    //document.getElementById("import").elements["out"].value = input.replace(/(?:\r\n|\r|\n)/g, '').split(/(?=[A-Z]{5,})/g);
    var all = input.replace(/(?:\r\n|\r|\n)/g, ',');

    document.getElementById("stats").elements["rap"].value = findValue(all, ',Ranged Attack Power');
    document.getElementById("stats").elements["map"].value = findValue(all, ',Attack Power');
    document.getElementById("stats").elements["cr"].value = findValue(all, ',Ranged Crit Rating');
    document.getElementById("stats").elements["hr"].value = findValue(all, ',Ranged Hit Rating');
    document.getElementById("stats").elements["agi"].value = findValue(all, ',Agility');
    document.getElementById("stats").elements["haste"].value = findValue(all, ',Haste Rating');
    document.getElementById("stats").elements["arpen"].value = findValue(all, ',Armor Penetration');
    document.getElementById("import").style.visibility = "hidden";
    document.getElementById("import-submit").style.visibility = "hidden";
    return false;
}
function loadDoc() {
  document.getElementById("rotplot").src = '';
  var xhttp = new XMLHttpRequest();
  var params = "";
  params += "agi=" + document.getElementById("stats").elements["agi"].value;
  params += "&rap=" + document.getElementById("stats").elements["rap"].value;
  params += "&map=" + document.getElementById("stats").elements["map"].value;
  params += "&cr=" + document.getElementById("stats").elements["cr"].value;
  params += "&hr=" + document.getElementById("stats").elements["hr"].value;
  params += "&haste=" + document.getElementById("stats").elements["haste"].value;
  params += "&rdps=" + document.getElementById("stats").elements["rdps"].value;
  params += "&rspd=" + document.getElementById("stats").elements["rspd"].value;
  params += "&mdps=" + document.getElementById("stats").elements["mdps"].value;
  params += "&mspd=" + document.getElementById("stats").elements["mspd"].value;
  //document.getElementById("params").innerHTML = params;
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("demo").innerHTML =
      this.responseText;

      document.getElementById("rotplot").src = 'dpsplot?' + new Date().getTime();
    }
  };
  xhttp.open("GET", "sim"+"?"+params, true);
  xhttp.send();
}
