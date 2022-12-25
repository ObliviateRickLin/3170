import streamlit as st
import numpy as np

def move_to_consumer_state():
    st.session_state["function"] = "consumer"

def move_to_staff_state():
    st.session_state["function"] = "staff"

def move_to_log_state():
    st.session_state["function"] = "log"
