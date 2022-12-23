import streamlit as st

from utils.icons import *
from utils.sqlcnx import *

def shopping_cart_page():
    # product_name
    chip_type = get_chip_type()
    # title
    st.title('Chip Shopping Cart')
    st.write("___________________________________")
    for _, row in chip_type.iterrows():
        with st.container():
            c0, c1, c2, c3, c4 = st.columns((1,5,1.4,2,1.8))
            with c0: display_icon(cpu)
            with c1: st.subheader(row["CHIP_NAME"]);st.caption("Version: %s"%row["CHIP_VERSION"])
            with c2: st.subheader("%s$"%row["PRICE"])
            with c3: st.selectbox("Selectable Plants", options=("Plant A", "Plant B","Platn C"), key = ("plant",row["CHIP_NAME"],row["CHIP_VERSION"]))
            with c4: row["NUMBER"] = st.number_input(label = "Number", value=0, step=1, min_value=0, key = ("version",row["CHIP_NAME"],row["CHIP_VERSION"]))
            row["COST"] = row["NUMBER"] * row["PRICE"]
            st.write("___________________________________")
    total = chip_type["COST"].sum()
    st.subheader(total)
    with st.expander("Check your shopping cart information"):
        st.table(chip_type)
    #st.write(product_quantities)
    return 

if __name__ == "__main__":
    shopping_cart_page()