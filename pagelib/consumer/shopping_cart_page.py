import streamlit as st

from datetime import datetime, timedelta
from utils.icons import *
from utils.sqlcnx import *
from utils.dfstyle import *
from utils.sltplt import select_plants_with_chip

def add_plant_info():
    result = run_query("SELECT PLANT_NAME, PLANT_ID FROM plant;")
    return dict(result)

def shopping_cart_page():
    # Calculate the minimum and maximum date range
    today = datetime.now()
    min_date = today + timedelta(days=10)
    max_date = today + timedelta(days=20)
    dft_date = today + timedelta(days=15)
    # product_name

    # title
    st.title('Chip Shopping Cart')
    st.write("___________________________________")
    if "chip" not in st.session_state:
        with st.spinner('Wait for it. We are checking avaliable plants'):
            st.session_state["chip"] = select_plants_with_chip()
    if "plant_info" not in st.session_state:
        st.session_state["plant_info"] = add_plant_info()
    if "package" not in st.session_state:
        st.session_state["package"] = 0
    chip_type = get_chip_type()
    chip_type = chip_type.merge(st.session_state["chip"], on=["CHIP_NAME","CHIP_VERSION"])
    with st.form("shopping cart"):
        for index, row in chip_type.iterrows():
            with st.container():
                c0, c1, c2, c3, c4 = st.columns((1,5,1.4,2,1.8))
                with c0: display_icon(cpu)
                with c1: st.subheader(row["CHIP_NAME"]);st.caption("Version: %s"%row["CHIP_VERSION"])
                with c2: st.subheader("%s$"%row["PRICE"])
                with c3: chip_type.loc[index,"PLANTS"] = st.selectbox("Selected_plants", options=(row["PLANTS"]), key = ("plant",row["CHIP_NAME"],row["CHIP_VERSION"]))
                chip_type.loc[index,"NUMBER"] = c4.number_input(label = "Number", value=0, step=1, min_value=0, key = ("version",row["CHIP_NAME"],row["CHIP_VERSION"]))
                chip_type["COST"] = chip_type["NUMBER"] * chip_type["PRICE"]
                st.write("___________________________________")
        submitted = st.form_submit_button("Check your package")
        if submitted:
            total = chip_type["COST"].sum() 
            c1, c2 = st.columns((1,2))
            with c1: 
                st.metric(label="TOTAL COST", value = total) 
            with c2: 
                ddl = st.date_input("Choose a DDL of your package", 
                        value = dft_date,
                        min_value = min_date, 
                        max_value = max_date, 
                        help="DDL should be about 10 to 20 days after today.")
            with st.expander("Check your shopping cart information"):
                st.dataframe(chip_type.style.applymap(color_zero))
            ddl = datetime.combine(ddl, datetime.now().time())
            st.session_state["package"] = (st.session_state["ID"], str(total), today.strftime("%Y-%m-%d %H:%M:%S"), ddl.strftime("%Y-%m-%d %H:%M:%S"))
    
    if st.button("SUBMIT YOUR PACKAGE"):
        try:
            package_info = st.session_state["package"]
            plant_info = st.session_state["plant_info"]
            cnx = mysql.connector.connect(
                    host="123.60.157.95",
                    port=3306,
                    user="root",
                    password="csc123456@",
                    database="project") 
            cur = cnx.cursor()
            query1 = """INSERT INTO package (USER_ID,  BUDGET, CREATE_TIME, DEADLINE) VALUES (%s, %s, %s, %s)"""
            cur.execute(query1, package_info)
            cnx.commit()
            cur2 = cnx.cursor()
            cur2.execute("SELECT LAST_INSERT_ID()")
            package_id, = cur2.fetchone()
            cnx.close()
            package_info = st.session_state["package"]
            plant_info = st.session_state["plant_info"]
            cnx = mysql.connector.connect(
                    host="123.60.157.95",
                    port=3306,
                    user="root",
                    password="csc123456@",
                    database="project") 
            cur = cnx.cursor()
            query = """INSERT INTO state (PACKAGE_ID, START_TIME, END_TIME, STATE_NAME) VALUES (%s, %s, %s, %s)"""
            cur.execute(query, (package_id, package_info[2], package_info[3], "Waiting"))
            cnx.commit()
            cnx.close()
            cnx = mysql.connector.connect(
                    host="123.60.157.95",
                    port=3306,
                    user="root",
                    password="csc123456@",
                    database="project") 
            cur = cnx.cursor()
            query3 = """INSERT INTO chip (CHIP_NAME, CHIP_VERSION, PRICE, PACKAGE_ID, PLANT_ID) VALUES (%s, %s,%s, %s, %s)"""
            chip_in_package = []
            for index, row in chip_type.iterrows():
                num = row["NUMBER"]
                for _ in range(num):
                    chip_in_package.append((row["CHIP_NAME"],row["CHIP_VERSION"],row["PRICE"],package_id, plant_info[row["PLANTS"]]))
            cur.executemany(query3, chip_in_package)
            cnx.commit()
            cnx.close()
            st.success("Subbmit successfully")
        except:
            st.warning("Please check your package first before submitting!")

    #st.write(product_quantities)
    return 

if __name__ == "__main__":
    shopping_cart_page()