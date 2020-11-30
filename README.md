# traveltek-task

To run the application visit: http://turtle-637.getforge.io/

The application frontend is composed of a basic static site, whilst the backend is a deployed API hosted on AWS' API gateway. 

Static site code is shown in the website folder and API code is shown in the API folder.

On the static site, the first 3 menu choices (left to right) only show text, however the final 3 deliver interactive content (e.g. graphs that show extra info on user mouse over/onclick).

Issues:
The API is fairly slow, takes a few seconds to retrieve requested data. This is probably because the flight data XML file has to be loaded and processed on each request and probably could have been optimised through storage on inital processing to JSON, and retrieval of this JSON.  
