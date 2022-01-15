import time
import pandas as pd
import numpy as np
import sys
import pprint

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
weeks = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']

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
    city = input('Please write city name: ').lower()
    while True:
        if city == '-1':
            break
        if city not in CITY_DATA:
            print('City not exist, plesase write one of list cities: ', list(CITY_DATA.keys()), 'or -1 to exit.')
            city = input('Please write city name: ').lower()
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    if city != '-1':
        month = input('Please write month name or all: ').lower()
        while True:
            if month == '-1':
                break
            if month not in months and month != 'all':
                print('Month is not exist, plesase write month as following: ', months, 'or -1 to exit.')
                month = input('Please write month name or all: ').lower()
            else:
                break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    if city != '-1' and month != '-1':
        day = input('Please write day of week name or all: ').lower()
        while True:
            if day == '-1':
                break
            if day not in weeks and day != 'all':
                print('day of week id not exist, plesase write day of week as following: ', weeks, 'or -1 to exit.')
                day = input('Please write month name or all: ').lower()
            else:
                break
    
    if city == '-1' or month == '-1' or day == '-1':
        print('Exit by user using -1')
        sys.exit(0)
        
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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print("The most common month is: {}".format( months[df['month'].value_counts().idxmax()-1].title() ))

    # TO DO: display the most common day of week
    print("The most common day of week is: {}".format( df['day_of_week'].value_counts().idxmax() ))

    # TO DO: display the most common start hour
    print("The most common start hour is: {} hrs".format( df['Start Time'].dt.hour.value_counts().idxmax() ))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most commonly used start station is: {}".format( df['Start Station'].value_counts().idxmax() ))


    # TO DO: display most commonly used end station
    print("The most commonly used end station is: {}".format( df['End Station'].value_counts().idxmax() ))

    # TO DO: display most frequent combination of start station and end station trip
    print("The most frequent combination of start station and end station trip is: {}".format( (df['Start Station'] + " - " + df['End Station']).value_counts().idxmax() ))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("The total travel time is: {} minutes ".format( df['Trip Duration'].sum() ))

    # TO DO: display mean travel time
    print("The mean travel time is: {} minutes ".format( df['Trip Duration'].mean().round(2) ))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    try:
        print("The counts of user types are : \n{}\n".format( df['User Type'].value_counts().to_string() ))
    except Exception as e:
        print("No {} field avaliable".format( e ))
    

    # TO DO: Display counts of gender
    try:
        print("The counts of gender are : \n{}\n".format( df['Gender'].value_counts().to_string() ))
    except Exception as e:
        print("No {} field avaliable".format( e ))

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        m_year = df['Birth Year'].value_counts().sort_index(ascending=False).sort_values(ascending=False).idxmax()
        print("The earliest, most recent, and most common year of birt is: {}".format( int(m_year) ))
    except Exception as e:
        print("No {} field avaliable".format( e ))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_data(df):
    i = 0
    while True:
        subdata = (df.iloc[ i*5 : (i+1) * 5]).to_dict('index')
        pprint.pprint(subdata)
        see_data = input('Would you like to view indedval trip data? yes or no\n')
        if see_data.lower() != 'yes':
            break
        i+=1

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_data(df)
		
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

# to startup the program
if __name__ == "__main__":
	main()
