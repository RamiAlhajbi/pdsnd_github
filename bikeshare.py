import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_user_input( input_msg, valid_values):
    """handles the user input vs the valid values, and chaning it to lower case."""
    user_input =''
    
    while True:
        # Get input from the user
        user_input = input('\n'+input_msg+'\n').strip().lower()
        
        # Validate the input
        if user_input in valid_values:
            break
        else:
            print ('Invalid input. Please enter one of the following: {}'.format(valid_values))
    
    return user_input
              

def ask_month():
    """Asks user to specify a month to filter by.

    Returns:
        (str) month - name of the month to filter by.
    """
    
    return get_user_input('Which month - January, February, March, April, May, or June?', ['january', 'february', 'march', 'april', 'may', 'june'])

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_user_input('Would you like to see data for Chicago, New York, or Washington?', ['chicago', 'new york', 'washington'])

    filter = get_user_input('Would you like to filter the data by month, day, both, or not at all? type "none" for no time filter', ['month', 'day', 'both', 'none'])

    
    if filter == 'both':
        month = ask_month()
        day = get_user_input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday', ['monday', 'tuesday', 'wednesday', 'thuresday', 'friday', 'saturday', 'sunday'])
    elif filter == 'month':
        # TO DO: get user input for month (all, january, february, ... , june)
        month = ask_month()
        day = 'all'
    elif filter == 'day':
        # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        day = get_user_input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday', ['monday', 'tuesday', 'wednesday', 'thuresday', 'friday', 'saturday', 'sunday'])
        month = 'all'
    else:
        # If the user chooses 'none', no filters are applied
        month = 'all'
        day = 'all'
    
    # Display the filters applied
    print('\nYou have selected the following filters:', 
          f'City: {city.title()}, Month: {month.title()}, Day: {day.title()}')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding month number
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day.lower()]
    
    # Reset index after filtering
    df.reset_index(drop=True, inplace=True)


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print('Most common month:', months[most_common_month - 1])


    # TO DO: display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('Most common day of week:', most_common_day)


    # TO DO: display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print('Most common start hour:', most_common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station:', most_common_start_station)   


    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station:', most_common_end_station)


    # TO DO: display most frequent combination of start station and end station trip
    most_common_trip = (df['Start Station'] + ' to ' + df['End Station']).mode()[0]
    print('Most frequent combination of start and end station trip:', most_common_trip)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['End Time'] - df['Start Time']
    total_travel_time_seconds = total_travel_time.dt.total_seconds().sum()
    print('Total travel time in seconds:', total_travel_time_seconds)


    # TO DO: display mean travel time
    mean_travel_time_seconds = total_travel_time.dt.total_seconds().mean()
    print('Mean travel time in seconds:', mean_travel_time_seconds)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of user types:\n', user_types)

    # will check if the Gender column exist in the DataFrame
    if 'Gender' in df.columns:
        # TO DO: Display counts of gender
        user_gender = df['Gender'].value_counts()
        print('\nCounts of gender:\n', user_gender)
    else:
        print('\nGender data is not available for this city.')


        # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print('\nEarliest year of birth:', earliest_year)
        print('Most recent year of birth:', most_recent_year)
        print('Most common year of birth:', most_common_year)
    else:
        print('\nNo birth year data available for this city.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_row_data(df):
        """Display 5 rows each time based on the user request."""
        
        # Display raw data if the user wants to see it
        show_data = get_user_input('Would you like to see 5 rows of raw data? Enter yes or no.',['yes', 'no'])
        
        start_loc = 0
        while show_data == 'yes':
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            show_data = get_user_input('Would you like to see 5 rows of raw data? Enter yes or no.',['yes', 'no'])
            if start_loc >= len(df):
                print('\nNo more data available.')
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        show_row_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
