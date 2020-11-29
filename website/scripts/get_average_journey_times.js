var request = new XMLHttpRequest();
var request_type = "GET";
var request_endpoint = "https://t423qudqv9.execute-api.eu-west-1.amazonaws.com/deployed?requestedData=flight-class-appearances"

// Make these globally accessible as we'll want to continually retrieve/update their values.
// Don't want to have to make a request to the API every time we do so!
var all_flights_count = null;
combobox = null;

request.open(request_type, request_endpoint);

request.onload = function() {
    all_flights_count = JSON.parse(request.responseText)["All flights count"];

    document.getElementById("top-level-container").innerHTML = `There are ${all_flights_count} total flights in the dataset`;
}

request.send();