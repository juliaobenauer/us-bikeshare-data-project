import time
import pandas as pd
import numpy as np
# use of calendar for full month and weekday names
import calendar as cal

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Let's first select a city! Which city are you interested "+
                     "in: Chicago, New York City or Washington?\n\n")
        # make entries case-insensitive and use small letters, as applied when assigning city names at lines 7-9
        city = city.lower()
        
        # invalid input handling for city
        if city not in ('new york city', 'chicago', 'washington'):
            print("Please enter a valid city.")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month would you like to analyze for " + city.title() + 
                      "? You can choose between January, February, March, " +
                      "April, May and June, or type all if you do not wish "+
                      "to specify a month.\n\n")
        # make entries case-insensitive and use small letters
        month = month.lower()
        
        # invalid input handling for month
        if month not in ('january', 'february', 'march', 'april', 'may', 
                         'june', 'all'):
            print("Please enter a valid month.")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Great choice. Now, let's pick a day." +
                    "You can choose between Monday, Tuesday, Wednesday," +
                    "Thursday, Friday, Saturday or Sunday, or type all if " +
                    "you do not wish to specify a day.\n\n")
        # make entries case-insensitive and use small letters
        day = day.lower()
        
        # invalid input handling for month
        if day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                       'saturday', 'sunday', 'all'):
            print("Please enter a valid day.")
            continue
        else:
            break

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
    # 1. read the dataframe of the selected city, using the pandas package
    df = pd.read_csv(CITY_DATA[city])
    
    # 2. convert Start Time to a datetime object, for subsequent extraction of
    # month and weekday (and later, hour)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # 3. extraction of month and day
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday
    
    # 4. filtering of dataset, based on selections
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['Month'] == month]
    
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day) 
        df = df[df['Weekday'] == day]
    
    return df


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month    
    # 1. list of full month names from calendar
    list(cal.month_name)
    
    # 2. determine most common month
    ind_month = df['Month'].value_counts().idxmax()
    
    # 3. print full name of most common month
    if month != 'all':
        print('You have selected ',month.title(),', so, unsurprisingly, the most common '+
              'month in',city.title(),'is', cal.month_name[ind_month], ';) \n\n')
    
    else:
        print('The most common month in ',city.title(),' is', 
              cal.month_name[ind_month], '.\n\n')
    

    # display the most common day of week    
    # 1. list of full weekday names from calendar    
    list(cal.day_name)
    
    # 2. determine most common weekday
    ind_day = df['Weekday'].value_counts().idxmax()
    
    # 3. print full name of most common weekday
    if day != 'all':
        print('You have selected',day.title(),'so, unsurprisingly, the most common '+
              'day of the week in',city.title(),'is', cal.day_name[ind_day], ';) \n\n')    
    else:
        print('The most common day of the week is', cal.day_name[ind_day], '\n\n')
    
        
    # display the most common start hour
    # 1. extract the hour part from Start Time and save in new variable
    df['Start Hour'] = df['Start Time'].dt.hour    
    
    # 2. print most common start hour
    print('The most common start hour for your selection is', 
          df['Start Hour'].value_counts().idxmax(), 'o\'clock.\n')
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common start station for your selection is', 
          df['Start Station'].value_counts().idxmax(), '.\n\n')

    # display most commonly used end station
    print('The most common end station for your selection is', 
          df['End Station'].value_counts().idxmax(), '.\n\n')

    # display most frequent combination of start station and end station trip
    # 1. combine start and end stations into new column 
    df['Station Combination'] = df['Start Station'] + ' (start) and ' + df['End Station'] + ' (end).'
    
    # 2. print station combination
    print('The most common station combination for your selection is ', 
          df['Station Combination'].value_counts().idxmax(), '\n')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # 1. calculate total travel time in seconds with .sum()
    trip_sum_sec = df['Trip Duration'].sum()
    
    # 2. convert total travel time to hours and round with zero decimal points
    trip_sum_h = round(trip_sum_sec / 60 / 60 ,0)
    
    # 3. print total travel time
    print('The total travel time for your selection is', trip_sum_h, 'hours.\n\n')

    # display mean travel time
    # 1. calculate mean travel time in seconds with .mean()
    trip_mean_sec = df['Trip Duration'].mean()
    
    # 2. convert total travel time to minutes and round with zero decimal points
    trip_mean_min = round(trip_mean_sec / 60  ,0)    
    
    # 3. display mean travel time either in minutes if below one hour, or in hours if above
    #    and print mean travel time
    if trip_mean_min < 60:
        print('The mean travel time for your selection is', trip_mean_min, 'minutes.\n\n')
    else:
        trip_mean_h = round(trip_mean_min / 60 ,1)
        print('The mean travel time for your selection is', trip_mean_h, 'hours.\n\n')
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users. Statistics will be calculated using NumPy."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # 1. convert user type to an NumPy array for subseqent counts
    usertypes = df['User Type'].values
    
    # 2. count the occurences of the different user types
    ct_subscriber  = (usertypes == 'Subscriber').sum()
    ct_customer = (usertypes == 'Customer').sum()
    
    # 3. print user type counts
    print('The number of subscribers in', city.title(), 'is:',ct_subscriber,'\n')
    print('The number of customers in', city.title(), 'is:',ct_customer,'\n')

    # Display counts of gender
    # Display earliest, most recent, and most common year of birth
    # gender and year of birth are missing from the Washington dataset
    if city.title() != 'Washington':
        # counts of gender
        # 1. convert gender to an NumPy array for subseqent counts
        gender = df['Gender'].values
        
        # 2. count the occurences of the different user types
        ct_male  = (gender == 'Male').sum()
        ct_female = (gender == 'Female').sum()
        
        # 3. print counts
        print('The number of male users in', city.title(), 'is:',ct_male,'\n')
        print('The number of female users in', city.title(), 'is:',ct_female,'\n')
        
        # year of birth
        # 1. convert gender to an NumPy array for subseqent statistics
        birthyear = df['Birth Year'].values
        
        # 2. get unique birth years and exclude NaNs
        birthyear_unique = np.unique(birthyear[~np.isnan(birthyear)])
        
        # 3. the latest birth year is the highest / maximum number
        latest_birthyear = birthyear_unique.max()
        
        # 4. the earliest birth year is the lowest / minimum number
        earliest_birthyear = birthyear_unique.min()
        
        # 5. print latest and earliest birth year
        print('The most recent birth year of users in', city.title(), 'is:',
              latest_birthyear ,'\n')
        print('The earliest birth year of users in', city.title(), 'is:',
              earliest_birthyear,'\n')   
        
        # 6. display most common birth year
        print('The most common birth year of users in', city.title(), 'is:', 
              df['Birth Year'].value_counts().idxmax(), '\n')
    
    else:
        # print message if Washington was chosen as city
        print('Sorry. Gender and birth year information are not available for Washington!')

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# new function for raw data display    
def raw_data(df):
    """ Displays 5 lines of raw data at a time when yes is selected."""
    # define index i, start at line 1
    i = 1
    while True:
        rawdata = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        if rawdata.lower() == 'yes':
            # print current 5 lines
            print(df[i:i+5])
            
            # increase index i by 5 to print next 5 lines in new execution
            i = i+5
            
        else:
            # break when no is selected
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        # arguments adapted to run function properly
        time_stats(df, city, month, day)
        station_stats(df)
        trip_duration_stats(df)
        # arguments adapted to run function properly
        user_stats(df, city)
        
        # additonal function to display raw data
        raw_data(df)
        
  
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

