var request = new XMLHttpRequest();
var request_type = "GET";
var request_endpoint = "https://t423qudqv9.execute-api.eu-west-1.amazonaws.com/deployed?requestedData=sweden-flights-data"

request.open(request_type, request_endpoint);

request.onload = function() {
    var sweden_flights_count = JSON.parse(request.responseText)["Sweden flights count"];
    var percent_flights_sweden = JSON.parse(request.responseText)["Percentage flights into Sweden"];

    document.getElementById("top-level-container").innerHTML = 
        `There are ${sweden_flights_count} flights that stop in Sweden dataset.<br>
        That's ${percent_flights_sweden}% of all flights in the dataset.`;
}

request.send();