import datetime

# importing dependencies
import matplotlib.pyplot as plt
import requests

# Constants
BASE_URI = "http://api.openweathermap.org/data/2.5/forecast/daily"
CONVERSON_CONSTANT = 273.15

def get_inputs():
    try:
        # Getting key from decoupled source
        info_obj = open('info.txt','r+')
        key = info_obj.read().split("=")[1].strip()
    except FileNotFoundError:
        # Get key from input
        key = input("Please Enter the key : ").strip()

    city = input("Please Enter Name of the city : ").strip()

    # Query data as dictonary
    params = {
            'q': city,
            'cnt': 10,
            'appid': key
            }

    return params

# Utility Functions
def get_datetime(timestamp):
    '''
    Get datetime object from the UNIX timestamp
    '''
    datetime_obj = datetime.datetime.fromtimestamp(timestamp)
    return datetime_obj

def get_celsius(kelvin):
    '''
    Get Celsius temperature from kelvin
    '''
    return kelvin - CONVERSON_CONSTANT

def get_json(data):
    '''
    Get JSON data from API url and we have a valid input return it
    '''
    response = requests.get(BASE_URI, params=data)
    if response.status_code == 404:
        print("Invalid City Name, please try again")
        return False
    elif response.status_code == 401:
        print("Invalid API key.")
        return False
    elif response.status_code == 200:
        return response.json()

def get_data_dict(weather_data):
    compiled_data = {
            'highs':[],
            'lows':[],
            'humidity':[],
            'dates':[]
            }
    
    # Read data from JSON Dictionary to lists
    for item in weather_data["list"]:
        compiled_data['dates'].append(get_datetime(item["dt"]).strftime("%d/%m"))
        compiled_data['highs'].append(get_celsius(item["temp"]["max"]))
        compiled_data['lows'].append(get_celsius(item["temp"]["min"]))
        compiled_data['humidity'].append(item["humidity"])

    return compiled_data

def plot_graph(city_name, compiled_data):
    dates = compiled_data['dates']
    humidity = compiled_data['humidity']
    highs = compiled_data['highs']
    lows = compiled_data['lows']

    # Plot High and Low Temperature Graph
    fig, (axs1, axs2) = plt.subplots(2)
    fig.suptitle("Forecast: " + city_name)
    axs1.set_ylabel('Temperature ( Celsius )')

    # Creating line object for legends
    high_line, = axs1.plot(dates, highs, 'o-', label="Max")
    low_line, = axs1.plot(dates, lows, 'o-', label="Min")

    # Increase Y-axis limit to make room for annotations
    y_lim = axs1.get_ylim()
    axs1.set_ylim((y_lim[0]-5, y_lim[1]+5))

    #creating legends
    legend_high = axs1.legend(
            bbox_to_anchor=(1, 1.25), 
            handles=[high_line,low_line,], 
            loc="upper right", 
            borderaxespad=0)

    for x, y in zip(dates, highs):
        label = "{:.2f}".format(y)
        axs1.annotate(label, # this is the text
                      (x,y), # this is the point to label
                      textcoords="offset points", # how to position the text
                      xytext=(0,-10), # distance from text to points (x,y)
                      fontsize="x-small",
                      ha='center')

    for x, y in zip(dates, lows):
        label = "{:.2f}".format(y)
        axs1.annotate(label, # this is the text
                      (x,y), # this is the point to label
                      textcoords="offset points", # how to position the text
                      xytext=(0,-10), # distance from text to points (x,y)
                      fontsize="x-small",
                      ha='center')

    # Plot Humidity Graph
    axs2.set_ylabel('Humidity ( Grams Per Kg )')
    axs2.set_xlabel("Date")
    axs2.plot(dates, humidity, 'o-')

    # Increase Y-axis limit to make room for annotations
    y_lim = axs2.get_ylim()
    axs2.set_ylim((y_lim[0]-10, y_lim[1]+10))

    for x, y in zip(dates, humidity):
        label = "{:.1f}".format(y)
        axs2.annotate(label, # this is the text
                      (x,y), # this is the point to label
                      textcoords="offset points", # how to position the text
                      xytext=(5,10), # distance from text to points (x,y)
                      fontsize="x-small",
                      ha='center')
    plt.show()

if __name__ == "__main__":
    weather_data = get_json(get_inputs())
    while not weather_data:
        print("Something Went wrong. Please try again.")
        weather_data = get_json(get_inputs())
    else:
        city_name = weather_data["city"]["name"]+", "+weather_data["city"]["country"]
        compiled_data = get_data_dict(weather_data)
        plot_graph(city_name, compiled_data)
