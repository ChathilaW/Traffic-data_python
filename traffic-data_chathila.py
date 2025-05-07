#Author: WIJESINGHE ARACHCHIGE CHATHILA UTHSARA WIJESINGHE
#Date: 24/12/2024

# Task A : Input Validation
def validate_date_input():
    """Prompts the user for a date in DD MM YYYY format
    and validates whether they are -in correct range
                                   -of correct type
    """
    while True: # validates range of day for month 2 if non-leap year
        while True: # validates range of day for month
            while True: # validates range,type for day
                try:
                    day = input("Please enter the day of the survey in the format dd:")
                    day = int(day)
                    if 1 > day or day > 31:
                        print("Day is out of range(1-31)")
                        continue
                    else:
                        break
                except:
                    print("Integer required")

            while True: #validates range,type for month
                try:
                    month = int(input("Please enter the month of the survey in the format MM:"))
                    if 1 > month or month > 12:
                        print("Month is out of range(1-12)")
                        continue
                    else:
                        break
                except:
                    print("Integer required")

            if month == 2 and day >= 30:
                print("Day is out of range(1-29) for month 02")
                continue
            elif month in [4,6,9,11] and day > 30:
                print(f'Day is out of range(1-30) for month {month}')
                continue
            else:
                break

        while True: # validates range,type for year
            try:
                year = int(input("Please enter the year of the survey in the format YYYY:"))
                if 2000 > year or year > 2024:
                    print("Year is out of range(2000-2024)")
                    continue
                else:
                    break
            except:
                print("Integer required")

        if year % 4 != 0 and month == 2 and day == 29:
            print(f'Day is out of range(1-28) for month 02 of non-leap year {year}')
            continue
        else:
            break

    day = f"{day:02d}"      # Converting day to a 2 digit string
    month = f"{month:02d}"  # Converting month to a 2 digit string
    year = str(year)
    global date
    date = day + month + year  # Converting day,month,year to a single string
    global Date
    Date = f'{day}/{month}/{year}' # To use in the Histogram

