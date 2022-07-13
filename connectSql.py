import cx_Oracle
import pandas as pd
import datetime

# Assigning the inclusive start and end dates of the required calendar to 2 variables
date1 = datetime.datetime(1999, 1, 1, 0, 0, 0)
date2 = datetime.datetime(2025, 12, 31, 0, 0, 0)

# Creating a .csv file in the current project directory and enabling the 'write(w)' permission
f = open("calendar1.csv", "w")

# Create a list and assign the starting date in the right format as the first value
dataList = [datetime.datetime(1999, 1, 1, 0, 0, 0), ]

# Using loops to add the rest of the dates to the list
while True:
    if date1 < date2:

        date1 += datetime.timedelta(days=1)

        dataList.append(date1)

    else:
        break

calendars = {"CALENDAR_DATE": dataList}

# Calling DataFrame constructor on list
df = pd.DataFrame(calendars)

# Populating the rest of the Dataframe
df['YEAR'] = df['CALENDAR_DATE'].dt.year
df['MONTH_OF_THE_YEAR'] = df['CALENDAR_DATE'].dt.month
df['DAY_OF_THE_MONTH'] = df['CALENDAR_DATE'].dt.day
df['WEEK_OF_THE_YEAR'] = df['CALENDAR_DATE'].dt.isocalendar().week
df['YEAR_QUARTER'] = df['CALENDAR_DATE'].dt.quarter

f.write(df.to_csv())

f.close()

dataDf = pd.read_csv("calendar1.csv")

# Connecting to the Oracle Database
conStr = 'classicmodels/classicmodels@54.190.118.110:1521/xe'

conn = cx_Oracle.connect(conStr)
cur = conn.cursor()

# Converting the read .csv file into list of tuples to help segregate records
dataInTuple = [tuple(x) for x in dataDf.values]

# SQL statement to be executed
query = 'INSERT INTO CLASSICMODELS.CALENDAR_2 (INDEX_VAL, CALENDAR_DATE, YEAR, MONTH_OF_THE_YEAR, DAY_OF_THE_MONTH, ' \
        'WEEK_OF_THE_YEAR, YEAR_QUARTER) VALUES ( :1, :2, :3, :4, :5, :6, :7) '

# Execution of query
cur.executemany(query, [x for x in dataInTuple])

conn.commit()
cur.close()
conn.close()
