from flask import Flask, request
import xmltodict, requests, math, time
app = Flask(__name__)

from geopy.geocoders import Nominatim
geocoder = Nominatim(user_agent='iss_tracker')


url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'
response = requests.get(url)
data = xmltodict.parse(response.text)
@app.route('/', methods=['GET'])
def entire_set() -> dict:
    """
    This function accesses the entire data set.
    Args: There are no arguments.
    Return: data (dict): A dictionary of dictionaries and lists containing the entire data set. 
    """
    return data

@app.route('/epochs', methods=['GET'])
def get_epochs() -> list:
    """
    This function generates a list of all Epochs in the data set.
    Args: there are no parameters called in the function definition, however the dictionary 'data' is accessed in this function.
    Return: epoch_list (list): A list of all epochs in the dataset. 
    """
    if data == None:
        return []
        exit()
    offset = request.args.get('offset',0)
    limit = request.args.get('limit',len(data))
    if offset:
        try: 
            offset = int(offset)
        except ValueError:
            return 'Invalid offset parameter; must be zero or a positive integer'
    if limit:
        try:
            limit = int(limit)
        except ValueError:
            return 'Please enter a positive integer or zero'
    epoch_list = []
    count = 0
    offset_count = 0
    for d in data['ndm']['oem']['body']['segment']['data']['stateVector']:
        if count == limit:
           break
        offset_count = offset_count + 1
        if offset_count >= offset:
            epoch_list.append(d['EPOCH'])
            count = count + 1
    return epoch_list

@app.route('/epochs/<epoch>', methods=['GET'])
def state_vec(epoch) -> list:
    """
    This function displays a state vector for a specific Epoch from the data set referenced by the user in the query line.
    Args: epoch (str): An epoch referenced by the user in the query line that is available in the data set. 
    Return: spec_state (list): Information specific to a certain state vector queried by the user.
    """
    if data == None:
        return []
        exit()
    epoch_list = []
    for d in data['ndm']['oem']['body']['segment']['data']['stateVector']:
        epoch_list.append(d['EPOCH'])
    if epoch in epoch_list:
        ind = epoch_list.index(epoch)
        spec_state = data['ndm']['oem']['body']['segment']['data']['stateVector'][ind] 
        return spec_state
    else:
        return 'Error, please enter a valid Epoch value'

@app.route('/epochs/<epoch>/speed', methods=['GET'])
def calc_speed(epoch) -> float:
    """
    This function calculates the instantaneous speed for a specific Epoch queried by the user in the data set
    Args: epoch (str): An epoch referenced by the user in the query line that is available in the data set.
    Return: speed (float): The instantaneous speed for a specific epoch calculated using the formula for speed from Cartesian velocity vectors. 
    """
    if data == None:
        return []
        exit()
    epoch_list = []
    for d in data['ndm']['oem']['body']['segment']['data']['stateVector']:
        epoch_list.append(d['EPOCH'])
    if epoch in epoch_list:
        ind = epoch_list.index(epoch)
        spec_state = data['ndm']['oem']['body']['segment']['data']['stateVector'][ind]
        x_dot = float(spec_state['X_DOT']['#text'])
        y_dot = float(spec_state['Y_DOT']['#text'])
        z_dot = float(spec_state['Z_DOT']['#text'])
        speed = math.sqrt(x_dot**2 + y_dot**2 + z_dot**2)
        return str(speed) 
    else:
        return 'Error, please enter a valid Epoch value'


@app.route('/help', methods=['GET'])
def help() -> str:
    """
    This function provides brief descriptions of all available routes and their methods.
    Args: There are no arguments for this function.
    Return: help_str (str): A long string that provides brief descriptions of all available routes and their methods.
    """
    help_str = """This program accesses different data elements from the ISS Trajectory site by NASA. Available routes include:
    /                               returns the entire data set ('GET' method)
    /epochs?limit=1&offset=4        where the entire path is enclosed in quotes if the ampersand is used. This returns a list of epochs up to the user's limit beginning at the user queried offset. There are default values for limit and offset so the user can truncate the question mark and everything after it if they desire. ('GET' method)
    /epochs/<epoch>                 returns the state vector associated with the specific epoch requested in the <> ('GET' method)
    /epochs/<epoch>/speed           calculates the instantaneous speed of a user-queried epoch ('GET' method)
    /delete-data                    deletes the entire data set ('DELETE' method)
    /post-data                      replaces deleted data ('POST' method)
    """
    return help_str

@app.route('/delete-data', methods=['DELETE'])
def delete_data() -> dict:
    """
    This function deletes all the memory for the data set. 
    Args: data (dict): The entire dataset of ISS trajectories.
    Returns: an empty dictionary 
    """
    # need to save data as a json locally in order to delete
    # going to need to go back through and recode paths so I can have deletion privileges
    global data
    data = data.clear()
    return []

@app.route('/post-data', methods=['POST'])
def replace_data() -> dict:
    """
    This function replaces the data in data_usable using a 'get' request.
    Args: none
    Returns: data (dict): the data replaced. 
    """
    response = requests.get(url)
    data = xmltodict.parse(response.text)
    return data

@app.route('/comment', methods=['GET'])
def get_comments() -> list:
    """
    This function returns the comments list object from the data set.
    Args: none
    Returns: comment_list (list): a list of all the comment objects in the data set.
    """
    
    if data == None:
        return []
        exit()
    comment_list = []
    for m in data['ndm']['oem']['body']['segment']['data']['COMMENT']:
        comment_list.append(m)
    return comment_list

@app.route('/header', methods=['GET'])
def get_header() -> dict:
    """
    This function returns the header information from the data set.
    Args: none
    Returns: header (dict): a dictionary of all the header information.
    """
    header = data['ndm']['oem']['header']
    return header