###############################################################################
######              Resources used 
#
# Udacity Introduction to Python programming course videos and notes
#
# Udacity project description and Rubric
#
# https://www.askpython.com/python/examples/python-user-input#:~:text=Python%20User%20Input%20from%20Keyboard%20%E2%80%93%20input%20%28%29,for%20the%20user%20input.%20...%20More%20items...%20
# 
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
# 
# https://stackoverflow.com/questions/51603690/extract-day-and-month-from-a-datetime-object
#
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.dt.month.html
#
# https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.weekday.html
#
# https://www.codespeedy.com/filter-rows-of-dataframe-in-python/?msclkid=bd629acbb45a11ecab45cfffe288aac0
#
# https://datascientyst.com/get-most-frequent-values-pandas-dataframe/#:~:text=To%20get%20the%20most%20frequent,value%20that%20appears%20most%20often.
#
# https://www.tutorialspoint.com/python/string_title.htm#:~:text=Python%20String%20title%20%28%29%20Method%201%20Description.%20Python,shows%20the%20usage%20of%20title%20%28%29%20method.%20?msclkid=2146553bb44d11ec8016e0c8f789849f
#
# https://stackoverflow.com/questions/36341484/get-day-name-from-weekday-int
#
# https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.hour.html
#
# https://stackoverflow.com/questions/19377969/combine-two-columns-of-text-in-pandas-dataframe
#
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.values.html
#
# https://stackoverflow.com/questions/28663856/how-to-count-the-occurrence-of-certain-item-in-an-ndarray
#
# https://stackoverflow.com/questions/28940412/how-to-find-the-unique-non-nan-values-in-a-numpy-array?msclkid=2a22e900b45411ec87fa194c60c6cefd
