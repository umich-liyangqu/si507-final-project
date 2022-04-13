import json
from queue import Queue
from bs4 import BeautifulSoup
import requests

F1COM_STARTING_POINT = "https://www.formula1.com/en/results.html/"
F1COM_DRIVER_STARTING_POINT = "/drivers.html"

YEAR_DICT = {}

def retrive_F1com_data(i, YEAR_DICT):
    year = str(i)
    if year in YEAR_DICT:
        return YEAR_DICT(year)
    else:
        response = requests.get(F1COM_STARTING_POINT+year+F1COM_DRIVER_STARTING_POINT)
        soup = BeautifulSoup(response.text, 'html.parser')
        DRIVER_2022 = soup.find("tbody").find_all("a")
        print(DRIVER_2022)
        for driver in DRIVER_2022:
            driver_name = driver.text.strip()
            print(driver_name)

class Vertex:
    def __init__(self, name):
        self.name = name
        self.connected_to = []

    def __str__(self):
        """String representation of the object."""
        string = "This is "+self.name
        return string

def main():
    pass

if __name__ == "__main__":
    # your control code for Part 4 (interactive search) should go here
    main()