# Task B : Processed Outcomes
def process_csv_data(file_path):
    """
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics
    """
    import csv
    from datetime import timedelta
    total_vehicles = 0                  # Total no.of vehicles going through both junction
    total_trucks = 0                    # Total no.of trucks going through both junction
    total_hybrid_vehicles = 0           # Total no.of electric vehicles going through both junction
    total_2wheeled_vehicles = 0         # Total no.of 2 wheeled vehicles going through both junction
    elm_out_north_buss_tot = 0          # Total no.of buses leaving Elm Avenue/Rabbit Road towards North
    straight_total = 0                  # Total no.of vehicles passing through both junctions without turning left or right
    over_limit_total = 0                # Total no.of vehicles over the speed limit
    elm_avenue_total = 0                # Total no.of vehicles through Elm Avenue/Rabbit Road
    hanley_highway_total = 0            # Total no.of vehicles going through Hanley Highway/Westway
    elm_scooter_total = 0               # Total no.of scooters going through Elm Avenue/Rabbit Road
    bicycle_total = 0                   # Total no.of bicycles
    max_veh_hour_hanley = 0             # Maximum no.of vehicles in an hour in Hanley Highway/Westway
    time_at_max_veh_hour_hanley = 0     # Time at when busiest on Hanley Highway starts
    time_at_max_veh_hour_hanley1 = 0    # Time at when busiest on Hanley Highway ends
    rain_hours = set()                  # No of hours rained
    elm = []                            # List of total no.of vehicles for each hour on Elm Avenue/Rabbit Road
    hanley = []                         # List of total no.of vehicles for each hour
    tot_per_hour_hanley = 0             # Calculating total no.of vehicles per hour on hanley road
    tot_per_hour_elm = 0                # Calculating total no.of vehicles per hour on elm road
    global outcomes                     # To get all calculated outcomes as a list and to use it in other defined functions


    date_csv = "traffic_data" + file_path + ".csv"
    hour_start = "0:0:0" # For comparing with hours in csv when finding vehicles per hour,vehicles at peak hour,peak hour on Hanley Highway
    h, m, s = map(int, hour_start.split(':'))
    hour_start = timedelta(hours=h, minutes=m, seconds=s)
    hour_start1 = hour_start # For comparing with hours in csv when listing vehicles per hour on Elm Avenue
    try: # Validates whether file is available
        with open(date_csv, 'r') as file:
            traffic = list(csv.reader(file))
            total_rows = len(traffic) # To find the index of the last row
            for i, row in enumerate(traffic):
                if i == 0:  # Skips 1st row containing topics
                    continue

                hour1 = row[2]
                h1, m1, s1 = map(int, hour1.split(':'))
                hour1 = timedelta(hours=h1, minutes=m1, seconds=s1)

                total_vehicles += 1

                if row[8] == "Truck": # Finding total no.of trucks
                    total_trucks += 1
                if row[9] == "True": # Finding total no.of electric vehicles
                    total_hybrid_vehicles += 1
                if row[8] == "Bicycle" or row[8] == "Motorcycle" or row[8] == "Scooter": # Finding total no.of 2 wheeled vehicles
                    total_2wheeled_vehicles += 1
                if row[8] == "Bicycle": # Finding total no.of bicycles
                    bicycle_total += 1
                if row[0] == "Elm Avenue/Rabbit Road" and row[4] == "N" and row[8] == "Buss":
                    elm_out_north_buss_tot += 1
                if row[3] == row[4]: # Finding Total no.of vehicles going straight
                    straight_total += 1
                if int(row[6]) < int(row[7]): # Finding total no.of vehicles exceeding the speed limit
                    over_limit_total += 1
                if row[0] == "Elm Avenue/Rabbit Road": # Finding total no.of vehicles on Elm Avenue
                    elm_avenue_total += 1
                if row[0] == "Hanley Highway/Westway": # Finding total no.of vehicles on Hanley Highway
                    hanley_highway_total += 1
                if row[0] == "Elm Avenue/Rabbit Road" and row[8] == "Scooter":
                    elm_scooter_total += 1

                if row[0] == "Hanley Highway/Westway": # Finding peak hour,vehicles at peak hour and listing total vehicles per hour on Hanley Highway
                    while True: # To detect hours with no vehicles
                        if hour_start == timedelta(hours=23):
                            tot_per_hour_hanley += 1
                            if tot_per_hour_hanley > max_veh_hour_hanley:
                                time_at_max_veh_hour_hanley  =  hour1  -  timedelta(hours=1, minutes=m1, seconds=s1) # If Starting time of peak hour is at 23
                                time_at_max_veh_hour_hanley1  =  time_at_max_veh_hour_hanley  +  timedelta(hours=1) # If Ending time of peak hour is at 23
                                max_veh_hour_hanley  =  tot_per_hour_hanley  # If maximum vehicle at an hour on hanley highway is at 23
                                break
                            else:
                                break

                        elif hour1 < hour_start + timedelta(hours=1):
                            tot_per_hour_hanley  +=  1
                            break

                        elif tot_per_hour_hanley > max_veh_hour_hanley:
                            time_at_max_veh_hour_hanley  =  hour1  -  timedelta(hours=1, minutes=m1, seconds=s1) # Finding Starting time of peak hour
                            time_at_max_veh_hour_hanley1  =  time_at_max_veh_hour_hanley  +  timedelta(hours = 1) # Finding Ending time of peak hour
                            max_veh_hour_hanley  =  tot_per_hour_hanley  # Finding maximum vehicle at an hour on hanley highway
                            hanley.append(tot_per_hour_hanley)
                            hour_start  +=  timedelta(hours=1)
                            tot_per_hour_hanley = 0
                            continue

                        else:
                            hanley.append(tot_per_hour_hanley)
                            hour_start  +=   timedelta(hours=1)
                            tot_per_hour_hanley = 0
                            continue

                if row[5] == "Light Rain" or row[5] == "Heavy Rain": # Finding no.of hours rained
                    rain_hours.add(h1)


                if row[0] == "Elm Avenue/Rabbit Road": # Listing total vehicles per hour on Elm Avenue
                    while True: # To detect hours with no vehicles
                        if hour_start1 == timedelta(hours=23):
                            tot_per_hour_elm  +=  1
                            break
                        else:
                            if hour1 < hour_start1 + timedelta(hours=1):
                                tot_per_hour_elm  +=  1
                                break
                            else:
                                elm.append(tot_per_hour_elm)
                                hour_start1  +=  timedelta(hours=1)
                                tot_per_hour_elm = 0
                                continue

                if i == (total_rows-1): # To detect hours with no vehicles at the end
                    if h1 != 23:
                        hanley.append(tot_per_hour_hanley) # Appends the previous hour vehicles to the hanley list
                        tot_per_hour_hanley = 0 # resets to zero to use in the empty hours of hanley highway

                        elm.append(tot_per_hour_elm) # Appends the previous hour vehicles to the elm list
                        tot_per_hour_elm = 0 # resets to zero to use in the empty hours of elm avenue

                        for i in range(int(h1),23): # Detecting no.of empty hours
                            hanley.append(tot_per_hour_hanley)
                            elm.append(tot_per_hour_elm)
                            
                    else: # If there are no empty hours at the end
                        hanley.append(tot_per_hour_hanley) # Appends the 23rd hour vehicles to the hanley list
                        elm.append(tot_per_hour_elm) # Appends the 23rd hour vehicles to the elm list


            truck_percentage = round((total_trucks / total_vehicles) * 100,0)               # Calculating percentage of trucks
            elm_scoot_percentage = round((elm_scooter_total / elm_avenue_total) * 100,0)    # Calculating percentage of scooters on Elm Avenue
            average_bicycle_per_hour = round(bicycle_total / 24) # Calculating average bicycles per hour

        file.close()
        outcomes = [date_csv,
                    total_vehicles,
                    total_trucks,
                    total_hybrid_vehicles,
                    total_2wheeled_vehicles,
                    elm_out_north_buss_tot,
                    straight_total,
                    truck_percentage,
                    average_bicycle_per_hour,
                    over_limit_total,
                    elm_avenue_total,
                    hanley_highway_total,
                    elm_scoot_percentage,
                    max_veh_hour_hanley,
                    time_at_max_veh_hour_hanley,
                    time_at_max_veh_hour_hanley1,
                    len(rain_hours),
                    elm,
                    hanley]
    except:
        print("File is missing / not available")
        outcomes = [] # Creates an empty list if the file is not available


