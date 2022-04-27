from bs4 import BeautifulSoup
import requests
import json
from queue import Queue

F1COM_STARTING_POINT = "https://www.formula1.com/en/results.html/"
F1COM_DRIVER_STARTING_POINT = "/drivers.html"

YEAR_DICT = {}

def write_json(filepath, data, encoding='utf-8', ensure_ascii=False, indent=2):
    """Serializes object as JSON. Writes content to the provided filepath.

    Parameters:
        filepath (str): the path to the file
        data (dict)/(list): the data to be encoded as JSON and written to the file
        encoding (str): name of encoding used to encode the file
        ensure_ascii (str): if False non-ASCII characters are printed as is; otherwise
                            non-ASCII characters are escaped.
        indent (int): number of "pretty printed" indention spaces applied to encoded JSON

    Returns:
        None
    """

    with open(filepath, 'w', encoding=encoding) as file_obj:
        json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)

def retrive_F1com_data(i, driver_dict, team_dict): # i is the year input
    year = str(i)
    response = requests.get(F1COM_STARTING_POINT+year+F1COM_DRIVER_STARTING_POINT)
    soup = BeautifulSoup(response.text, 'html.parser')
    DRIVER_2022 = soup.find("tbody").find_all("a")

    yearly_dict = {
        i : []
    }
    p = 0
    driver_name = ''
    team_name = ""
    for driver in DRIVER_2022:
        p += 1
        driver_info = driver.text.strip()
        if p % 2 == 1:
            driver_name = driver_info.split()[0] + " " + driver_info.split()[1]
        else:
            team_name = driver_info
            team_class = Vertex(team_name)
            driver_class = Vertex(driver_name)
            if driver_name not in driver_dict: #create a new driver vertex if it is not existed before
                driver_dict[driver_name] = driver_class
                driver_class.connected_to.append(team_class)
            else: # Update an existing driver with new team inside it.
                team_existing_name = []
                for team in driver_dict[driver_name].connected_to:
                    team_existing_name.append(team.name)
                if team_name not in team_existing_name:
                    driver_dict[driver_name].connected_to.append(team_class)

            if team_name not in team_dict:
                team_dict[team_name] = team_class
                team_class.connected_to.append(driver_class)
            else:
                driver_existing_name = []
                for driver in team_dict[team_name].connected_to:
                    driver_existing_name.append(driver.name)
                if driver_name not in driver_existing_name:
                    team_dict[team_name].connected_to.append(driver_class)
            yearly_dict[i].append([driver_dict[driver_name].jsonable(), team_dict[team_name].jsonable()])

    return yearly_dict

class Vertex:
    def __init__(self, name):
        self.name = name
        self.connected_to = []

    def __str__(self):
        """String representation of the object."""
        string = "This is "+self.name
        return string

    def jsonable(self):
        connection = []
        for connection_vertex in self.connected_to:
            connection.append(connection_vertex.name)
        output = {
            'name': self.name,
            'connection': connection
        }
        return output

def make_connection(combine_dict, start, end_input):
    visited = {}
    level = {}
    parent = {}
    bfs_traversal_output = []
    queue = Queue()
    # SET UP COMPLETE
    for key in combine_dict:
        visited[key] = False
        parent[key] = None
        level[key] = 0
    visited[start] = True
    level[start] = 0
    queue.put(start)

    while not queue.empty():
        u = queue.get()
        bfs_traversal_output.append(u)

        for v in combine_dict[u].connected_to:
            #print(v.name)
            if not visited[v.name]:
                #print("pushed")
                visited[v.name] = True
                parent[v.name] = u
                level[v.name] = level[u] + 1
                queue.put(v.name)

    print("Connection established...")
    end = end_input
    connection = int(level[end_input] / 2)
    path = []
    while end_input is not None:
        path.append(end_input)
        end_input = parent[end_input]
    path.reverse()
    print(f"\nBetween {start} and {end}, there is {connection} connection with the path of \n{path} ")