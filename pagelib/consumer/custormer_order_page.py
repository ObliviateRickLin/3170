import streamlit as st
import pandas as pd

import mysql.connector
import numpy as np

# user id for testing
USER_ID = 100

cnx = mysql.connector.connect(
host="123.60.157.95",
port=3306,
user="root",
password="csc123456@",
database="project")

CIPY_PATH = "web\data\plant_pos.csv"

@st.cache
def load_data():
    df = pd.read_csv(CIPY_PATH)
    return df

def run_query(query, cnx):
    with cnx.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

def custormer_order_page(user_id):
    
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
    
    # Current Orders
    st.markdown("***")
    st.markdown(
        """
        ## ***Current Orders***
        """
    )
    
    package_info = pd.DataFrame(run_query("SELECT * FROM package", cnx), columns=['user_id', 'package_id', 'budget', 'create_time', 'deadline'])
    current_user_order = package_info.loc[package_info['user_id'] == USER_ID]
    cur_order = current_user_order[['package_id', 'budget', 'create_time', 'deadline']]
    cur_package = cur_order[['package_id']]
    st.dataframe(cur_order, use_container_width=True)
    
    # Cancel Orders
    st.markdown(
        """
        ## ***Cancel Orders***
        """
    )
    
    package_selectbox, cancel_button = st.columns((5,1)) 
    
    selected_pacakge = package_selectbox.selectbox(
        'package id',
        cur_package
    )
    
    cancel = cancel_button.button('cancel')
    
    if (cancel):
        st.write('cancel package')
    
    
    # Current working Plants
    st.markdown(
        """
        ## ***Current Working Plants***
        """
    )
    
    data = load_data()
    plant_package_info = pd.DataFrame(run_query("SELECT * FROM plant_with_package", cnx), columns=['package_id', 'plant_id'])
    plant_info = pd.DataFrame(run_query('SELECT plant_id, plant_name, province, street_address from plant;', cnx), 
                              columns=['plant_id', 'plant_name', 'province', 'street_address'],)
        
    plant_list = plant_package_info.loc[plant_package_info['package_id'].isin(np.array(cur_package).squeeze())]['plant_id'].unique()
    
        
    # st.dataframe(plant_package_info)
    
    plant_expander = st.expander("plant informtion")
    with plant_expander:
        st.dataframe(plant_info.loc[plant_info['plant_id'].isin(plant_list)], use_container_width=True)
    
    plant_name = plant_info.loc[plant_info['plant_id'].isin(plant_list)]['plant_name']
    plant_name = np.array(plant_name).squeeze()
    plant_name = [x.lower() for x in plant_name]
    
    city_name = []
    for name in plant_name:
        if name.find('-') == -1:
            city_name.append(name)
        else:
            city_name.append(name[:name.find('-')])
        
    st.map(data.loc[data['city'].isin(city_name)])

    
#custormer_order_page(user_id=USER_ID)