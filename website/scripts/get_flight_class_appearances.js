// Setup request attributes
var request = new XMLHttpRequest();
var request_type = "GET";
var request_endpoint = "https://t423qudqv9.execute-api.eu-west-1.amazonaws.com/deployed?requestedData=flight-class-appearances"

// Setup request
request.open(request_type, request_endpoint);

// Setup request event handle for once made
request.onload = function() {
    // Extract flight class appearance data from the API response and format as required by Canvas.js
    var flight_class_appearances_obj = JSON.parse(request.responseText);

    var flight_class_pairs = [];
    for (const [fclass, appearance_counts] of Object.entries(flight_class_appearances_obj)) {
        flight_class_pairs = flight_class_pairs.concat([{label: fclass, y : appearance_counts}])
    }

    // Initalise the Canvas.js chart and render on the webpage
    var chart = new CanvasJS.Chart(
        "top-level-container", {
            animationEnabled: true,
            theme: "light1",
            title : {text : "In-Flight Class Appearance Percentage Shares"},
            data : [
                {
                    type: "doughnut",
                    startAngle : 60,
                    indexLabelFontSize: 12,
                    indexLabel: "{label} - #percent%",
		            toolTipContent: "<b>{label}:</b> {y} (#percent%)",
                    dataPoints : flight_class_pairs
                }
            ] 
        }
    );
    chart.render();
}

// Send the request
request.send();