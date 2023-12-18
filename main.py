import PySimpleGUI as sg
import requests
import json
from datetime import datetime
from geopy.geocoders import Nominatim

def main():
    """
    The `main` function is the entry point of the program. It calls several other functions to get the location, coordinates, weather information, and then displays the weather details.

    Example Usage:
    main()

    Inputs:
    No inputs are required for the `main` function.

    Flow:
    1. The `main` function calls the `get_location` function to retrieve the user's location.
    2. It then passes the location to the `get_coordinates` function to obtain the latitude and longitude.
    3. The latitude and longitude are used as inputs for the `get_weather_info` function, which returns the temperature, feels like temperature, weather description, current date, current time, sunrise time, and sunset time.
    4. Finally, the `weather_display` function is called with the location and all the weather information to display the weather details to the user.

    Outputs:
    The `main` function does not return any values. It is responsible for calling other functions to retrieve and display the weather information.
    """
    location = get_location()
    latitude, longitude = get_coordinates(location)
    temperature, feels_like, weather, current_date, current_time, sunrise, sunset = get_weather_info(latitude, longitude)
    weather_display(location, temperature, feels_like, weather, current_date, current_time, sunrise, sunset)


def get_location(): 
    """
    Get the location from the user through a GUI input window.

    Returns:
        str: The location entered by the user.
    """
    layout = [
        [sg.InputText('Location')],
        [sg.Button('Ok'), sg.Button('Cancel')]
    ]

    window = sg.Window('Get location' ,layout)

    while True:
        event, values = window.read()
        if event == 'Cancel':
            break
        location = values[0]
        
        window.close()
        return location

def get_coordinates(location):
    """
    Retrieve the latitude and longitude coordinates of a given location.

    Args:
        location (str): The name of the location for which coordinates are needed.

    Returns:
        tuple: A tuple containing the latitude and longitude coordinates of the given location.

    Example:
        >>> location = "New York City"
        >>> latitude, longitude = get_coordinates(location)
        >>> print(latitude, longitude)
        40.7128 -74.0060
    """

    # Calling the Nominatim tool and create class
    loc = Nominatim(user_agent="Geopy Library")

    # Entering the location name
    getloc = loc.geocode(location)

    # Return the coordinates
    return getloc.latitude, getloc.longitude   

def get_weather_info(latitude, longitude):
    """
    Retrieves weather information for a given latitude and longitude.

    Args:
        latitude (float): The latitude of the location for which weather information is requested.
        longitude (float): The longitude of the location for which weather information is requested.

    Returns:
        tuple: A tuple containing the following weather information:
            - temperature (float): The current temperature in Celsius.
            - feels_like (float): The current feels like temperature in Celsius.
            - weather (str): A description of the current weather conditions.
            - current_date (datetime.date): The current date.
            - current_time (datetime.time): The current time.
            - sunrise (datetime.time): The time of sunrise.
            - sunset (datetime.time): The time of sunset.
    """
    # Set up the request 
    response = requests.get(f"https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&units=metric&exclude=hourly,daily,minutely&appid=e910ca23666885e532ef4983ecbbfb32")
    current_weather = response.json()['current']
    
    # Convert timestamps to times and dates
    current_time = datetime.fromtimestamp(current_weather['dt']).time()
    current_date = datetime.fromtimestamp(current_weather['dt']).date()
    sunrise = datetime.fromtimestamp(current_weather['sunrise']).time()
    sunset = datetime.fromtimestamp(current_weather['sunset']).time()

    
    # Get weather info
    temperature = current_weather['temp']
    feels_like = current_weather['feels_like']
    weather = current_weather['weather'][0]['description']

    # Return weather info
    return temperature, feels_like, weather, current_date, current_time, sunrise, sunset



def weather_display(location, temperature, feels_like, weather, current_date, current_time, sunrise, sunset):
    """
    Display the weather information in a GUI window.

    Args:
        location (str): The name of the location for which the weather information is being displayed.
        temperature (str): The current temperature.
        feels_like (str): The temperature that it feels like.
        weather (str): The description of the weather.
        current_date (str): The current date.
        current_time (str): The current time.
        sunrise (str): The time of sunrise.
        sunset (str): The time of sunset.

    Example:
        weather_display("New York", "25°C", "28°C", "Sunny", "2021-07-15", "12:00 PM", "06:00 AM", "08:00 PM")

    """
    layout = [
        [sg.Text(f'The weather in {location} is')],
        [sg.Text(f'Date: {current_date}'), sg.Text(f'Time: {current_time}')],
        [sg.Text(f'Sunrise: {sunrise}'), sg.Text(f'Sunset: {sunset}')],
        [sg.Text(f'Temperature: {temperature}'), sg.Text(f'Feels Like: {feels_like}')],
        [sg.Text(f'Weather description: {weather}')],
        [sg.Button('Close')]
    ]

    window = sg.Window("Weather info", layout)

    while True:
        event, values = window.read()
        if event == 'Close' or event == sg.WIN_CLOSE_ATTEMPTED_EVENT or event == sg.WIN_CLOSED:
            break


if __name__ == "__main__":
    main()