// Setup request attributes
var request = new XMLHttpRequest();
var request_type = "GET";
var request_endpoint = "https://t423qudqv9.execute-api.eu-west-1.amazonaws.com/deployed?requestedData=morning-flights-count"

// Setup request
request.open(request_type, request_endpoint);

// Setup request event handle for once made
request.onload = function() {
    var morning_flights_count = JSON.parse(request.responseText)["Morning departures"];

    document.getElementById("top-level-container").innerHTML = `There are ${morning_flights_count} morning flights in the dataset`;
}

// Send the request
request.send();