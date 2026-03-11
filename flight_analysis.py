"""
****************************************************************************
Additional info
 1. I declare that my work contins no examples of misconduct, such as
 plagiarism, or collusion.
 2. Any code taken from other sources is referenced within my code solution.
 3. Student ID: w2153319/20240311
 4. Date: 09/05/2025
****************************************************************************

"""
from graphics import *
import csv # Import CSV module 
import math


# Global list to hold flight data loaded from CSV
data_list = []

# Dictionary of airport codes mapped to airport names
AIRPORTS = {
    "LHR": "London Heathrow",
    "MAD": "Madrid Adolfo Suárez-Barajas",
    "CDG": "Charles De Gaulle International",
    "IST": "Istanbul Airport International",
    "AMS": "Amsterdam Schiphol",
    "LIS": "Lisbon Portela",
    "FRA": "Frankfurt Main",
    "FCO": "Rome Fiumicino",
    "MUC": "Munich International",
    "BCN": "Barcelona International",
}

# Dictionary of airline codes mapped to airline names
AIRLINES = {
    "BA": "British Airways",
    "AF": "Air France",
    "AY": "Finnair",
    "KL": "KLM",
    "SK": "Scandinavian Airlines",
    "TP": "TAP Air Portugal",
    "TK": "Turkish Airlines",
    "W6": "Wizz Air",
    "U2": "easyJet",
    "FR": "Ryanair",
    "A3": "Aegean Airlines",
    "SN": "Brussels Airlines",
    "EK": "Emirates",
    "QR": "Qatar Airways",
    "IB": "Iberia",
    "LH": "Lufthansa",
}

def load_csv(selected_csv):
    #Load data from a CSV file into the global data_list.
    with open(selected_csv, 'r', newline='') as file:
        csvreader = csv.reader(file)
        header = next(csvreader, None)   # Skip header row
        for row in csvreader:
            data_list.append(row)

def prompt_airportcode() :
    #Prompt user to enter a valid 3-letter airport code.
    while True:
        code = input(
            "Please enter the three-letter code for the departure city required  : "
        ).strip().upper()
        if len(code) != 3:   # Ensure code is exactly 3 characters
            print("Wrong code length - please enter a three-letter city code:", end="")
            continue
        return code
        
def prompt_year() :
    #Prompt user for a valid year between 2000 and 2025.
    while True:
        raw = input("Please enter the year required in the format YYYY :").strip()
        if not (raw.isdigit() and len(raw) == 4):   # Must be a 4-digit number
            print("Wrong data type - please enter a four-digit year value:", end="")
            continue
        year = int(raw)
        if year < 2000 or year > 2025:   # Range check
            print("Out of range - please enter a value from 2000 to 2025:", end="")
            continue
        return year

def display_header(filename, year): 
    #Print header information when a file is selected.
    airport_code = filename[:3].upper()
    stars = "*" * 81
    print(stars)
    print(f"File {filename} selected - Planes departing {airport_code} airport {year}.")
    print(stars)

def calculate_outcomes():
    #Process loaded data and calculate statistics about flights.
    total_flights = len(data_list)       # Total flights
    runway1 = 0                          # Flights departing runway 1
    over500 = 0                          # Flights over 500 miles
    british = 0                          # British Airways flights
    rain_flights = 0                     # Flights in rainy weather
    scheduled_actual_diff_count = 0      # Delayed flights
    rain_hours = set()                   # Hours when it rained
    dest_counter = {}                    # Destination counts (manual dictionary)

    # Iterate over each row of flight data
    for row in data_list:
        if len(row) < 10:  
            continue

        flight_num = row[1].strip()
        scheduled_dep = row[2].strip()
        actual_dep = row[3].strip()
        dest_code = row[4].strip()
        distance_str = row[5].strip()
        runway = row[8].strip()
        weather = row[9].strip().lower()

        if runway == "1":   # Count runway 1 flights
            runway1 += 1
        try:
            distance = int(distance_str)
            if distance > 500:
                over500 += 1
        except:
            pass   # Ignore invalid distances
        if flight_num.upper().startswith("BA"):   # British Airways flights
            british += 1
        if "rain" in weather:   # Flights in rain
            rain_flights += 1
            if ":" in scheduled_dep:
                hour = scheduled_dep.split(":")[0]
                rain_hours.add(hour)
        if scheduled_dep != actual_dep:   # Check delays
            scheduled_actual_diff_count += 1

        # Count destination codes manually
        if dest_code not in dest_counter:
            dest_counter[dest_code] = 0
        dest_counter[dest_code] += 1

    # Average flights per hour
    avg_perhour = round(total_flights / 12, 2) if total_flights else 0.00
    
    # Count Air France flights
    af_count = 0
    for row in data_list:
        if len(row) >= 2:
            code = row[1].strip().upper()
            if code.startswith("AF"):
                af_count += 1
                
  
    airfrance_pct = round(af_count / total_flights * 100, 2) if total_flights else 0.00
    delayed_pct = round(scheduled_actual_diff_count / total_flights * 100, 2) if total_flights else 0.00
    hours_ofrain = len(rain_hours)

    # Find most common destination
    most_common_names = []
    if dest_counter:
        max_freq = max(dest_counter.values())
        most_common_codes = []
        for code, cnt in dest_counter.items():
            if cnt == max_freq:
                most_common_codes.append(code)

        most_common_names = []
        for code in most_common_codes:
            if code in AIRPORTS:
                most_common_names.append(AIRPORTS[code])
            else:
                most_common_names.append(code)
                      
    # Return results in dictionary
    outcomes = {
        "total": total_flights,
        "runway1": runway1,
        "over500": over500,
        "british": british,
        "rain_flights": rain_flights,
        "avg_perhour": avg_perhour,
        "airfrance_pct": airfrance_pct,
        "delayed_pct": delayed_pct,
        "hours_ofrain": hours_ofrain,
        "common_dests": most_common_names,
    }
    return outcomes

