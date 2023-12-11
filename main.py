import PySimpleGUI as sg
import requests
import json


def main():
    location = get_location()
    x = get_weather_info(location)
    extract_weather_info(x)



def get_location():
    #TODO: Ask for permission on location

    location = sg.popup_get_text('Which place would you like to see the weather?', size=(100, 200))
    return location

def get_weather_info(location):
    x = requests.get(f'http://api.weatherapi.com/v1/current.json?key=fda6842448dd49d4a09113333230712&q={location}&aqi=no')
    if x.text == '{"error":{"code":1006,"message":"No matching location found."}}':
        sg.popup("No such location found")
    else:
        return x
    
def extract_weather_info(x):
    
        



if __name__ == "__main__":
    main()