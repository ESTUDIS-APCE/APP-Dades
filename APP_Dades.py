import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import base64
from streamlit_option_menu import option_menu
import io
import geopandas as gpd
from mpl_toolkits.axes_grid1 import make_axes_locatable
import plotly.graph_objects as go
import matplotlib.colors as colors
# import streamlit.components.v1 as components
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


# user="/home/ruben/" 
user="C:/Users/joana.APCE/"

path = user + "Dropbox/Dades/APP Dades/"
# path = ""

st.set_page_config(
    page_title="APCE",
    page_icon=":house:",
    layout="wide"
)

with open(path + 'config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Inicia Sessió', 'main')


if authentication_status is False:
    st.error('Usuari o contrasenya incorrecte')
    try:
        if authenticator.reset_password(username, 'Reset password'):
            st.success('Password modified successfully')
    except Exception as e:
        st.error(e)
elif authentication_status is None:
    st.warning("Siusplau entri el nom d'usuari i contrasenya")
elif authentication_status:
    authenticator.logout('Tanca Sessió', 'main')
    st.write(f'Benvingut **{name}**')


    # Creating a dropdown menu with options and icons, and customizing the appearance of the menu using CSS styles.
    selected = option_menu(
        menu_title=None,  # required
        options=["Producció","Compravendes"],  # Dropdown menu
        icons=[None,"map", "house-fill","envelope"],  # Icons for dropdown menu
        menu_icon="cast",  # optional
        default_index=0,  # optional
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {
                "font-size": "25px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee",
                },
            "nav-link-selected": {"background-color": "#4BACC6"},
            })

    def load_css_file(css_file_path):
        with open(css_file_path) as f:
            return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        


dades_DT = pd.read_excel(path + "DT.xlsx")
st.write(dades_DT)

if selected == "Producció":
    load_css_file(path + "main.css")
    left_col, center_col, right_col = st.columns((1, 1, 1))
    with right_col:
        with open(path + "APCE.png", "rb") as f:
            data_uri = base64.b64encode(f.read()).decode("utf-8")
        markdown = f"""
        #
        ![image](data:image/png;base64,{data_uri})
        """
        st.markdown(markdown, unsafe_allow_html=True)
    st.sidebar.header("Índex de continguts")
    index_names = ["Introducció","Característiques", "Qualitats i equipaments", "Superfície i preus", "Comparativa 2022-2021"]
    selected_index = st.sidebar.selectbox("", index_names)
    st.write("""<h1 style="text-align:center">ESTUDI D'OFERTA DE NOVA CONSTRUCCIÓ 2022</h1>""", unsafe_allow_html=True)
    if selected_index=="Introducció":
        left_col, right_col = st.columns((1, 1))