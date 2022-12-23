import mysql.connector
import pandas as pd

# Fetch one result
def get_chip_type():
    cnx = mysql.connector.connect(
        host="123.60.157.95",
        port=3306,
        user="root",
        password="csc123456@",
        database="project")
    cur = cnx.cursor()
    cur.execute("""
            SELECT *  
            FROM chip_type;
            """)
    chip_type = pd.DataFrame(cur.fetchall())
    chip_type.columns = ["CHIP NAME", "CHIP VERSION"]
    chip_type["PRICE"] = 0
    chip_type["NUMBER"] = 0
    chip_type["COST"] = 0
    cnx.close()     
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