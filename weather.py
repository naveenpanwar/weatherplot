import datetime

# importing dependencies
import matplotlib.pyplot as plt
import requests

# Constants
BASE_URI = "http://api.openweathermap.org/data/2.5/forecast/daily"
CONVERSON_CONSTANT = 273.15

try:
    # Getting key from decoupled source
    info_obj = open('info.txt','r+')
    key = info_obj.read().split("=")[1].strip()
except FileNotFoundError:
    # Get key from input
    key = input("Please Enter the key : ").strip()

# Query data as dictonary
DATA = {
        'q': 'dehradun',
        'cnt': 10,
        'appid': key
        }

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

# Get JSON data
response = requests.get(BASE_URI, params=DATA)
weather_data = response.json()

city_name = weather_data["city"]["name"]+", "+weather_data["city"]["country"]

highs = []
lows = []
humidity = []
dates = []

# Read data from JSON Dictionary to lists
for item in weather_data["list"]:
    dates.append(get_datetime(item["dt"]).strftime("%d/%m"))
    highs.append(get_celsius(item["temp"]["max"]))
    lows.append(get_celsius(item["temp"]["min"]))
    humidity.append(item["humidity"])

# Plot High and Low Temperature Graph
fig, (axs1, axs2) = plt.subplots(2)
fig.suptitle("Forecast: " + city_name)
axs1.set_ylabel('Temperature ( Celsius )')
axs1.plot(dates, highs, 'o-')
axs1.plot(dates, lows, 'o-')
for x, y in zip(dates, highs):
    label = "{:.2f}".format(y)
    axs1.annotate(label, # this is the text
                  (x,y), # this is the point to label
                  textcoords="offset points", # how to position the text
                  xytext=(0,-15), # distance from text to points (x,y)
                  fontsize="x-small",
                  ha='center')

for x, y in zip(dates, lows):
    label = "{:.2f}".format(y)
    axs1.annotate(label, # this is the text
                  (x,y), # this is the point to label
                  textcoords="offset points", # how to position the text
                  xytext=(0,10), # distance from text to points (x,y)
                  fontsize="x-small",
                  ha='center')

# Plot Humidity Graph
axs2.set_ylabel('Humidity ( Grams Per Kg )')
axs2.set_xlabel("Date")
axs2.plot(dates, humidity, 'o-')
for x, y in zip(dates, humidity):
    label = "{:.1f}".format(y)
    axs2.annotate(label, # this is the text
                  (x,y), # this is the point to label
                  textcoords="offset points", # how to position the text
                  xytext=(10,3), # distance from text to points (x,y)
                  fontsize="x-small",
                  ha='center')
plt.show()