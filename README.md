mle.py contains two functions, days_of_precip and chance_of_precip, to determine:
1. The average number of days in a year that a given city had non-zero precipitation.
2. The likelihood of precipitaiton on a given day of the year in a given city.

Both functions rely on historical weather data from NOAA, provided in the csv.

Run either function from the commmand line -
1. days_of_precip: takes a city name (str) as an argument, either 'mia', 'bos', or 'jun' (for Miami, Boston, and Juneau, respectively).
2. chance_of_precip: takes a city name (str), a month (int), and a day (int) in that order as arguments.
