import streamlit as st
import pandas as pd

import mysql.connector
import numpy as np

from utils.sqlcnx import *
# user id for testing
CIPY_PATH = "data/plant_pos.csv"

@st.cache
def load_data():
    df = pd.read_csv(CIPY_PATH)
    return df

def delete_package(package_id):
    st.write("delete package {}".format(package_id))
    
def cancel_order(query):
    cnx = mysql.connector.connect(
        host="123.60.157.95",
        port=3306,
        user="root",
        password="csc123456@",
        database="project")
    cnx.reconnect()
    with cnx.cursor(buffered=True) as cur:
        cur.execute(query)
    cnx.commit()
    cnx.close()

def custormer_order_page():
    user_id = st.session_state["ID"] 

    ## CSS
    m = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: rgb(61, 43, 113);
        position: absolute;
        top : 35px;
        
    }
    </style>""", unsafe_allow_html=True)
    
    
    
    st.title("Current Order")
    
    name = run_query("SELECT FIRST_NAME, LAST_NAME FROM user WHERE USER_ID = {}".format(user_id))
    first_name, last_name = name[0][0], name[0][1]
    # Current Orders
    st.markdown("***")
    st.markdown(
        """
        ## ***Current Orders***
        Hi, ***{} {}***. Here are your current orders.
        """.format(first_name, last_name)
    )
    
    package_info = pd.DataFrame(run_query("SELECT * FROM package"), columns=['user_id', 'package_id', 'budget', 'create_time', 'deadline'])
    package_state = pd.DataFrame(run_query("SELECT package_id, state_name from state;"), columns=['package_id', 'state_name'])
    package_info = pd.merge(package_info, package_state, on="package_id", how="left")
    # st.dataframe(package_info)
    current_user_order = package_info.loc[package_info['user_id'] == user_id]
    cur_order = current_user_order[['package_id', 'budget', 'create_time', 'deadline', "state_name"]]
    cur_package = cur_order[['package_id']]
    st.dataframe(cur_order, use_container_width=True)
    
    # Cancel Orders
    st.markdown(
        """
        ## ***Cancel Orders in Waiting Stage***
        
        """
    )
    cur_waiting_package = current_user_order[current_user_order['state_name'].isin(['Waiting'])]['package_id']
    
    package_selectbox, cancel_button = st.columns((5,1)) 
    
    selected_pacakge = package_selectbox.selectbox(
        'package id',
        cur_waiting_package
    )
    
    cancel = cancel_button.button('cancel')
    
    if (cancel):
        cancel_order("UPDATE state SET state_name='Cancelled' where package_id = {}".format(selected_pacakge))
    
    
    # Current working Plants
    st.markdown(
        """
        ## ***Current Working Plants***
        The following are plants that currently working for you.
        """
    )
    
    data = load_data()
    plant_package_info = pd.DataFrame(run_query("SELECT * FROM plant_with_package"), columns=['package_id', 'plant_id'])
    plant_info = pd.DataFrame(run_query('SELECT plant_id, plant_name, province, street_address, phone_number from plant;'), 
                              columns=['plant_id', 'plant_name', 'province', 'street_address', 'phone_number'],)
    
    if cur_package.empty:
        plant_list = []
    else :
        plant_list = plant_package_info.loc[plant_package_info['package_id'].isin(cur_package.values[0].tolist())]['plant_id'].unique()
        
    # st.dataframe(plant_package_info)
    
    plant_expander = st.expander("plant informtion")
    with plant_expander:
        st.dataframe(plant_info.loc[plant_info['plant_id'].isin(plant_list)], use_container_width=True)
    
    plant_name = plant_info.loc[plant_info['plant_id'].isin(plant_list)]['plant_name']
    print(plant_name)
    plant_name = np.array(plant_name)
    if len(plant_name.shape) != 1:
        plant_name = plant_name.squeeze()
    plant_name = [x.lower() for x in plant_name]
    
    city_name = []
    for name in plant_name:
        if name.find('-') == -1:
            city_name.append(name)
        else:
            city_name.append(name[:name.find('-')])
        
    st.map(data.loc[data['city'].isin(city_name)])

    
#custormer_order_page(user_id=USER_ID)