import json
from queue import Queue
from bs4 import BeautifulSoup
import requests

F1COM_STARTING_POINT = "https://www.formula1.com/en/results.html/"
F1COM_DRIVER_STARTING_POINT = "/drivers.html"


def retrive_F1com_data():
    pass

class Vertex:
    def __init__(self, name):
        self.name = name
        self.connected_to = []

    def __str__(self):
        """String representation of the object."""
        string = "This is "+self.name
        return string

def main():
    response = requests.get(F1COM_STARTING_POINT+"2022"+F1COM_DRIVER_STARTING_POINT)
    soup = BeautifulSoup(response.text, 'html.parser')
    DRIVER_2022 = soup.find("tbody").find_all("a")
    print(DRIVER_2022)
    subject_options = [i.findAll('option') for i in soup.findAll('select', {"name":"driverRef"})]
    # print(subject_options[0])
    for driver in DRIVER_2022:
        driver_name = driver.text.strip()
        print(driver_name)

if __name__ == "__main__":
    # your control code for Part 4 (interactive search) should go here
    main()