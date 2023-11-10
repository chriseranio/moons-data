import requests
import json
import pandas as pd

'''

This Python program presents a menu with options that will generate interesting data points from any or all of the 
celestial bodies which have moons orbiting them in our Solar System.

For example, if you pick only Jupiter a CSV file will output to the directory that contains all Jupiter's many moons
and their density gravity, inclination, and much more.

The program pulls API data from System Solaire API. Simply run "python moons.py" and follow the menu prompts.

'''

all_moons = requests.get("https://api.le-systeme-solaire.net/rest/bodies/").json()

def get_moons(all_moons):
    extract_moon_data = [body for body in all_moons['bodies'] if body['isPlanet'] is False]
    allmoons = pd.json_normalize(extract_moon_data).set_index('id')
    allmoons = allmoons.drop(columns='moons')
    planet_names = allmoons['aroundPlanet.planet'].unique()
    for i, name in enumerate(planet_names):
        print(f"{i+1}. {name}")

    picker = input("Choose the celestial body to generate it's moons data for (separated by comma), for all type 'All': ")
    if picker.lower() == "all":
        return allmoons
    else:
        choices = picker.split(",")
        selected_planets = [planet_names[int(choice)-1] for choice in choices]
        selected_moons = allmoons.loc[allmoons['aroundPlanet.planet'].isin(selected_planets)]
        return selected_moons

planets_moons = get_moons(all_moons)
output_filename = input("Please name the Excel file to be generated: ")
planets_moons.to_excel(f"{output_filename}.xlsx", index=False)