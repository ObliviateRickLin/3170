import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector


def plant_management_sys():
    user_id = st.session_state["ID"] 
    cnx1 = mysql.connector.connect(
        host="123.60.157.95",
        port=3306,
        user="root",
        password="csc123456@",
        database="project")

    cur1 = cnx1.cursor()
    cur1.execute("""
                SELECT plant_id, plant_name 
                FROM plant 
                WHERE  boss_id = %i; 
                """%user_id)
    try:
        plantID, plantName = cur1.fetchone()
    except:
        plantID, plantName = "1","Xi'an-1"
    cnx1.close()
    st.title("Welcome to Plant %s" %plantName)
    st.header("Please manage and confirm the existing chip orders.")
    tab1, tab2 = st.tabs(["Manage Chip Order", "Remaining Orders"])

    with tab1:
        st.header("Select the chip and let it be proccessed.")
        cnx2 = mysql.connector.connect(
            host="123.60.157.95",
            port=3306,
            user="root",
            password="csc123456@",
            database="project")
        cur2 = cnx2.cursor()
        cur2.execute("""
                    select c.chip_name, c.package_id
                    from chip as c natural join state as s
                    where c.plant_id = %s and s.state_name = 'Wait'
                    """%plantID)
        waiting_chip = cur2.fetchall()
        Select_Box = []
        packageID = []
        for i in waiting_chip:
            Select_Box.append(i[0])
            packageID.append(i[1])

        with st.form("my_form"):
            selected = st.multiselect(
                'Select the chip you want to manage:',
                Select_Box,
            )
            if st.form_submit_button('Submit'):
                chip = ""
                for i in packageID:
                    chip += str(i)
                    chip += ','
                chip = chip[:-1]

                cnx3 = mysql.connector.connect(
                    host="123.60.157.95",
                    port=3306,
                    user="root",
                    password="csc123456@",
                    database="project")
                cur3 = cnx3.cursor()
                cur3.execute("""
                            UPDATE state
                            SET state.state_name = 'Processing'
                            WHERE package_id in (%s)
                            """%chip)
                cnx3.commit()
                cnx3.close()
                st.text("Successful Management!\nPlease Reflash This Page")
        
    with tab2:
        st.header("Remaining Packages Needed to be Completed")
        cnx4 = mysql.connector.connect(
            host="123.60.157.95",
            port=3306,
            user="root",
            password="csc123456@",
            database="project")
        cur4 = cnx4.cursor()
        cur4.execute("""
                    SELECT c.chip_name, s.state_name
                    FROM chip AS c NATURAL JOIN state AS s
                    WHERE c.plant_id = %s and s.state_name = 'Processing'
                    """,(plantID,))
        df2 = pd.DataFrame(
            cur4.fetchall(),
            columns=["Chip Name", "State"])
        cnx4.close()
        st.table(df2)