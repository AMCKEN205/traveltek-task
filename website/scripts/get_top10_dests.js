var request = new XMLHttpRequest();
var request_type = "GET";
var request_endpoint = "https://t423qudqv9.execute-api.eu-west-1.amazonaws.com/deployed?requestedData=top10-destinations"

request.open(request_type, request_endpoint);

request.onload = function() {
    // Extract top 10 destination data from the API response and format as required by Canvas.js
    var top10_dests_obj = JSON.parse(request.responseText);

    var top10_dests_pairs = [];
    for (const [dest, arrival_counts] of Object.entries(top10_dests_obj)) {
        top10_dests_pairs = top10_dests_pairs.concat([{label: dest, y : arrival_counts}])
    }

    // Initalise the Canvas.js chart and render on the webpage
    var chart = new CanvasJS.Chart(
        "top-level-container", {
            animationEnabled: true,
            theme: "light2",
            title : {text : "Top 10 Flight Destinations"},
            axisX : {
                title: "Desination Airport IATA Code"
            },
            axisY: {
                title: "Count Of Arrivals"
            },
            data : [
                {
                    type: "column",
                    dataPoints : top10_dests_pairs
                }
            ] 
        }
    );
    chart.render();
}

request.send();