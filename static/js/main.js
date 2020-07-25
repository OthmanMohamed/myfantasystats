var teamHolders = document.querySelectorAll(".team-holder");

var radioBest = document.getElementById("best");
var radio541 = document.getElementById("541");
var radio532 = document.getElementById("532");
var radio523 = document.getElementById("523");
var radio451 = document.getElementById("451");
var radio442 = document.getElementById("442");
var radio433 = document.getElementById("433");
var radio352 = document.getElementById("352");
var radio343 = document.getElementById("343");

radioBest.onchange = radioButtonAction;
radio541.onchange = radioButtonAction;
radio532.onchange = radioButtonAction;
radio523.onchange = radioButtonAction;
radio451.onchange = radioButtonAction;
radio442.onchange = radioButtonAction;
radio433.onchange = radioButtonAction;
radio352.onchange = radioButtonAction;
radio343.onchange = radioButtonAction;

var teamHolder;
for (var i = 0; i < teamHolders.length; i++) {
  teamHolder = teamHolders[i];
  teamHolderStyle(teamHolder);
}

function radioButtonAction() {
  "use strict";
  clearPitch();
  var idName = "team" + this.id;
  var teamToShow = document.getElementById(idName);
  teamToShow.classList.remove("hidden");
}

function clearPitch() {
  "use strict";
  for (var i = 0; i < teamHolders.length; i++) {
    if (!teamHolders[i].classList.contains("hidden")) {
      teamHolders[i].classList.add("hidden");
      break;
    }
  }
}

function teamHolderStyle(teamHolder) {
  "use strict";
  var defenceLine = teamHolder.querySelector(".defence");
  var noOfBoxes = defenceLine.childElementCount;
  var childList = defenceLine.children;
  boxesStyle(noOfBoxes, childList);

  var midLine = teamHolder.querySelector(".midfield");
  var noOfBoxes = midLine.childElementCount;
  var childList = midLine.children;
  boxesStyle(noOfBoxes, childList);

  var attackLine = teamHolder.querySelector(".attack");
  var noOfBoxes = attackLine.childElementCount;
  var childList = attackLine.children;
  boxesStyle(noOfBoxes, childList);
}

function boxesStyle(noOfBoxes, childList) {
  "use strict";
  switch (noOfBoxes) {
    case 1:
      for (var i = 0; i < noOfBoxes; i++) {
        childList[i].classList.add("one-box");
      }
      break;
    case 2:
      for (var i = 0; i < noOfBoxes; i++) {
        childList[i].classList.add("two-box");
      }
      break;
    case 3:
      for (var i = 0; i < noOfBoxes; i++) {
        childList[i].classList.add("three-box");
      }
      break;
    case 4:
      for (var i = 0; i < noOfBoxes; i++) {
        childList[i].classList.add("four-box");
      }
      break;
    case 5:
      for (var i = 0; i < noOfBoxes; i++) {
        childList[i].classList.add("five-box");
      }
      break;
    default:
    // code block
  }
}

var teamSelection = document.querySelector(".team-selection");
var left = teamSelection.querySelector(".left");
var top7Teams = [];
var top7TeamsPoints = [];
var top7Sum = 0;
for (var i = 0; i < 7; i++) {
  top7Teams.push(left.children[i].querySelector("h3").textContent);
  top7TeamsPoints.push(
    parseInt(left.children[i].querySelector(".number").textContent)
  );
  top7Sum += top7TeamsPoints[i];
}

var overallScore = parseInt(
  document.querySelector(".overview-holder").querySelector(".jsValueHolder")
    .textContent
);
var restScore = overallScore - top7Sum;

google.charts.load("current", { packages: ["corechart"] });
google.charts.setOnLoadCallback(drawChart);

// Draw the chart and set the chart values
function drawChart() {
  "use strict";
  var data = google.visualization.arrayToDataTable([
    ["Team", "Percentage"],
    [top7Teams[0], top7TeamsPoints[0] / overallScore],
    [top7Teams[1], top7TeamsPoints[1] / overallScore],
    [top7Teams[2], top7TeamsPoints[2] / overallScore],
    [top7Teams[3], top7TeamsPoints[3] / overallScore],
    [top7Teams[4], top7TeamsPoints[4] / overallScore],
    [top7Teams[5], top7TeamsPoints[5] / overallScore],
    [top7Teams[6], top7TeamsPoints[6] / overallScore],
    ["Other Teams", restScore / overallScore],
  ]);

  // Optional; add a title and set the width and height of the chart
  var options = {
    width: 1000,
    height: 500,
    backgroundColor: "#FFF",
  };

  // Display the chart inside the <div> element with id="piechart"
  var chart = new google.visualization.PieChart(
    document.getElementById("piechart")
  );
  chart.draw(data, options);
}

var coll = document.getElementsByClassName("collapsible");

for (var i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function () {
    this.classList.toggle("active");
    var content = this.parentElement.nextElementSibling.firstElementChild;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
}

function sortTable(n, tableID) {
  var table,
    rows,
    switching,
    i,
    x,
    y,
    shouldSwitch,
    dir,
    THs,
    innerDataX,
    innerDataY,
    switchcount = 0;
  table = document.getElementById(tableID);
  clearHeaderArrows(table);
  THs = table.querySelectorAll("th");
  switching = true;
  // Set the sorting direction to ascending:
  dir = "asc";
  THs[n].children[0].textContent = " ↓";
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < rows.length - 1; i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      innerDataX = x.innerHTML.split("%");
      innerDataY = y.innerHTML.split("%");
      /* Check if the two rows should switch place,
      based on the direction, asc or desc: */
      if (dir == "asc") {
        if (isNaN(innerDataX[0])) {
          if (innerDataX[0].toLowerCase() < innerDataY[0].toLowerCase()) {
            // If so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
          }
        } else {
          if (parseFloat(innerDataX[0]) < parseFloat(innerDataY[0])) {
            // If so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
          }
        }
      } else if (dir == "desc") {
        THs[n].children[0].textContent = " ↑";
        if (isNaN(innerDataX[0])) {
          if (innerDataX[0].toLowerCase() > innerDataY[0].toLowerCase()) {
            // If so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
          }
        } else {
          if (parseFloat(innerDataX[0]) > parseFloat(innerDataY[0])) {
            // If so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
          }
        }
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      // Each time a switch is done, increase this count by 1:
      switchcount++;
    } else {
      /* If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again. */
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}

function clearHeaderArrows(table) {
  THs = table.querySelectorAll("th");
  for (var i = 0; i < THs.length; i++) {
    if (THs[i].children[0].textContent != "") {
      THs[i].children[0].textContent = "";
      break;
    }
  }
}

body = document.querySelector("body");
body.onload = hideLoader;

function showLoader() {
  document.querySelector(".loader-wrapper").style.display = "flex";
}
function hideLoader() {
  document.querySelector(".loader-wrapper").style.display = "none";
}
