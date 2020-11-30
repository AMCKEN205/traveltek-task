import os
import json
import datetime
from typing import Counter
from xmltodict import parse as xmltodict
import time as time_formatter


""" This code is run locally to test API functions prior to deployment. """

""" Functional/exposed methods """

def get_all_flights_count():
    """ Get the count of all flights within flight data """
    flight_data_dicts = get_flight_data()

    all_flights_count = len(flight_data_dicts)

    all_flights_data_json = json.dumps\
        (
            {"All flights count" : all_flights_count}
        )
    
    return all_flights_data_json

def get_morning_flights_count():
    """ Get the count of morning flights within flight data """  
    flight_data_dicts = get_flight_data()

    morning_departures_count = 0

    time_extract_format = "%H:%M:%S"

    # define time values for comparison/filtering
    midnight = datetime.time(hour=0,minute=0,second=0)
    afternoon = datetime.time(hour=12,minute=0,second=0)  
   
    # Assumption made that the requirements want the inital/outbound departure time
    for flight_data_dict in flight_data_dicts:    
        
        outbound_depart_time = datetime.datetime.strptime(flight_data_dict["@outdeparttime"], time_extract_format).time()

        current_flight_is_morning_departure = outbound_depart_time > midnight and outbound_depart_time < afternoon       
        
        if current_flight_is_morning_departure:
           morning_departures_count += 1
    
    morning_departures_count_json = json.dumps\
        (
            { "Morning departures" : morning_departures_count }
        )
    
    return morning_departures_count_json

def get_sweden_flight_data():
    """ Get the percentage and counts of flights that stop in Sweden within flight data"""
    flight_data_dicts = get_flight_data()

    # As the Sweden IATA codes list is so long declutter the publicly used function by 
    # denoising into a helper method. 'contains_segments' returned as the function existing
    # for IATA codes makes it the most convenient place to go.
    sweden_iata_codes, contains_segments = get_sweden_flight_filters()
    
    sweden_flights_count = 0

    for flight_data_dict in flight_data_dicts:

        if flight_data_dict["@destair"] in sweden_iata_codes:
            sweden_flights_count += 1

        # Check to see if segments fly into Sweden also and include this in the count
        elif contains_segments(flight_data_dict):
            flight_segments = flight_data_dict["segments"]["segment"]

            for flight_segment in flight_segments:

                if flight_segment["@arrcode"] in sweden_iata_codes:
                    sweden_flights_count += 1
                    break
        

    all_flights_count = json.loads(get_all_flights_count())["All flights count"]
    sweden_flights_percent = sweden_flights_count / all_flights_count * 100

    sweden_flights_data_json = json.dumps\
        (
            {
                "Percentage flights into Sweden" : sweden_flights_percent,
                "Sweden flights count" : sweden_flights_count            
            }
        )
    
    return sweden_flights_data_json

def get_top10_destinations():
    """ Get the top 10 destination airports along with a count of how often they appear in flight data""" 
    flight_data_dicts = get_flight_data()
    airport_destinations = list()

    for flight_data_dict in flight_data_dicts:
        airport_destinations.append(flight_data_dict["@destair"])

    dest_appearances = Counter(airport_destinations)
    
    # Sort in descending order
    dest_appearances_sorted = dest_appearances.most_common()
    # Then take the top ten
    dest_appearances_top_ten = dest_appearances_sorted[:10]
    # and convert to a dictionary for ease of use
    dest_appearances_top_ten_dict = dict(dest_appearances_top_ten)

    dest_appearances_top_ten_json = json.dumps(dest_appearances_top_ten_dict)

    return dest_appearances_top_ten_json
    

def get_average_journey_times():
    """ Get average journey times for all airport combos """
    flight_data_dicts = get_flight_data()        
    airport_av_travel_times_dict, airport_start_and_end_dests = get_airport_travel_dests_data(flight_data_dicts)

    datetime_format = "%Y-%m-%d %H:%M:%S"
    time_format = "%H:%M:%S"

    # Prepends used to denote outbound or inbound flights
    inbound_and_outbound_prepends = ["out", "in"]

    # Collect together all outbound and inbound flight times for the current destination combo
    for airport_start_and_end_dest in airport_start_and_end_dests:
        airport_start_dest = airport_start_and_end_dest[0]
        airport_end_dest = airport_start_and_end_dest[1]

        travel_times = list()

        for flight_data_dict in flight_data_dicts:
            
            if flight_data_dict["@depair"] == airport_start_dest and flight_data_dict["@destair"] == airport_end_dest:
                for prepend in inbound_and_outbound_prepends:
                    # Flight may be overnight which will reset time, so also use date for travel time calculations
                    depart_date = flight_data_dict["@{}departdate".format(prepend)]
                    depart_time = flight_data_dict["@{}departtime".format(prepend)]

                    # Can't properly get travel time so skip to next
                    if depart_date == "" or depart_time == "":
                        continue

                    depart_datetime = datetime.datetime.strptime("{} {}".format(depart_date, depart_time), datetime_format)

                    arrival_date = flight_data_dict["@{}arrivaldate".format(prepend)]
                    arrival_time = flight_data_dict["@{}arrivaltime".format(prepend)]

                    # Can't properly get travel time so skip to next
                    if arrival_date == "" or arrival_time == "":
                        continue

                    arrival_datetime = datetime.datetime.strptime("{} {}".format(arrival_date, arrival_time), datetime_format)

                    diff = arrival_datetime - depart_datetime

                    # just get the average seconds in numeric form as it's simpler, then convert back to time when we have the average in secs.
                    travel_time = int(diff.total_seconds())

                    travel_times.append(travel_time)

        # Get the average travel time of the combined outbound and inbound travel times for the current destination combo
        
        average_travel_time = int(sum(travel_times) / len(travel_times))

        average_travel_time = time_formatter.strftime(time_format, time_formatter.gmtime(average_travel_time))

        key_val_to_set = "{}->{}".format(airport_start_dest, airport_end_dest)
        airport_av_travel_times_dict[key_val_to_set] = average_travel_time

    average_travel_times = json.dumps(airport_av_travel_times_dict)

    return average_travel_times

