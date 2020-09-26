# Weather Forecast for 10 Days #
The script creates a graph of the Weather forecast for the given city.

## Requirements / Dependencies ##
* matplotlib
* requests

## Function Description ##
#### get_inputs() ####
* Takes no arguments.
* Input the API key if *info.txt* does not exist
* Input city name
* Returned Values
	* Returns a dictonary of query parameters

#### get_datetime() ####
* Arguments
	* UNIX timestamp
* Returned Values
	* Returns a datetime object.

#### get_celsius() ####
* Arguments
	* Temperature in kelvin 
* Returned Values
	* Corresponding temperature in __Celsius__

#### get_json() ####
* Arguments
	* Query parameters to the URI as a python dictonary 
* Returned Values
	* Returns JSON as python object if request succeds

#### get_data_dict() ####
* Arguments
	* Response python object 
* Returned Values
	* Returns a dictonary with the *dates*, *max_temp*, *min_temp*, *humidity* lists.

#### plot_graph() ####
* Arguments
	* Takes *city_name* and *compiled_data* as parameters
* Returned Values
	* Creates a graph with __pyplot__ of the following data 
