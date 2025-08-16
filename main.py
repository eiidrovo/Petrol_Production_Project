import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image

icon= Image.open('Resources/Logo.png')
st.set_page_config(page_title="Proyecto", page_icon="<UNK>")
FIMCM_Logo = Image.open('Resources/FIMCM_logo.png')
FICT_Logo = Image.open('Resources/FICT_logo.png')


# Menú lateral
with st.sidebar:
    seleccion = option_menu(
        "Menú principal",
        ["Home","Production Plots", "IPR curves", "Nodal Analysis"],
        icons=["house", "bar-chart-line-fill", "graph-up-arrow","option"],
        menu_icon="list",
        default_index=0
    )
st.write(seleccion)


file = st.file_uploader("Upload data to plot", type=["xlsx"])