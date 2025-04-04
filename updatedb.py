import pyodbc
import pandas as pd


# 1 Transform Raw to CSV


conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=darkesthj;'  # server name
    'DATABASE=main_db;' # database name
    'Trusted_Connection=yes;'
)

cursor = conn.cursor()

# 2 Delete all data from data_raw table
cursor.execute("DELETE FROM data_raw")
print('Data from data_raw has been deleted.')






# End Connection
conn.commit()
cursor.close()
conn.close()