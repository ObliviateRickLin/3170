import streamlit as st

from utils.icons import *
from utils.sqlcnx import *

def shopping_cart_page():
    # product_name
    product_names = get_chip_type()

    # product_dict
    product_quantities = {name: 0 for name in product_names}

    # title
    st.title('Chip Shopping Cart')
    st.write("___________________________________")
    for name, version in product_names:
        with st.container():
            c0, c1, c2, c3, c4 = st.columns((1,5,1,2,1.9))
            with c0: display_icon(cpu)
            with c1: st.subheader(name);st.caption("Version: %s"%version)
            with c2: st.subheader("5$")
            with c3: st.selectbox("Selectable Plants", options=("Plant A", "Plant B","Platn C"), key = ("plant",name,version))
            with c4: quantity = st.number_input(label = "Number", value=0, step=1, min_value=0, key = ("version",name,version))
            product_quantities[name] = quantity
            st.write("___________________________________")

    #st.write(product_quantities)
    return 
