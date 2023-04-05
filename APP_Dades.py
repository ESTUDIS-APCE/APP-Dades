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
from datetime import datetime
import plotly.graph_objs as go

user="/home/ruben/" 
# user="C:/Users/joana.APCE/"


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
        options=["Catalunya","Províncies i àmbits", "Municipis", "Districtes de Barcelona", "Contacte"],  # Dropdown menu
        icons=[None, "map", "house-fill", "house-fill", "envelope"],  # Icons for dropdown menu
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
        
    @st.cache_data
    def import_data():
        DT_terr = pd.read_excel('DT.xlsx', sheet_name= 'terr_q')
        # DT_terr = DT_terr.drop(['Trimestre'], axis=1)

        DT_mun = pd.read_excel('DT.xlsx', sheet_name= 'mun_q')
        # DT_mun = DT_mun.drop(['Trimestre'], axis=1)

        DT_dis = pd.read_excel('DT.xlsx', sheet_name= 'dis_q')
        # DT_dis = DT_dis.drop(['Trimestre'], axis=1)

        DT_terr_y = pd.read_excel('DT.xlsx', sheet_name= 'terr_y')
        DT_mun_y = pd.read_excel('DT.xlsx', sheet_name= 'mun_y')
        DT_dis_y = pd.read_excel('DT.xlsx', sheet_name= 'dis_y')
        
        return([DT_terr, DT_terr_y, DT_mun, DT_mun_y, DT_dis, DT_dis_y])

    DT_terr, DT_terr_y, DT_mun, DT_mun_y, DT_dis, DT_dis_y = import_data()

    def tidy_Catalunya(data_ori, columns_sel, fecha_ini, fecha_fin, columns_output):
        output_data = data_ori[["Trimestre"] + columns_sel][(data_ori["Fecha"]>=fecha_ini) & (data_ori["Fecha"]<=fecha_fin)]
        output_data.columns = ["Trimestre"] + columns_output
        return(output_data.set_index("Trimestre").drop("Data", axis=1))
    
    def filedownload(df, filename):
        towrite = io.BytesIO()
        df.to_excel(towrite, encoding='latin-1', index=True, header=True)
        towrite.seek(0)
        b64 = base64.b64encode(towrite.read()).decode("latin-1")
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Descarregar arxiu Excel</a>'
        return href

    if selected == "Catalunya":
        load_css_file(path + "main.css")
        margin_left, left_col, center_col, right_col, margin_right = st.columns((0.2, 1, 1, 1, 0.2))
        with right_col:
            with open(path + "APCE.png", "rb") as f:
                data_uri = base64.b64encode(f.read()).decode("utf-8")
            markdown = f"""
            #
            ![image](data:image/png;base64,{data_uri})
            """
            st.markdown(markdown, unsafe_allow_html=True)
        st.sidebar.header("Principals indicadors")
        index_names = ["Producció", "Compravendes", "Preus", "Superfície"]
        selected_index = st.sidebar.selectbox("", index_names)


        max_year=2022
        if selected_index=="Producció":
            min_year=2008
            st.header("PRODUCCIÓ D'HABITATGES A CATALUNYA")
            st.markdown("La producció d'habitatge a Catalunya al 2022")
            min_year, max_year = st.sidebar.slider("Selecciona el rang d'anys de la mostra", value=[min_year, max_year], min_value=min_year, max_value=max_year)
            table_Catalunya = tidy_Catalunya(DT_terr, ["Fecha", "iniviv_Catalunya", "finviv_Catalunya", "calprov_Cataluña", "caldef_Cataluña"], f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Habitatges Iniciats", "Habitatges acabats", "Qualificacions provisionals d'habitatge protegit", "Qualificacions definitives d'habitatge protegit"])
            selected_columns = st.multiselect("Selecciona el indicador: ", table_Catalunya.columns.tolist(), default=table_Catalunya.columns.tolist())
            left_margin, center_margin, right_margin = st.columns((0.5,10,0.5))
            with center_margin:
                st.dataframe(table_Catalunya[selected_columns])
                st.markdown(filedownload(table_Catalunya, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                plot_cat = table_Catalunya[selected_columns]
                traces = []
                for col in plot_cat.columns:
                    trace = go.Scatter(
                        x=plot_cat.index,
                        y=plot_cat[col],
                        mode='lines',
                        name=col
                    )
                    traces.append(trace)
                layout = go.Layout(
                    title="Oferta d'habitatges a Catalunya",
                    xaxis=dict(title="Trimestre"),
                    yaxis=dict(title="Indicador d'oferta en nivells")
                )
                fig = go.Figure(data=traces, layout=layout)
                st.plotly_chart(fig)
        if selected_index=="Compravendes":
            min_year=2014
            st.header("COMPRAVENDES D'HABITATGES A CATALUNYA")
            st.markdown("Les compravendes d'habitatge a Catalunya al 2022")
            min_year, max_year = st.sidebar.slider("Selecciona el rang d'anys de la mostra", value=[min_year, max_year], min_value=min_year, max_value=max_year)
            table_Catalunya = tidy_Catalunya(DT_terr, ["Fecha", "trvivt_Catalunya", "trvivs_Catalunya", "trvivn_Catalunya"], f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Compravendes d'habitatge total", "Compravendes d'habitatge de segona mà", "Compravendes d'habitatge nou"])
            selected_columns = st.multiselect("Selecciona el indicador: ", table_Catalunya.columns.tolist(), default=table_Catalunya.columns.tolist())
            left_margin, center_margin, right_margin = st.columns((0.5,10,0.5))
            with center_margin:
                st.dataframe(table_Catalunya[selected_columns])
                st.markdown(filedownload(table_Catalunya, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                plot_cat = table_Catalunya[selected_columns]
                traces = []
                for col in plot_cat.columns:
                    trace = go.Scatter(
                        x=plot_cat.index,
                        y=plot_cat[col],
                        mode='lines',
                        name=col
                    )
                    traces.append(trace)
                layout = go.Layout(
                    title="Compravendes d'habitatge per tipologia d'habitatge",
                    xaxis=dict(title="Trimestre"),
                    yaxis=dict(title="Indicador d'oferta en nivells")
                )
                fig = go.Figure(data=traces, layout=layout)
                st.plotly_chart(fig)
        if selected_index=="Preus":
            min_year=2014
            st.header("PREUS PER M2 ÚTIL A CATALUNYA")
            st.markdown("Els preus per m2 útil d'habitatge a Catalunya al 2022")
            min_year, max_year = st.sidebar.slider("Selecciona el rang d'anys de la mostra", value=[min_year, max_year], min_value=min_year, max_value=max_year)
            table_Catalunya = tidy_Catalunya(DT_terr, ["Fecha", "prvivt_Catalunya", "prvivs_Catalunya", "prvivn_Catalunya"], f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Preu d'habitatge total", "Preus d'habitatge de segona mà", "Preus d'habitatge nou"])
            selected_columns = st.multiselect("Selecciona el indicador: ", table_Catalunya.columns.tolist(), default=table_Catalunya.columns.tolist())
            left_margin, center_margin, right_margin = st.columns((0.5,10,0.5))
            with center_margin:
                st.dataframe(table_Catalunya[selected_columns])
                st.markdown(filedownload(table_Catalunya, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                plot_cat = table_Catalunya[selected_columns]
                traces = []
                for col in plot_cat.columns:
                    trace = go.Scatter(
                        x=plot_cat.index,
                        y=plot_cat[col],
                        mode='lines',
                        name=col
                    )
                    traces.append(trace)
                layout = go.Layout(
                    title="Preus per m2 per tipologia d'habitatge",
                    xaxis=dict(title="Trimestre"),
                    yaxis=dict(title="Indicador d'oferta en nivells")
                )
                fig = go.Figure(data=traces, layout=layout)
                st.plotly_chart(fig)
        if selected_index=="Superfície":
            min_year=2014
            st.header("SUPERFÍCIE EN M2 ÚTILS")
            st.markdown("La superfície en m2 útils dels habitatges a Catalunya al 2022")
            min_year, max_year = st.sidebar.slider("Selecciona el rang d'anys de la mostra", value=[min_year, max_year], min_value=min_year, max_value=max_year)
            table_Catalunya = tidy_Catalunya(DT_terr, ["Fecha", "supert_Catalunya", "supers_Catalunya", "supern_Catalunya"], f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Superfície mitjana total", "Superfície mitjana d'habitatge de segona mà", "Superfície mitjana d'habitatge nou"])
            selected_columns = st.multiselect("Selecciona el indicador: ", table_Catalunya.columns.tolist(), default=table_Catalunya.columns.tolist())
            left_margin, center_margin, right_margin = st.columns((0.5,10,0.5))
            with center_margin:
                st.dataframe(table_Catalunya[selected_columns])
                st.markdown(filedownload(table_Catalunya, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                plot_cat = table_Catalunya[selected_columns]
                traces = []
                for col in plot_cat.columns:
                    trace = go.Scatter(
                        x=plot_cat.index,
                        y=plot_cat[col],
                        mode='lines',
                        name=col
                    )
                    traces.append(trace)
                layout = go.Layout(
                    title="Superfície mitjana per tipologia d'habitatge",
                    xaxis=dict(title="Trimestre"),
                    yaxis=dict(title="Indicador d'oferta en nivells")
                )
                fig = go.Figure(data=traces, layout=layout)
                st.plotly_chart(fig)


    if selected == "Províncies i àmbits":
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
        index_names = ["Províncies", "Comarques", "Municipis", "Districtes de Barcelona"]
        selected_index = st.sidebar.selectbox("", index_names)
        if selected_index=="Producció":
            st.header("Producció")
            left_margin, left_col, center_margin, right_col, right_margin = st.columns((0.2, 1, 0.2, 1, 0.2))
            ["iniviv_Catalunya", "finviv_Catalunya", "calprov_Cataluña", "caldef_Cataluña"]

        if selected_index=="Compravendes":
            st.header("Compravendes")
            left_col, right_col = st.columns((1, 1))
            ["trvivt_", "trvivs_", "trvivn_"]
            ["Barcelona", "Girona", "Tarragona", "Lleida"]

        if selected_index=="Preus":
            st.header("Preus")
            left_col, right_col = st.columns((1, 1))
            ["prvivt_", "prvivs_", "prvivn_"]
            ["Barcelona", "Girona", "Tarragona", "Lleida"]

        if selected_index=="Superfície":
            st.header("Superfície")
            left_col, right_col = st.columns((1, 1))
            ["supert_", "supers_", "supern_"]
            ["Barcelona", "Girona", "Tarragona", "Lleida"]           
    
    if selected=="Municipis":
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
        index_names = ["Producció", "Compravendes", "Preus", "Superfície"]
        selected_index = st.sidebar.selectbox("", index_names)
        if selected_index=="Producció":
            left_col, right_col = st.columns((1, 1))
        if selected_index=="Compravendes":
            left_col, right_col = st.columns((1, 1))
        if selected_index=="Preus":
            left_col, right_col = st.columns((1, 1))
        if selected_index=="Superfície":
            left_col, right_col = st.columns((1, 1))
    if selected=="Districtes de Barcelona":
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
        index_names = ["Producció", "Compravendes", "Preus", "Superfície"]
        selected_index = st.sidebar.selectbox("", index_names)
        if selected_index=="Producció":
            left_col, right_col = st.columns((1, 1))
        if selected_index=="Compravendes":
            left_col, right_col = st.columns((1, 1))
        if selected_index=="Preus":
            left_col, right_col = st.columns((1, 1))
        if selected_index=="Superfície":
            left_col, right_col = st.columns((1, 1))

    if selected=="Contacte":
        load_css_file(path + "main.css")
        CONTACT_EMAIL = "estudis@apcecat.cat"
        st.write("")
        st.subheader(":mailbox: Contacteu-nos!")
        contact_form = f"""
        <form action="https://formsubmit.co/{CONTACT_EMAIL}" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" placeholder="Nom" required>
            <input type="email" name="email" placeholder="Correu electrónic" required>
            <textarea name="message" placeholder="La teva consulta aquí"></textarea>
            <button type="submit" class="button">Enviar ✉</button>
        </form>
        """
        st.markdown(contact_form, unsafe_allow_html=True)


