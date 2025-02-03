import argparse
import pandas as pd
import numpy as np
import math

def read_data():
    """Weather data from NOAA"""

    df = pd.read_csv("noaa_historical_weather_10yr.csv", usecols=['NAME','DATE','PRCP','SNOW','TMAX','TMIN'])
    
    mapping={'MIAMI INTERNATIONAL AIRPORT, FL US': 'mia',
            'JUNEAU AIRPORT, AK US': 'jnu', 
            'BOSTON, MA US': 'bos'}

    df.NAME = df.NAME.replace(mapping)

    df['RAIN_TF'] = df["PRCP"].apply(lambda x: 1 if x > 0.0 else 0)
    df['SNOW_TF'] = df["SNOW"].apply(lambda x: 1 if x > 0.0 else 0)
    df['PRCP_TF'] = df["RAIN_TF"] + df["SNOW_TF"]
    df['PRCP_TF'] = df['PRCP_TF'].apply(lambda x: min(x, 1)) # so no 2s
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['DAY'] = df['DATE'].dt.day
    df['MONTH'] = df['DATE'].dt.month
    df['YEAR'] = df['DATE'].dt.year

    return df


def days_of_precip(city):
    """
    Find the average days of precipitation for a given city.

    Parameters:
    city (str): City name (e.g., 'bos', 'jnu', 'mia')

    Returns:
    float: Average number of days
    """
    print(f"Getting average days of precip for {city} in millimeters")
    df = read_data()

    df_city = df[df['NAME'] == city]
    days_precip = float(df_city.groupby(['YEAR'])['PRCP_TF'].sum().mean())
    print(days_precip)


def chance_of_precip(city, month, day):
    """
    Estimate the probability of precipitation for a given city and date.

    Logic:
    Simple framing as the likelihood of precip given past observations of precip on a given day.
    I used only the presence or absense of precip (discrete) to define the likelihood function, 
    but in reality, a joint distribution of continuous precip and temp values may provide better results.

    Parameters:
    city (str): City name (e.g., 'bos', 'jnu', 'mia')
    month (int): Month of the year (1-12)
    day (int): Day of the month (1-31)

    Returns:
    float: Precipitation likelihood (0 to 1)
    """
    print(f"Getting precipitation likelihood in {city} for month: {month}, day: {day}")
    df = read_data()

    df_a_day = df[(df.NAME == city) & (df.MONTH == month) & (df.DAY == day)]

    n_obs = len(df_a_day)
    if n_obs == 0:  
        return np.nan
    
    n_rain_obs = df_a_day['PRCP_TF'].sum()
    
    # Binominal coefficient is because order (Rain, Dry, Dry) doesn't matter for the likelihood func.
    binomial_coeff = math.factorial(n_obs) / (math.factorial(n_rain_obs) * math.factorial(n_obs-n_rain_obs))

    p_vec = np.linspace(0.01, 1, 100)
    f_p = binomial_coeff * (p_vec ** n_rain_obs) * ((1 - p_vec) ** (n_obs - n_rain_obs))

    p_rain = p_vec[np.argmax(f_p)]

    print(float(p_rain))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run precip functions")
    parser.add_argument("function", type=str, help="Choose to run functions: days_of_precip, chance_of_precip")
    parser.add_argument("args", nargs="*", help="Arguments required by the function")

    args = parser.parse_args()

    # Mapping function names to actual functions
    function_map = {
        "days_of_precip": days_of_precip,
        "chance_of_precip": chance_of_precip,
    }

    # Validate function input and call the function dynamically
    if args.function in function_map:
        try:
            if args.function == "days_of_precip":
                city = args.args[0]
                function_map[args.function](city)
            elif args.function == "chance_of_precip":
                city = args.args[0] 
                month = int(args.args[1]) 
                day = int(args.args[2]) 
                function_map[args.function](city, month, day)
        except TypeError as e:
            print(f"Error: {e}\nCheck the expected arguments for {args.function}.")
    else:
        print(f"Unknown function: {args.function}")
