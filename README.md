# SQLAlchemy-Challenge
## Table of Content
-climate_starter-fin.ipynb
-app.py 

## References of code sourced from
-Monash Lesson Plans - Advanced SQL
-Stack overflow 
  - https://stackoverflow.com/questions/22235245/calculate-summary-statistics-of-columns-in-dataframe
  - https://stackoverflow.com/questions/53460391/passing-a-date-as-a-url-parameter-to-a-flask-route
-AskBCs (Liang, Celine, Dinh) - polishing code
## code
# Convert the query parameters to datetime objects
    start_date_q = dt.datetime.strptime(start_date, '%Y-%m-%d')

## code
# Create a dictionary with the temperature summary
    summary_dict = {'start_date_q': start_date,
            'TMIN': result.TMIN,
            'TAVG': result.TAVG,
            'TMAX': result.TMAX,
            'end_date_q': end_date
        }