# Task B : Displaying Outcomes
def display_outcomes(outcomes):
    """
    Displays the calculated outcomes in a clear and formatted way.
    """
    if len(outcomes) == 0: # Avoids displaying outcomes when file is missing/not available
        pass
    else:
        print(" ")
        print("**********************************")
        print(f'data file selected is {outcomes[0]}')
        print("**********************************")
        print(" ")
        print(f'The total number of vehicles recorded for this date is {outcomes[1]}')
        print(f'The total number of trucks recorded for this date is {outcomes[2]}')
        print(f'The total number of electric vehicles for this date is {outcomes[3]}')
        print(f'The total number of two-wheeled vehicles for this date is {outcomes[4]}')
        print(f'The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes[5]}')
        print(f'The total number of Vehicles through both junctions not turning left or right is {outcomes[6]}')
        print(f'The percentage of total vehicles recorded that are trucks for this date is {outcomes[7]} %')
        print(f'the average number of Bikes per hour for this date is {outcomes[8]}')
        print(" ")
        print(f'The total number of Vehicles recorded as over the speed limit for this date is {outcomes[9]}')
        print(f'The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes[10]}')
        print(f'The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes[11]}')
        print(f'{outcomes[12]} % of vehicles recorded through Elm Avenue/Rabbit Road are scooters.')
        print(" ")
        print(f'The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes[13]}')
        print(f'The most vehicles through Hanley Highway/Westway were recorded between {outcomes[14]} and {outcomes[15]}')
        print(f'Number of hours of rain for this date is {outcomes[16]}')
        print(" ")


