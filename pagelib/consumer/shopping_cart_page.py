import streamlit as st

from utils.icons import *
from utils.sqlcnx import *
from utils.dfstyle import *

def shopping_cart_page():
    # product_name
    chip_type = get_chip_type()
    # title
    st.title('Chip Shopping Cart')
    st.write("___________________________________")
    for index, row in chip_type.iterrows():
        with st.container():
            c0, c1, c2, c3, c4 = st.columns((1,5,1.4,2,1.8))
            with c0: display_icon(cpu)
            with c1: st.subheader(row["CHIP_NAME"]);st.caption("Version: %s"%row["CHIP_VERSION"])
            with c2: st.subheader("%s$"%row["PRICE"])
            with c3: st.selectbox("Selectable Plants", options=("Plant A", "Plant B","Platn C"), key = ("plant",row["CHIP_NAME"],row["CHIP_VERSION"]))
            chip_type.loc[index,"NUMBER"] = c4.number_input(label = "Number", value=0, step=1, min_value=0, key = ("version",row["CHIP_NAME"],row["CHIP_VERSION"]))
            chip_type["COST"] = chip_type["NUMBER"] * chip_type["PRICE"]
            st.write("___________________________________")
    total = chip_type["COST"].sum()
    c1, c2 = st.columns((1,2))
    with c1: st.metric(label="TOTAL COST", value = total) 
    with c2: st.date_input("Choose a DDL of your package")
    with st.expander("Check your shopping cart information"):
        st.dataframe(chip_type.style.applymap(color_zero))
    #st.write(product_quantities)
    return 

if __name__ == "__main__":
    shopping_cart_page()