@app.route('/metadata', methods=['GET'])
def get_meta() -> dict:
    """
    This function returns the metadata dict object from the data set.
    Args: none
    Returns: meta (dict): dictionary object of metadata extracted from data set.
    """
    meta = data['ndm']['oem']['body']['segment']['metadata']
    return meta

@app.route('/epochs/<epoch>/location', methods=['GET'])
def location(epoch) -> dict:
    """
    This function takes in a user-specified epoch and calculates the latitude, longitude, altitude, and geoposition.
    Args: epoch (str): An epoch referenced by the user in the query line that is available in the data set.
    Returns: loc_dict (dict): a dictionary with the keys latitude, longitude, altitude, and geoposition and their corresponding values.
    """
    MEAN_EARTH_RADIUS = 6371 # km
    epoch_list=[]
    if data == None:
        return []
        exit()
    for d in data['ndm']['oem']['body']['segment']['data']['stateVector']:
        epoch_list.append(d['EPOCH'])
    if epoch in epoch_list:
        zoom_set = 15
        ind = epoch_list.index(epoch)
        spec_state = data['ndm']['oem']['body']['segment']['data']['stateVector'][ind]
        x = float(spec_state['X']['#text'])
        y = float(spec_state['Y']['#text'])
        z = float(spec_state['Z']['#text'])
        
        epoch_splitter = epoch.split('T', 1) # series of splits to access hrs and minutes needed for lon calculations
        time = epoch_splitter[1]
        remove_z = time.split('.',1)
        hrs_list = remove_z[0].split(':')
        hrs = float(hrs_list[0])
        mins = float(hrs_list[1])
        
        lat = math.degrees(math.atan2(z, math.sqrt(x**2 + y**2)))
        lon = math.degrees(math.atan2(y, x)) - ((hrs-12)+(mins/60))*(360/24) + 24
        alt = math.sqrt(x**2 + y**2 + z**2) - MEAN_EARTH_RADIUS
        geoloc = geocoder.reverse((lat, lon), zoom=zoom_set, language='en')
        if geoloc == None:
            while True:
                zoom_set = zoom_set - 1
                if zoom_set < 0 or zoom_set > 18:
                    return 'Error, could not find geolocation. The ISS might be over a large area of ocean or the initial zoom_set is not between 0 and 18.'
                geoloc = geocoder.reverse((lat, lon), zoom=zoom_set, language='en')
                if geoloc != None:
                    break
        
        loc_dict = {'latitude' : lat, 'longitude' : lon, 'altitude' : alt, 'geolocation' : geoloc.raw}
        return loc_dict


    else:
        return 'Error, please enter a valid Epoch value'

@app.route('/now', methods=['GET'])
def now() -> dict:
    """
    This function notes the current time and returns a dictionary of latitude, longitude, altitude, and geoposition of the epoch nearest in time.
    Args: none
    Returns: now_dict (dict): A dictionary with key values: latitude, longitude, altitude, and geoposition of the most recent epoch.
    {} (dict): an empty dict if the data has been deleted and not reposted.
    """
    if data == None:
        return {}
        exit()
    # get current time
    # convert to seconds if it is not
    # for loop to find closest epoch to it (might have to use slicing methodfrom location route)
    # once smallest difference is found, return that epoch's information as well as the epoch itself as 'closest epoch' and the difference in seconds
    closest_epoch = 0;
    smallest_diff = 1e6;
    MEAN_EARTH_RADIUS = 6371 #km
    time_current = time.time()
    epoch_list=[]
    for d in data['ndm']['oem']['body']['segment']['data']['stateVector']:
        epoch_list.append(d['EPOCH'])
        epoch = d['EPOCH']
        time_epoch = time.mktime(time.strptime(epoch[:-5], '%Y-%jT%H:%M:%S'))
        difference = time_current - time_epoch
        if difference < smallest_diff:
            smallest_diff = difference
            closest_epoch = epoch
            ind = epoch_list.index(epoch)

    spec_state = data['ndm']['oem']['body']['segment']['data']['stateVector'][ind]
    x = float(spec_state['X']['#text'])
    y = float(spec_state['Y']['#text'])
    z = float(spec_state['Z']['#text'])

    epoch_splitter = epoch.split('T', 1) # series of splits to access hrs and minutes needed for lon calculations
    time_notmod = epoch_splitter[1]
    remove_z = time_notmod.split('.',1)
    hrs_list = remove_z[0].split(':')
    hrs = float(hrs_list[0])
    mins = float(hrs_list[1])

    lat = math.degrees(math.atan2(z, math.sqrt(x**2 + y**2)))
    lon = math.degrees(math.atan2(y, x)) - ((hrs-12)+(mins/60))*(360/24) + 24
    alt = math.sqrt(x**2 + y**2 + z**2) - MEAN_EARTH_RADIUS
    geoloc = geocoder.reverse((lat, lon), zoom=15, language='en')
    if geoloc == None:
            while True:
                zoom_set = zoom_set - 1
                if zoom_set < 0 or zoom_set > 18:
                    return 'Error, could not find geolocation. The ISS might be over a large area of ocean or the initial zoom_set is not between 0 and 18.'
                geoloc = geocoder.reverse((lat, lon), zoom=zoom_set, language='en')
                if geoloc != None:
                    break
    loc_dict = {'latitude' : lat, 'longitude' : lon, 'altitude' : alt, 'geolocation' : geoloc.raw}

    now_dict = {'closest_epoch' : closest_epoch, 'seconds_from_now':difference, 'location':loc_dict}
    return now_dict


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