# Task C : Save Result To Text File
def save_result_to_file(outcomes, file_name="Results.txt"):
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    if len(outcomes) == 0: # Avoids appending to a text file when file is missing/not available
        pass
    else:
        with open(file_name,'a') as file1:
            file1.write(f'data file selected is {outcomes[0]}\n')
            file1.write(f'The total number of vehicles recorded for this date is {outcomes[1]}\n')
            file1.write(f'The total number of trucks recorded for this date is {outcomes[2]}\n')
            file1.write(f'The total number of electric vehicles for this date is {outcomes[3]}\n')
            file1.write(f'The total number of two-wheeled vehicles for this date is {outcomes[4]}\n')
            file1.write(f'The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes[5]}\n')
            file1.write(f'The total number of Vehicles through both junctions not turning left or right is {outcomes[6]}\n')
            file1.write(f'Total number of vehicles passing through both junctions without turning left or right = {outcomes[7]}\n')
            file1.write(f'the average number of Bikes per hour for this date is {outcomes[8]} \n')
            file1.write(f'The total number of Vehicles recorded as over the speed limit for this date is {outcomes[9]}\n')
            file1.write(f'The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes[10]}\n')
            file1.write(f'The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes[11]}\n')
            file1.write(f'{outcomes[12]} % of vehicles recorded through Elm Avenue/Rabbit Road are scooters.\n')
            file1.write(f'The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes[13]}\n')
            file1.write(f'The most vehicles through Hanley Highway/Westway were recorded between {outcomes[14]} and {outcomes[15]}\n')
            file1.write(f'Number of hours of rain for this date is {outcomes[16]}\n')
            file1.write("\n")
            file1.write("*************************\n")
            file1.write("\n")
            file1.close()


