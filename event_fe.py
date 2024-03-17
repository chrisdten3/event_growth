import csv
import streamlit as st
from datetime import datetime, timedelta

def count_flights(csv_file, city, target_date):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        flights_count_early = 0
        flights_count_before = 0
        target_date = datetime.strptime(target_date, '%Y-%m-%d')
        one_month_ago = target_date - timedelta(days=30)
        two_weeks_ago = target_date - timedelta(days=14)
        target_date_str = target_date.strftime('%Y-%m-%d')

        for row in reader:
            row_date = datetime.strptime(row['Date'], '%Y-%m-%d')
            # Check if the flight count is within one month before the target date and two weeks before the target date for the given city
            if one_month_ago <= row_date < two_weeks_ago:
                try:
                    flights_count_early += int(float(row[city]))
                except ValueError:
                    pass  # Skip this row if the value cannot be converted to an integer
            # Check if the flight count is within two weeks before the target date for the given city
            elif two_weeks_ago <= row_date < target_date:
                try:
                    flights_count_before += int(float(row[city]))
                except ValueError:
                    pass  # Skip this row if the value cannot be converted to an integer

    return flights_count_early, flights_count_before


st.header('Event Growth Analysis')
# Example usage:
csv_file = 'numflights.csv'
city = st.text_input("Enter the city: ")
target_date = st.text_input("Enter the target date (YYYY-MM-DD): ")
early_flights, before_flights = count_flights(csv_file, city, target_date)
print(f"Number of flights in {city} one month before {target_date} and in the two weeks leading to {target_date}:")
print(f"Early flights: {early_flights}")
print(f"Flights before target date: {before_flights}")
#print increase percentage of flights from early to before
print(f"Increase in flights: {((before_flights-early_flights)/early_flights)*100:.2f}%")