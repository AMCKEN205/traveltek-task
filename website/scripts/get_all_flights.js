var request = new XMLHttpRequest();
var request_type = "GET";
var request_endpoint = "https://t423qudqv9.execute-api.eu-west-1.amazonaws.com/deployed?requestedData=total-flights-count"

request.open(request_type, request_endpoint);

request.onload = function() {
    var all_flights_count = JSON.parse(request.responseText)["All flights count"];

    document.getElementById("top-level-container").innerHTML = `There are ${all_flights_count} total flights in the dataset`;
}

request.send();