def display_outcomes(outcomes):
    #Print results to the console.
    print(f"The total number of flights from this airport was {outcomes['total']}")
    print(f"The total number of flights departing Runway one was {outcomes['runway1']}")
    print(f"The total number of departures of flights over 500 miles was {outcomes['over500']}")
    print(f"There were {outcomes['british']} British Airways flights from this airport")
    print(f"There were {outcomes['rain_flights']} flights from this airport departing in rain")
    print("")
    print(f"There was an average of {outcomes['avg_perhour']} flights per hour from this airport")
    print(f"Air France planes made up {outcomes['airfrance_pct']}% of all departures")
    print(f"{outcomes['delayed_pct']}% of all departures were delayed")
    print(f"There were {outcomes['hours_ofrain']} hours in which rain fell")
    print(f"The most common destinations are {outcomes['common_dests']}")

def save_results(filename, year, outcomes):
    #Save the calculated outcomes to a results.txt file.
    airport_code = filename[:3].upper()
    with open("results.txt", "a", encoding="utf-8") as file:
        file.write("*******************************************************************\n")
        file.write(f"File {filename} selected - Planes departing {airport_code} {year}.\n")
        file.write("*******************************************************************\n")
        file.write("\n")
        file.write(f"The total number of flights from this airport was {outcomes['total']}\n")
        file.write(f"The total number of flights departing Runway one was {outcomes['runway1']}\n")
        file.write(f"The total number of departures of flights over 500 miles was {outcomes['over500']}\n")
        file.write(f"There were {outcomes['british']} British Airways flights from this airport\n")
        file.write(f"There were {outcomes['rain_flights']} flights from this airport departing in rain\n")
        file.write(f"There was an average of {outcomes['avg_perhour']} flights per hour from this airport\n")
        file.write(f"Air France planes made up {outcomes['airfrance_pct']}% of all departures\n")
        file.write(f"{outcomes['delayed_pct']}% of all departures were delayed\n")
        file.write(f"There were {outcomes['hours_ofrain']} hours in which rain fell\n")
        file.write(f"The most common destinations are {outcomes['common_dests']}\n")
        file.write("\n")
        file.write("\n")

def prompt_airline_code() :
    #Prompt user for a valid 2-character airline code for histogram plotting.
    while True:
        code = input("Enter a two-character Airline code to plot a histogram: ").strip().upper()
        if len(code) != 2:
            print("Enter the two-character Airline code to plot a histogram : ", end="")
            continue
        if code not in AIRLINES:
            print("Unavailable Airline code please try again:", end="")
            continue
        return code

def count_departures_per_hour(airline_code) :
   #Count the number of departures per hour (0–11) for a given airline.
    counts = [0] * 12
    for row in data_list:
        if len(row) < 3:
            continue
        flight_num = row[1].strip().upper()
        if not flight_num.startswith(airline_code):   # Only count selected airline
            continue
        sched = row[2].strip()
        if ":" in sched:
            try:
                hour = int(sched.split(":")[0])
                if 0 <= hour <= 11:   # Only first 12 hours
                    counts[hour] += 1
            except:
                continue
    return counts

def draw_histogram(airline_code, filename, year, counts) :
    
    airline_name = AIRLINES[airline_code]
    airport_code = filename[:3].upper()
    win = GraphWin("Histogram", 900, 600)
    win.setCoords(-1, -2, 13, max(counts) + 5 if counts else 10)

    # Draw bars 
    for hour in range(12):
        bar_height = counts[hour]
        rect = Rectangle(Point(hour + 0.2, 0), Point(hour + 0.8, bar_height))
        rect.setFill("lightgreen")
        rect.setOutline("darkgreen")
        rect.draw(win)

        # Label above bar
        Text(Point(hour + 0.5, bar_height + 0.5), str(bar_height)).draw(win)

        # Hour labels below
        Text(Point(hour + 0.5, -0.8), f"{hour:02}").draw(win)

    # Title
    title = Text(Point(6, max(counts) + 3 if counts else 8),
                 f"Departures by hour for {airline_name} from {airport_code} {year}")
    title.setSize(14)
    title.setStyle("bold")
    title.draw(win)

    # Subtitle for x-axis
    Text(Point(6, -1.5), "Hours 00:00 to 12:00").draw(win)

    
    win.getMouse()
    win.close() 
    

def main():
    
    while True:
        code = prompt_airportcode()
        year = prompt_year()
        filename = f"{code}{year}.csv"
        try:
            data_list.clear()
            load_csv(filename)
            display_header(filename, year)
        except FileNotFoundError:
            print(f"File {filename} not found - please ensure it's in the same folder as this script.")
            return
        except Exception as e:
            print(f"An error occurred while loading {filename}: {e}")
            return

        # Process outcomes
        outcomes = calculate_outcomes()
        display_outcomes(outcomes)
        save_results(filename, year, outcomes)
        print("\nResults saved to results.txt")

        # Draw histogram for chosen airline
        airline_code = prompt_airline_code()
        counts = count_departures_per_hour(airline_code)
        draw_histogram(airline_code, filename, year, counts)
        while True:
            again = input("Do you want to analyse another CSV file (Y/N)? ").strip().upper()
            if again in ["Y", "N"]:
                break
            print("Invalid input - please enter Y or N only.")
        if again == "N":
            print("Program terminated.")
            break
    
        


if __name__ == "__main__":
    main()

