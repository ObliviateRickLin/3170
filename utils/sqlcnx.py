import mysql.connector
import pandas as pd

def run_query(query):
    cnx = mysql.connector.connect(
        host="123.60.157.95",
        port=3306,
        user="root",
        password="csc123456@",
        database="project")
    cnx.reconnect()
    with cnx.cursor(buffered=True) as cur:
        cur.execute(query)
        result = cur.fetchall()
    cnx.close()
    return result
    
# Fetch one result
def get_chip_type():
    chip_type_sql = run_query("""
                                SELECT *  
                                FROM chip_type;
                                """)
    chip_type = pd.DataFrame(chip_type_sql)
    chip_type.columns = ["CHIP_NAME", "CHIP_VERSION", "PRICE"]
    chip_type["NUMBER"] = 0
    chip_type["COST"] = 0
   
    return chip_type


if __name__ == '__main__':
    print(get_chip_type())

