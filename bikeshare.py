import time
import numpy as np
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# get filters provides user input filers  (City, Month, Day of the Week, and raw data).
def get_filters():
    print('\nHello! Let\'s explore some US bikeshare data!')

    while True:
        print("\nWhich city would you like to review? \nCurrent options are: 'Chicago', 'New York City', or 'Washington'.") 
        city = input("Please enter your selection here: ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid city. Please try again.")

    months = ('january', 'february', 'march', 'april', 'may', 'june', 'all')

    while True:
        print("\nWhich month would you like to analyze?")
        print("You may select: 'January', 'February', 'March', 'April', 'May', 'June', or 'all'.")
        month = input("\nPlease type your selection here: ").lower()
        if month in months:
            break
        else:
            print("Invalid month. Please try 'all' or any single month up to June.")

    while True:
        print("\nWhich day of the week would you like to analyze?")
        print("You may enter 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', or 'all'.")
        day = input("\nPlease type your selection: ").lower()
        if day in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
            break
        else:
            print("Invalid day of the week. Please try again")

    while True:
        fivelines = input("\nWould you like the raw data to be displayed five rows at a time?\nPlease type: 'Yes' or 'No': ").lower()
        if fivelines in ('yes', 'no'):
            break
        else:
            print("Invalid input. Please only enter 'Yes' or 'No' in the prompt below!")            
    
#prints data concerning selected filters before the program executes the analysis 
    print("")
    print('-'*40)
    print(f"You have selected the following filters:\nCity: {city.title()}\nMonth: {month.title()}\nDay: {day.title()}")
    print(f"Raw data to be displayed and partitioned: {fivelines.title()}")
    print('-'*40)
#Ask the user if they would like to contine with the selected filters or would like to restart the program
    while True:
        cont = input("\nWoud you like to contine with these filters?\nPlease type 'Yes' to continue or 'No' to reset and start over: ").lower() 
        if cont == 'yes':
            break
        elif cont == 'no':
            get_filters()
        else:
            print("\nInvalid input. Please only enter 'Yes' or 'No' in the prompt below!")
                
    return city, month, day, fivelines

def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])

    # Converts the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extracts month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    # Filters by month if applicable
    if month != 'all':
        df = df[df['month'] == month]

    # Filters by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df

#Displays DataFrame in rows of five pausing after each to allow user input.
def display_data_in_chunks(df, chunk_size=5):
    start_loc = 0
    while start_loc < len(df):
        print(df.iloc[start_loc:start_loc + chunk_size])
        start_loc += chunk_size
        if start_loc < len(df):
            user_input = input("\nPress Enter to continue, or type 'stop' to end: ")
            if user_input.lower() == 'stop':
                break

def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = df['month'].mode()[0]
    print(f"Most Common Month: {most_common_month.title()}")

    most_common_day = df['day_of_week'].mode()[0]
    print(f"Most Common Day of Week: {most_common_day.title()}")

    most_common_hour = df['hour'].mode()[0]
    print(f"Most Common Hour: {most_common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_common_start_station = df['Start Station'].mode()[0]
    print(f"Most Common Start Station: {most_common_start_station}")
    
    most_common_end_station = df['End Station'].mode()[0]
    print(f"Most Common End Station: {most_common_end_station}")
    
    df['trip'] = df['Start Station'] + " to " + df['End Station']
    most_common_trip = df['trip'].mode()[0]
    print(f"Most Common Trip: {most_common_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print(f"Total Travel Time: {total_travel_time} seconds.")

    mean_travel_time = df['Trip Duration'].mean()
    print(f"Mean Travel Time: {mean_travel_time} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print("User Types:\n", user_types)

    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nGender Counts:\n", gender_counts)
    else:
        print("\nGender data not available for this city.")
    
    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print(f"\nEarliest Birth Year: {earliest_birth_year}")
        print(f"Most Recent Birth Year: {most_recent_birth_year}")
        print(f"Most Common Birth Year: {most_common_birth_year}")
    else:
        print("\nBirth Year data not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#loads filter data, displays raw data (if requested), prints statistics, and ask if user if they would like to restart. 
def main():
    while True:
        city, month, day, fivelines = get_filters()
        df = load_data(city, month, day)

        if fivelines == 'yes':
            display_data_in_chunks(df)
        else:
            print("")

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no: ')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
