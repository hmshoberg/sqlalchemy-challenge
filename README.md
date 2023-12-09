# sqlalchemy-challenge
 
# Part 1: Analyze and Explore the Climate Data

In this section, you’ll use Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database. Specifically, you’ll use SQLAlchemy ORM queries, Pandas, and Matplotlib.

Precipitation Analysis

Find the most recent date in the dataset.

Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.

Select only the "date" and "prcp" values.

Load the query results into a Pandas DataFrame. Explicitly set the column names.

Sort the DataFrame values by "date".

Plot the results by using the DataFrame plot method

Use Pandas to print the summary statistics for the precipitation data.

Station Analysis

Design a query to calculate the total number of stations in the dataset.

Design a query to find the most-active stations (that is, the stations that have the most rows). To do so, complete the following steps:

List the stations and observation counts in descending order.

Answer the following question: which station id has the greatest number of observations?
Design a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.

# Part 2: Design Your Climate App

Now that you’ve completed your initial analysis, you’ll design a Flask API based on the queries that you just developed. To do so, use Flask to create your routes as follows:

# Sources
To find date one year from last date : 
chatgpt, 
https://github.com/ermiasgelaye/sqlalchemy-challenge/blob/master/climate.ipynb
