// Setup request attributes
var request = new XMLHttpRequest();
var request_type = "GET";
var request_endpoint = "https://t423qudqv9.execute-api.eu-west-1.amazonaws.com/deployed?requestedData=average-journey-times"

// Make average journey times globally accessible as we'll want to continually retrieve/update its value.
// Don't want to have to make a request to the API every time we do so!
var flight_av_journey_times_obj = null;

// Setup request
request.open(request_type, request_endpoint);

// Setup request event handle for once made
request.onload = function() {
    // Extract flight average journey times data.
    flight_av_journey_times_obj = JSON.parse(request.responseText);

    var default_depart_dest = "LHR->DXB"

    // Build depart->dest combobox selector

    // Combobox start and end tags we use when building our combobox from API data.
    var combobox_start_string = '<br><select onchange="on_depart_dest_change(this)">'
    var combobox_end_string = " </select><br>"

    var combobox = combobox_start_string;

    for (const [depart_dest, average_flight_time] of Object.entries(flight_av_journey_times_obj)) {
        if (depart_dest == default_depart_dest){
            depart_dest_option = `<option selected="selected" value="${depart_dest}">${depart_dest}</option>`
        }
        else{
            depart_dest_option = `<option value="${depart_dest}">${depart_dest}</option>`
        }
        combobox = combobox.concat(depart_dest_option)
    }

    var combobox = combobox.concat(combobox_end_string)

    // Build average flight time paragraph, gets updated on depart->dest combobox selected value change
    var av_flight_time_para= '<p id="average_flight_time"></p>'

    var top_level_container_inner_html = combobox.concat(av_flight_time_para)

    document.getElementById("top-level-container").innerHTML = top_level_container_inner_html;

    // Set the intial average flight time value
    set_average_flight_time(default_depart_dest)

}

// Send the request
request.send();

function on_depart_dest_change(selected_depart_dest_combo){
    // Handle depart->dest combobox value change
    var selected_depart_dest = selected_depart_dest_combo["value"]
    set_average_flight_time(selected_depart_dest)

}

function set_average_flight_time(selected_depart_dest){
    // Set the value of average flight text
    var average_flight_time = flight_av_journey_times_obj[selected_depart_dest]
    var average_flight_time_text = `Average flight time is (HH:MM:SS): ${average_flight_time}`
    document.getElementById("average_flight_time").innerHTML = average_flight_time_text;
}