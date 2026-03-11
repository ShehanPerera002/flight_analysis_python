# flight_analysis_python

A Python tool that processes airport departure data from CSV files to generate statistics and hourly histograms.

## Features
* **Data Processing:** Calculates total flights, runway usage, and weather impacts.
* **CSV Integration:** Loads and parses flight data dynamically based on user input.
* **Visualizations:** Generates histograms of departures by hour using the `graphics.py` library.
* **Reporting:** Automatically saves calculation summaries to a text file.

## How to Run
1. Ensure you have `graphics.py` in the root directory.
2. Run the script: `flight_analysis.py`
3. Enter the 3-letter airport code (e.g., LHR) and year (2024).
