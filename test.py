import mysql.connector 
import datetime

now  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
package_info = (1000,3000,now, now)
cnx = mysql.connector.connect(
        host="123.60.157.95",
        port=3306,
        user="root",
        password="csc123456@",
        database="project") 
cur = cnx.cursor()
query1 = """INSERT INTO package (USER_ID, BUDGET, CREATE_TIME, DEADLINE) VALUES (%s, %s, %s, %s)"""
cur.execute(query1, package_info)
cnx.commit()
cnx.close()