def histogram_validation():  # Avoids displaying histogram if csv file not available
    if len(outcomes) != 0:
        # Task D : Histogram Display
        import tkinter as tk

        class HistogramApp:
            """
            Initializes the histogram application with the traffic data and selected date.
            """
            def __init__(self, data1, data2, data3):
                self.data1 = data1
                self.data2 = data2
                self.data3 = data3
                self.root = tk.Tk()
                self.root.title("Histogram")
                self.canvas = None  # Will hold the canvas for drawing

            def setup_window(self):
                """
                Sets up the Tkinter window and canvas for the histogram.
                """
                self.width = 1300
                self.height = 800
                self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="white")
                self.canvas.pack()


            def draw_histogram(self):
                """
                Draws the paired bar histogram with axes, labels, and bars.
                """
                self.padding_left = 80      # keeping blank space from left side of the window
                self.padding_right = 50     # keeping blank space from right side of the window
                self.padding_bottom = 80    # keeping blank space from the bottom of the window
                self.padding_top = 100      # keeping blank space from the top of the window

                max_value = max(max(self.data1), max(self.data2)) # Finding value of the tallest bar
                max_height = self.height - self.padding_bottom - (self.padding_top + 90) # creating maximum usable height of the window while keeping space for topic and legends

                bar_space = 10  # For keeping white space between paired bars
                bar_width = (self.width - (self.padding_left + self.padding_right)) // (len(self.data1) * 2.5)  # finding maximum width of a single bar fitting to the window
                # *2 because there are 2 data sets , *0.5 because of the blank space between paired bars


                #CREATING X-AXIS
                self.canvas.create_line(self.padding_left, self.height - self.padding_bottom, self.width - self.padding_right, self.height - self.padding_bottom,
                                        width=1,
                                        fill="black",
                                        arrow=tk.LAST)
                #LABELING X-AXIS
                self.canvas.create_text(self.width / 2, self.height - self.padding_bottom + 40,
                                        text="Hours 00:00 to 24:00",
                                        font=("Arial", 13))

                #CREATING Y-AXIS
                self.canvas.create_line(self.padding_left, self.height - self.padding_bottom,
                                        self.padding_left, self.padding_top + 20,
                                        width=1,
                                        fill="black",
                                        arrow=tk.LAST)
                #LABELING Y-AXIS
                self.canvas.create_text(self.padding_left - 20, self.height / 2,
                                        text="Number  Of  Vehicles  Per  Hour",
                                        font=("Arial", 13),
                                        angle=90)


                for i in range(len(self.data1)):
                    # Calculating heights for bar1 & bar2
                    height1 = (self.data1[i] / max_value) * max_height # Finding bar 1 height respective to the max_value
                    height2 = (self.data2[i] / max_value) * max_height # Finding bar 2 height respective to the max_value

                    # Calculating x coordinates of bar1 & bar2
                    x1 = self.padding_left + i * (bar_width * 2 + bar_space) #starting x coordinate for bar 1
                    x2 = x1 + bar_width # Ending x coordinate for bar 1 / starting x coordinate for bar 2
                    x3 = x2 + bar_width # Ending x coordinate for bar 2

                    # Drawing bar for data1
                    self.canvas.create_rectangle(x1, (self.height - self.padding_bottom) - height1 , x2, self.height - self.padding_bottom,
                                                 fill="light green")
                                              # (starting x coordinate, top y coordinate, ending x coordinate, bottom y coordinate)
                    self.canvas.create_text((x1 + x2) / 2, (self.height - self.padding_bottom) - height1  - 10,
                                            text=str(self.data1[i]),
                                            font=("Arial", 10),
                                            fill="light green")

                    # Creating bar for data2
                    self.canvas.create_rectangle(x2, (self.height - self.padding_bottom) - height2, x3, self.height - self.padding_bottom, fill="salmon")
                                            # (starting x coordinate, top y coordinate, ending x coordinate, bottom y coordinate)
                    self.canvas.create_text((x2 + x3) / 2, ((self.height - self.padding_bottom) - height2) - 10,
                                            text=str(self.data2[i]),
                                            font=("Arial", 10),
                                            fill="salmon")

                    # Creating the x-axis label for the pair
                    self.canvas.create_text((x1 + x3) / 2, self.height - self.padding_bottom + 15,
                                            text=f"{i:02d}",
                                            font=("Arial", 10))

            def add_legend(self):

                #CREATING HISTOGRAM TITLE
                self.canvas.create_text(self.padding_left, self.padding_top - 70,
                                        text=f"Histogram of Vehicle Frequency per hour {self.data3} ",
                                        anchor="w",
                                        font=("Arial", 17, "bold"))

                #CREATING LEGENDS
                legend_y = self.padding_top - 50

                self.canvas.create_rectangle(self.padding_left, legend_y, self.padding_left + 16, legend_y + 16,
                                             fill="light green")
                self.canvas.create_text(self.padding_left + 21, legend_y + 8,
                                        text="Elm Avenue/Rabbit Road",
                                        anchor="w",
                                        font=("Arial", 11))
                
                self.canvas.create_rectangle(self.padding_left, legend_y + 21, self.padding_left + 16, legend_y + 36,
                                             fill="salmon")
                self.canvas.create_text(self.padding_left + 21, legend_y + 28,
                                        text="Hanley Highway/Westway",
                                        anchor="w",
                                        font=("Arial", 11))

            def run(self):
                """
                Runs the Tkinter main loop to display the histogram.
                """
                self.setup_window()
                self.draw_histogram()
                self.add_legend()
                self.root.mainloop()

        app = HistogramApp(outcomes[17], outcomes[18], Date)
        app.run()
    else:
        pass


class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.current_data = None

    def load_csv_file(self):
        """
        Loads a CSV file and processes its data.
        """
        validate_date_input()
        process_csv_data(date)
        display_outcomes(outcomes)
        save_result_to_file(outcomes)
        histogram_validation()


    def handle_user_interaction(self):
        """
        Handles user input for processing multiple files.
        """
        while True:
            continue_validation = input("Do you want select another data file for a different date?Y/N:").upper()
            if continue_validation == 'Y':
                self.load_csv_file()
            elif continue_validation == 'N':
                break
            else:
                print('Please enter "Y" or "N" only!')

    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        self.load_csv_file()
        self.handle_user_interaction()

run = MultiCSVProcessor()
run.process_files()
