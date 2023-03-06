# Orbital Ephemeris Message (OEM) Data Query and Containerization 
This folder, `homework05` , contains a program called `iss_tracker.py`, `Dockerfile` and this `README.md` file. `iss_tracker.py` takes in xml data from [NASA](https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml) and converts the xml information to a dictionary. With this data type, the user can use flask to query for the program to return the options listed under Flask App. This is important because by sifting through this data, the user can harvest important information about the International Space Station's trajectory to predict clear paths and prevent collisions. 
## How to Access the Data
The [data](https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml) is available through this hyperlink on ISS's trajectory website. This link is already in `iss_tracker.py` therefore downloading the raw XML data is only necessary if the user prefers to view the structure of the data. 
## Flask App
The flask app contains 12 routes: 
1. `/` : returns the entire data set
2. `/epochs` : returns a list of all epochs in the data set 
3. `/epochs/<epoch>`: returns state vector for a specific epoch in the data set
4.  `/epochs/<epoch>/speed`: returns the instantaneous speed for a specific epoch using the cartesian velocity vectors in the state vector.
5. `/help`: returns a string that lists all available routes and their methods
6. `/delete-data`: deletes the entire data set off the json file that is loaded from the url
7. `/post-data`: replaces the deleted data with the data from the website
8. `/comment`: returns the 'comment' list from ISS data
9. `/header`: returns the 'header' dictionary from ISS data
10. `/metadata`: returns the 'metadata' dictionary from ISS data
11. `/epochs/<epoch>/location` returns the latitude, longitude, altitude, and geoposition for a user-specified epoch
12. `/now`: returns the same values as '/../../location' but for the epoch that is nearest to the current time
## Run Instructions
### To Pull an Image from Docker Hub
To pull this image from Docker Hub, type `docker pull amymanning1/iss_tracker:midterm` in your command line. Ensure you are in the same directory as `iss_tracker.py`. 
### Build a new Image
To build a new image using the existing Dockerfile in this repo, `docker build -t <dockerhubusername>/iss_tracker:midterm .` filling in the <> with your Docker Hub username. Check that the image built using `docker images`. 
### Run the Containerized App
To test the image you either built or pulled, use `docker run -it --rm -p 5000:5000 username/iss_tracker:midterm` to start flask inside of the container. The `-p` flag is important to connect the port on the user's device to the port on the container. Because the virtual machines where this program is used are connected on port 5000, it is imperative that we connect that to the container's port 5000. In another window with the command line, interact with the program `curl 127.0.0.1:5000/epochs` ensuring the order of connections is `<host port>:<container port>`. If you are having issues determining the port, check the flask window where it says `* Running on http://127.0.0.1:5000`, remove the `http://` and use that address, filling in the addresses with what your flask displays. 
#### Docker Tip
Each time you change the `Dockerfile` or `iss_tracker.py`, you must rebuild the container using the build commands found in the above section. 
### Example Paths and Outputs
+ `curl 127.0.0.1:5000/`
   - `},
                "X_DOT": {
                  "#text": "5.2410359153923798",
                  "@units": "km/s"
                },
                "Y": {
                  "#text": "-5991.3267501460596",
                  "@units": "km"
                },
                "Y_DOT": {
                  "#text": "0.32894397165270001",
                  "@units": "km/s"
                },
                "Z": {
                  "#text": "1991.1683453687999",
                  "@units": "km"
                },
                "Z_DOT": {
                  "#text": "-5.57976406061041",
                  "@units": "km/s"
                }
              },
              {`
   - This is only a sample output, the actual output is much longer
- `curl 127.0.0.1:5000/epochs`
  - `[
  "2023-048T12:00:00.000Z",
  "2023-048T12:04:00.000Z",
  "2023-048T12:08:00.000Z",
  "2023-048T12:12:00.000Z",
  "2023-048T12:16:00.000Z", ...
        ]`
* `curl 127.0.0.1:5000/epochs/2023-063T11:15:00.000Z`
   - `{
  "EPOCH": "2023-063T11:15:00.000Z",
  "X": {
    "#text": "-3230.7742245286299",
    "@units": "km"
  },
  "X_DOT": {
    "#text": "-4.7139536603293903",
    "@units": "km/s"
  },
  "Y": {
    "#text": "5860.46590407639",
    "@units": "km"
  },
  "Y_DOT": {
    "#text": "-1.4242336555306401",
    "@units": "km/s"
  },
  "Z": {
    "#text": "-1183.7150780833999",
    "@units": "km"
  },
  "Z_DOT": {
    "#text": "5.8695829401146797",
    "@units": "km/s"
  }
}`
+ `curl 127.0.0.1:5000/epochs/2023-063T11:15:00.000Z/speed`
   - `7.6617102861022035`
* `curl 127.0.0.1:5000/help`
   - This program accesses different data elements from the ISS Trajectory site by NASA. Available routes include:
    /                               returns the entire data set ('GET' method) ....
