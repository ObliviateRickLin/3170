import os
import streamlit as st
import pandas as pd
from PIL import Image
import mysql.connector
import re

from utils.sqlcnx import *

path = os.path.dirname(__file__)

CIPY_PATH = "data/plant_pos.csv"

MACHINE_PATH = "source/data_generation/dataset/machine_type.csv"

PLANT_PATH = "source/data_generation/dataset/plants.csv"

CHIP_PATH = "source/data_generation/dataset/chip_type.csv"

PIN_COUNT = {
    "ST" : [20, 28, 32],
    "AD" : [20, 32, 36],
    "EP" : [32, 26, 48],
}

TEMP_RANGE = {
    "ST" : "-40~85°C",
    "AD" : "-40~85°C",
    "EP" : "-40~105°C",
}

@st.cache
def load_data():
    df = pd.read_csv(CIPY_PATH)
    return df

def select_chip(chip_info, c_name, c_ver):
    if c_name == None:
        chip_list = chip_info
    else:
        if c_ver == None:
            chip_list = chip_info.loc[chip_info['chip_name'] == c_name]
        else:
            chip_list = chip_info.loc[(chip_info['chip_name'] == c_name) & (chip_info['chip_version'] == c_ver)]
    return chip_list

def select_machine(machine_info, m_name, m_ver):
    if m_name == None:
        machine_list = machine_info
    else:
        if m_ver == None:
            machine_list = machine_info.loc[machine_info['machine_name'] == m_name]
        else:
            machine_list = machine_info.loc[(machine_info['machine_name'] == m_name) & (machine_info['machine_version'] == m_ver)]
    return machine_list


    
def preview_page():

    # st.set_page_config(page_title="Main Demo", page_icon="📈")
    # st.sidebar.header("Main Demo")
    
    chip_img = Image.open("images/chip_img.jpg")
    st.image(chip_img)
    
    st.title("Introduction")

    st.markdown(
        """
        ## ***Who is this platform for***?
        ***With the help of Smart contract, High speed internet and Cloud manufacturing systems, we provide a platform where chip consumers (with ability of basic circuit design) can send their request of chip
        manufacturing and even make real-time scheduling over the machines of those plants.***
                
        """
    )
    
    st.markdown("***")
    # Load 300 rows of data into the dataframe.
    data = load_data()
    
    plant_text_col, plant_img_col = st.columns((1,2))
    
    plant_text_col.header("***Our Plants***")
    plant_text_col.markdown("***Our plants are all over the country. We are able provide you with the most efficient solution!***")
    plant_img = Image.open("images/plant.jpg")
    plant_img_col.image(plant_img)
    
    # plant_info = pd.read_csv(PLANT_PATH)
    plant_info = pd.DataFrame(run_query('SELECT plant_name, province, street_address from plant;'), 
                              columns=['plant_name', 'province', 'street_address'],)
    plant_list = plant_info[['plant_name', 'province', 'street_address']]
    
    plant_expander = st.expander("plant informtion")
    with plant_expander:
        st.dataframe(plant_list, use_container_width=True)

    st.markdown(
        """
        ### ***Are ALL OVER the country***!!

        """
    )
    st.map(data)

    st.markdown("***")

    
    #########################################################################
    # The following are information about machines, including information about machine name, chip version, etc.
    
    machine_img_col, machine_text_col = st.columns((2,1))
    machine_img = Image.open("images/machine.jpeg")
    machine_img_col.image(machine_img)
    
    machine_text_col.header("***Our Machines***")
    machine_text_col.markdown("***Customize your chipset with all the machines we provide!***")

    # machine_info = pd.read_csv(MACHINE_PATH)
    machine_info = pd.DataFrame(run_query('SELECT machine_name, machine_version, price from machine_type;'), 
                                columns=['machine_name', 'machine_version', 'price'])
    
    # st.dataframe(machine_info, use_container_width=True)
    
    machine_name_box, select_m_name_checkbox, machine_version_box, select_m_ver_checkbox = st.columns((5,1,5,1))
    
    use_m_name_col = select_m_name_checkbox.checkbox(" ")
    use_m_ver_col = select_m_ver_checkbox.checkbox("  ")

    if use_m_name_col:
        if use_m_ver_col:
            selected_m_type = machine_name_box.selectbox(
            'machine name',
            machine_info['machine_name'].unique())
            
            selected_m_ver = machine_version_box.selectbox(
            'machine version',
            machine_info.loc[machine_info['machine_name'] == selected_m_type]['machine_version'])
            
        else:
            selected_m_type = machine_name_box.selectbox(
            'machine name',
            machine_info['machine_name'].unique())
            
            selected_m_ver = machine_version_box.selectbox(
            'machine version',
            [])
    else:
        selected_m_type = machine_name_box.selectbox(
        'machine name',
        [])
        selected_m_ver = machine_version_box.selectbox(
        'machine version',
        [])

    machine_list = select_machine(machine_info, selected_m_type, selected_m_ver)
    st.dataframe(machine_list, use_container_width=True)
    
    #########################################################################
    # The following are information about products, including information about chip name, chip version, etc.
    st.markdown("***")
    st.header("***Our Products***")
    # chip_info = pd.read_csv(CHIP_PATH)
    chip_info = pd.DataFrame(run_query('SELECT chip_name, chip_version, price from chip_type;'), 
                                columns=['chip_name', 'chip_version', 'price'])
    
    chip_names = chip_info['chip_name']
    chip_vers = chip_info['chip_version']
    # add pincount information
    leading_letters = [chip_name.lstrip()[:2] for chip_name in chip_names]
    pin_counts = [PIN_COUNT[leading_letters[i]][int(chip_vers[i])-1] for i in range(len(leading_letters))]
    chip_info['pin_count'] = pin_counts
    # add temperature information
    temperature_ranges = [TEMP_RANGE[leading_letter] for leading_letter in leading_letters]
    chip_info['temperature_range'] = temperature_ranges
    
    chip_name_box, select_c_name_checkbox, chip_version_box, select_c_ver_checkbox = st.columns((5,1,5,1))
    
    use_c_name_col = select_c_name_checkbox.checkbox("   ")
    use_c_ver_col = select_c_ver_checkbox.checkbox("    ")

    if use_c_name_col:
        if use_c_ver_col:
            selected_c_type = chip_name_box.selectbox(
            'chip name',
            chip_info['chip_name'].unique())
            
            selected_c_ver = chip_version_box.selectbox(
            'chip version',
            chip_info.loc[chip_info['chip_name'] == selected_c_type]['chip_version'])
            
        else:
            selected_c_type = chip_name_box.selectbox(
            'chip name',
            chip_info['chip_name'].unique())
            
            selected_c_ver = chip_version_box.selectbox(
            'chip version',
            [])
    else:
        selected_c_type = chip_name_box.selectbox(
        'chip name',
        [])
        selected_c_ver = chip_version_box.selectbox(
        'chip version',
        [])

    chip_list = select_chip(chip_info, selected_c_type, selected_c_ver)
    st.dataframe(chip_list, use_container_width=True)
    st.write("***")
    

    # st.write(chip_list)
if __name__ == "__main__":
    preview_page()