import Final_Project_Liyang_utl as utl

def main():
    driver_dict = {}
    team_dict = {}
    yearly_data = {}
    first_input = 1950
    last_input = 2023
    first_input_raw = input("Please enter a year you would like to start the data gathering(between 1950 ~ 2022, enter anything else will use the default value 1950): \n")
    print()
    try:
        first_input = int(first_input_raw)

        last_input_raw = input("Please enter a year you would like to end the data gathering(between 1950 ~ 2022, enter anything else will use the default value 2022): \n")
        print()
        try:
            last_input = int(last_input_raw) + 1
        except ValueError:
            print("Input a number for years")
            print()
    except ValueError:
        print("Input a number for years")
        print()

    for i in range(first_input, last_input):
        data = utl.retrive_F1com_data(i, driver_dict, team_dict)
        yearly_data = yearly_data | data

    utl.write_json("yearly_data.json", yearly_data)
    print("The following F1 season are recorded for connection: ")
    print(yearly_data.keys())
    condition = True
    combine_dict = team_dict | driver_dict
    while condition:
        start = input("\nPlease input a driver name(Last, First. Case sensitive) as your starting point: \n")
        print()
        end_input = input("Input a driver name(Last, First) you would like to end connection with: \n")
        print()
        try:
            utl.make_connection(combine_dict=combine_dict, start=start, end_input=end_input)
        except KeyError:
            print("No such driver(s), please doublecheck your spelling or driver.")
        checker = input("Would you like to try another connection? (Input yes to continute, anything else will exit)\n")
        if checker.lower() != "yes":
            condition = False


if __name__ == "__main__":
    # your control code for Part 4 (interactive search) should go here
    main()
