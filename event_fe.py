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

        for row in reader:
            row_date = datetime.strptime(row['Date'], '%Y-%m-%d')
            # Check if the flight count is within one month before the target date and two weeks before the target date for the given city
            if one_month_ago <= row_date < two_weeks_ago:
                try:
                    flights_count_early += int(float(row[city]))
                except ValueError:
                    pass  # Skip this row if the value cannot be converted to an integer
            # Check if the flight count is within two weeks before the target date for the given city
            elif two_weeks_ago <= row_date <= target_date:
                try:
                    flights_count_before += int(float(row[city]))
                except ValueError:
                    pass  # Skip this row if the value cannot be converted to an integer

    return flights_count_early, flights_count_before


st.header('Event Growth Analysis')
# Example usage:
csv_file = 'numflights.csv'
city = st.text_input("Enter your target city: ")
target_date = st.text_input("Enter the target date (YYYY-MM-DD): ")
early_flights, before_flights = count_flights(csv_file, city, target_date)

if early_flights == None or before_flights == None: 
    st.write("Please enter a new target date or city")
else:
    st.write(f"Number of flights in {city} one month before {target_date} and in the two weeks leading to {target_date}:")
    st.write(f"Flights one month to 2 weeks before the target date: {early_flights}")
    st.write(f"Flights two weeks leading up to the target date: {before_flights}")
    st.write(f"Percent increase in flights: {((before_flights-early_flights)/early_flights)*100:.2f}%")
