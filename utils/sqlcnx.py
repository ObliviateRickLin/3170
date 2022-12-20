import mysql.connector
import pandas as pd

global cnx
cnx = mysql.connector.connect(
    host="123.60.157.95",
    port=3306,
    user="root",
    password="csc123456@",
    database="project")



# Fetch one result
def get_chip_type():
    cur = cnx.cursor()
    cur.execute("""
            SELECT *  
            FROM chip_type;
            """)
    chip_type = cur.fetchall()      
    return chip_type

if __name__ == '__main__':
    print(get_chip_type())

'''
# Get a cursor
cur = cnx.cursor()
# Execute a query
cur.execute("""
            SELECT *  
            FROM user;
            """)
print(pd.DataFrame(cur.fetchall()))
'''