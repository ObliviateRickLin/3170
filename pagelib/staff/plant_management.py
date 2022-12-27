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
                    where c.plant_id = %s and s.state_name = 'Waiting'  
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
                for i in selected:
                    index = Select_Box.index(i)
                    pid = packageID[index]
                    chip += str(pid)
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
                for i in selected:
                cnx6 = ms.connect(
                    host="123.60.157.95",
                    port=3306,
                    user="root",
                    password="csc123456@",
                    database="project")
                cur6 = cnx6.cursor()
                cur6.execute("""select chip_id
                                from chip
                                where chip_name = %s
                """%i)
                chip_id = cur6.fetchone()
                allocate_task(chip_id)
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

def run_query(query, *args):
    cnx = mysql.connector.connect(
        host="123.60.157.95",
        port=3306,
        user="root",
        password="csc123456@",
        database="project")
    cnx.reconnect()
    with cnx.cursor(buffered=True) as cur:
        cur.execute(query,*args)
        result = cur.fetchall()
    cnx.close()
    return result


def generate_operation(machine_id, operation_name, chip_id):
    cnx = mysql.connector.connect(
        host="123.60.157.95",
        port=3306,
        user="root",
        password="csc123456@",
        database="project")

    # Write an operation
    start_time = str(datetime.datetime.now())
    cur = cnx.cursor()
    cur.execute("INSERT INTO operation(operation_name, start_time, end_time) VALUES (%s, %s, NULL);", (operation_name, start_time))
    cnx.commit()

    # Derive the operation id
    cur2 = cnx.cursor()
    cur2.execute("SELECT LAST_INSERT_ID();")
    operation_id = cur2.fetchone()[0]


    """
    # Write a relation between chip and operation
    cur3 = cnx.cursor()
    cur3.execute("INSERT INTO operation_with_chip(operation_id, chip_id) VALUES (%s, %s);", (operation_id, chip_id))
    cnx.commit()
    """

    # Write a relation between machine and operation
    cur4 = cnx.cursor()
    cur4.execute("INSERT INTO operation_with_machine(operation_id, machine_id) VALUES (%s, %s);", (operation_id, machine_id))
    cnx.commit()

    cnx.close()


def allocate_task(chip_id):

    cnx = mysql.connector.connect(
        host="123.60.157.95",
        port=3306,
        user="root",
        password="csc123456@",
        database="project")
    # Find chip_name and chip_version
    chip_info = run_query("SELECT chip_name, chip_version FROM chip WHERE chip_id = %s;", (chip_id))
    chip_name, chip_version = chip_info[0][0], chip_info[0][1]


    # Find all operation type needed
    first_order_operation_name = run_query("SELECT operation_name FROM chip_type_with_operation_type WHERE chip_name = %s AND chip_version = %s AND order_op = 0;", (chip_name, chip_version))[0][0]


    # Find all machines in the plant of the chip
    plant_id = run_query("SELECT plant_id FROM chip WHERE chip_id = %s;", (chip_id))[0]
    machines = run_query("SELECT machine_id, machine_name, machine_version FROM machine WHERE plant_id = %s;", (plant_id))

    # Find suitable machines which could process the corresponding operation type
    for machine in machines:
        operation_names = run_query("SELECT operation_name FROM machine_type_with_operation_type WHERE machine_name = %s AND machine_version = %s;", (machine[1], machine[2]))
        operation_names = [i[0] for i in operation_names]
        if first_order_operation_name in operation_names:
            # Need to do: if machine is free, then allocate to the machine
            generate_operation(machine[0], first_order_operation_name, chip_id[0])
            # Need to do: set the state of machine as `busy`
            break
