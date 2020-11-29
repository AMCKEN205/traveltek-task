var request = new XMLHttpRequest();
var request_type = "GET";
var request_endpoint = "https://t423qudqv9.execute-api.eu-west-1.amazonaws.com/deployed?requestedData=total-flights-count"

request.open(request_type, request_endpoint);

request.onload = function() {
    var all_flights_count = JSON.parse(request.responseText)["All flights count"];
    console.log(all_flights_count);

    document.getElementById("total-flights-count").innerHTML = all_flights_count;
}

request.send();