+ `curl -X DELETE 127.0.0.1:5000/delete-data`
   - []
   - NOTE: Anything curled after this query will be empty until `post-data` is run
   - NOTE: you must include `-X DELETE`, you will receive an error if you do not
* `curl -X POST 127.0.0.1:5000/post-data`
   - `},
                "X_DOT": {
                  "#text": "5.2410359153923798",
                  "@units": "km/s"
                },
+ `curl 127.0.0.1:5000/comment`
  - `[
  "Units are in kg and m^2",
  "MASS=473413.00",
  "DRAG_AREA=1618.40",
  "DRAG_COEFF=2.20",
  "SOLAR_RAD_AREA=0.00",
  "SOLAR_RAD_COEFF=0.00",
  "Orbits start at the ascending node epoch",
  "ISS first asc. node: EPOCH = 2023-03-03T16:45:01.089 $ ORBIT = 2542 $ LAN(DEG) = 78.61627",
  "ISS last asc. node : EPOCH = 2023-03-18T14:19:09.505 $ ORBIT = 2773 $ LAN(DEG) = 26.64425",
  "Begin sequence of events",
  "TRAJECTORY EVENT SUMMARY:",
  null,
  "|       EVENT        |       TIG        | ORB |   DV    |   HA    |   HP    |",
  "|                    |       GMT        |     |   M/S   |   KM    |   KM    |",
  "|                    |                  |     |  (F/S)  |  (NM)   |  (NM)   |",
  "=============================================================================",
  "GMT 067 ISS Reboost   067:20:02:00.000             1.0     427.0     407.3",
  "(3.3)   (230.6)   (219.9)",
  null,
  "Crew05 Undock         068:08:00:00.000             0.0     427.0     410.8",
  "(0.0)   (230.6)   (221.8)",
  null,
  "SpX27 Launch          074:00:30:00.000             0.0     426.7     409.9",
  "(0.0)   (230.4)   (221.3)",
  null,
  "SpX27 Docking         075:12:00:00.000             0.0     426.7     409.8",
  "(0.0)   (230.4)   (221.3)",
  null,
  "=============================================================================",
  "End sequence of events"
]`
* `curl 127.0.0.1:5000/header`
  - {
  "CREATION_DATE": "2023-063T04:34:04.606Z",
  "ORIGINATOR": "JSC"
}
+ `curl 127.0.0.1:5000/metadata`
  - {
  "CENTER_NAME": "EARTH",
  "OBJECT_ID": "1998-067-A",
  "OBJECT_NAME": "ISS",
  "REF_FRAME": "EME2000",
  "START_TIME": "2023-062T15:47:35.995Z",
  "STOP_TIME": "2023-077T15:47:35.995Z",
  "TIME_SYSTEM": "UTC"
}
* `{
  "altitude": 420.6341310992075,
  "geolocation": {
    "address": {
      "ISO3166-2-lvl4": "US-AZ",
      "country": "United States",
      "country_code": "us",
      "county": "Pima County",
      "state": "Arizona"
    },
    "boundingbox": [
      "31.4254941",
      "32.514423",
      "-113.333992",
      "-110.4473185"
    ],
    "display_name": "Pima County, Arizona, United States",
    "lat": "32.1112624",
    "licence": "Data \u00a9 OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
    "lon": "-111.6546163",
    "osm_id": 1832206,
    "osm_type": "relation",
    "place_id": 298478213
  },
  "latitude": 31.815794472620638,
  "longitude": -111.15947635149035
}`
* `curl 127.0.0.1:5000/now`
  - {
  "closest_epoch": "2023-077T15:47:35.995Z",
  "location": {
    "altitude": 428.6137193341565,
    "geolocation": {
      "address": {
        "ISO3166-2-lvl4": "AO-BGU",
        "country": "Angola",
        "country_code": "ao",
        "state": "Benguela Province"
      },
      "boundingbox": [
        "-13.874445",
        "-11.7589169",
        "12.3159609",
        "15.1108341"
      ],
      "display_name": "Benguela Province, Angola",
      "lat": "-12.9104657",
      "licence": "Data \u00a9 OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
      "lon": "14.0356608",
      "osm_id": 1802540,
      "osm_type": "relation",
      "place_id": 298335923
    },
    "latitude": -13.479282638990789,
    "longitude": 13.126560404682472
  },
  "seconds_from_now": -1079988.4640915394
} 
## About the Data
This data is coordinates on the international space station's current location. After the headers, the state vectors are listed at four-minute intervals and updated three times a week. This data is collected to determine the trajectory of the ISS to prevent collisions or it going too far off course. Determining trajectory is also important to maintain communication with the ground. There is a unique epoch for every data point which acts as an id. The data inside the state vector is the epoch, X, Y, Z, X_DOT, Y_DOT, and Z_DOT coordinates. The raw coordinates are in kilometers and the _DOT coordinates and the time derivatives or velocities at each position in km/s.   