def get_flight_class_appearances():
    """ Identify the different types of flight classes that appear in flight data along with counts of how often they appear """
    flight_data_dicts = get_flight_data()        

    flight_classes = list()

    filters_to_apply = get_flight_class_filters()

    for flight_data_dict in flight_data_dicts:
        # On inspection of the flight data xml file seems as though inbound and outbound flight classes are always identical.
        # However, just in case they aren't, and as we're going to visualise these as percentage shares instead of counts anyway, 
        # treating them differently shouldn't cause an issue.
        out_flight_class = flight_data_dict["@outflightclass"]
        in_flight_class = flight_data_dict["@inflightclass"]

        classes_to_add = [out_flight_class, in_flight_class]

        class_pos = 0
        
        while class_pos < len(classes_to_add):

            for filter in filters_to_apply:
                classes_to_add[class_pos], filter_applied = filter(classes_to_add[class_pos])

                if filter_applied:
                    # Already handled the formatting inconsistency for this current class so just move onto the next.
                    break

            class_pos += 1

        flight_classes += classes_to_add
    
    # Count flight class appearances and sort in descending order 
    flight_classes_counted = Counter(flight_classes)
    flight_classes_counted = flight_classes_counted.most_common()
    flight_classes_counted = dict(flight_classes_counted)

    flight_classes_json = json.dumps(flight_classes_counted)

    return flight_classes_json
    

""" Helper methods """

def get_flight_data():
    """ Define the flight data xml filepath locally here, however we'll access it in a bucket on AWS. """
    script_run_dir = os.path.dirname(os.path.realpath(__file__))
    flight_data_file = "flight_data/flightdata_A.xml"
    flight_data_filepath = "{}/../{}".format(script_run_dir, flight_data_file)

    # Easier to deal with XML data as a dictionary, so just open in byte format and convert to dict,
    # this then gets used for result filtering. Convert to JSON after filtering and return to user.

    # xmltodict uses an ordered dict so no danger of messing around with attribute ordering.
    flight_data_xml = open(flight_data_filepath, "rb")

    # Flights just acts as a wrapper around all other attributes so no real need to use it.
    # While xmltodict groups all flights under the same key ('flight'), so we only need the list of flight data dicts it contains.
    flight_data_dicts = xmltodict(flight_data_xml)["flights"]["flight"]

    return flight_data_dicts  

def get_sweden_flight_filters():
    # Sourced from: https://getbybus.com/en/blog/airports-in-sweden/
    sweden_iata_codes = \
            [
                "ARN",
                "GOT",
                "NYO",
                "BMA",
                "MMX",
                "LLA",
                "UME",
                "AGH",
                "OSD",
                "VBY",
                "SDL",
                "SFT",
                "RNB",
                "KRN",
                "KLR",
                "VXO",
                "VST",
                "VST",
                "NRK",
                "JKG",
                "HAD",
                "OER",
                "KSD",
                "ORB"
            ]

    # Check if a flight contains segment data that needs to be counted, just looks a bit neater in the exposed method. 
    contains_segments = lambda flight_data: "segments" in flight_data

    return sweden_iata_codes, contains_segments

def get_airport_travel_dests_data(flight_data_dicts):
    # Store a list of tuples with each start point and end point/destination airport
    airport_start_and_end_dests = list()

    for flight_data_dict in flight_data_dicts:
        airport_start_dest = flight_data_dict["@depair"]
        airport_end_dest = flight_data_dict["@destair"]

        airport_start_and_end_dests.append((airport_start_dest, airport_end_dest))
    
    # Only persist unique start and destination airport combos
    airport_start_and_end_dests = list(set(airport_start_and_end_dests))

    airport_travel_times_dict = dict.fromkeys\
        (
            list
                (
                    map
                        (
                            lambda start_and_end_dest : "{}->{}"
                            .format(start_and_end_dest[0],start_and_end_dest[1]),
                            airport_start_and_end_dests
                        )
                )
        )
    
    return airport_travel_times_dict, airport_start_and_end_dests

def get_flight_class_filters():
    """ Specify filters used to minimise output formatting inconsistencies """
    handle_no_class = lambda fclass, applied = False : (fclass,applied) if fclass != "" else ("No class specified",True)
    handle_economy_misformat = lambda fclass, applied = False : (fclass, applied) if fclass != "Economy / Economy" else ("Economy", True)
    handle_prem_economy_misformat = lambda fclass, applied = False : (fclass, applied) if fclass != "PremiumEconomy" else ("Premium Economy", True)

    filters = [handle_no_class, handle_economy_misformat, handle_prem_economy_misformat]

    return filters

print(get_all_flights_count())
print(get_morning_flights_count())
print(get_sweden_flight_data())
print(get_top10_destinations())
print(get_average_journey_times())
print(get_flight_class_appearances())