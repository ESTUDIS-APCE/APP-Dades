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


# path = user + "Dropbox/Dades/APP Dades/"
path = ""

st.set_page_config(
    page_title="CONJUNTURA DE SECTOR",
    page_icon="""data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAA1VBMVEVHcEylpKR6eHaBgH9GREGenJxRT06op6evra2Qj49kYWCbmpqdnJyWlJS+vb1CPzyurKyHhYWMiYl7eXgOCgiPjY10cnJZV1WEgoKCgYB9fXt
    /fHyzsrGUk5OTkZGlo6ONioqko6OLioq7urqysbGdnJuurazCwcHLysp+fHx9fHuDgYGJh4Y4NTJcWVl9e3uqqalcWlgpJyacm5q7urrJyMizsrLS0tKIhoaMioqZmJiTkpKgn5+Bf36WlZWdnJuFg4O4t7e2tbXFxMR3dXTg39/T0dLqKxxpAAAAOHRSTlMA/WCvR6hq/
    v7+OD3U9/1Fpw+SlxynxXWZ8yLp+IDo2ufp9s3oUPII+jyiwdZ1vczEli7waWKEmIInp28AAADMSURBVBiVNczXcsIwEAVQyQZLMrYhQOjV1DRKAomKJRkZ+P9PYpCcfbgze+buAgDA5nf1zL8TcLNamssiPG/
    vt2XbwmA8Rykqton/XVZAbYKTSxzVyvVlPMc4no2KYhFaePvU8fDHmGT93i47Xh8ijPrB/0lTcA3lcGQO7otPmZJfgwhhoytPeKX5LqxOPA9i7oDlwYwJ3p0iYaEqWDdlRB2nkDjgJPA7nX0QaVq3kPGPZq/V6qUqt9BAmVaCUcqEdACzTBFCpcyvFfAAxgMYYVy1sTwAAAAASUVORK5CYII=""",
    layout="wide"
)
def load_css_file(css_file_path):
    with open(css_file_path) as f:
        return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css_file(path + "main.css")

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
    left_col, right_col, margin_right = st.columns((0.7, 1, 0.25))
    with left_col:
        st.markdown(f'Benvingut **{name}**')
        # st.header("CONJUNTURA SECTORIAL")
    with margin_right:
        authenticator.logout('Tanca Sessió', 'main')
    with right_col:
        with open(path + "APCE_mod.png", "rb") as f:
            data_uri = base64.b64encode(f.read()).decode("utf-8")
        markdown = f"""
        <div class="image">
        <img src="data:image/png;base64, {data_uri}" alt="image" />
        </div>
        """
        st.markdown(markdown, unsafe_allow_html=True)

    # Creating a dropdown menu with options and icons, and customizing the appearance of the menu using CSS styles.
    selected = option_menu(
        menu_title=None,  # required
        options=["Espanya","Catalunya","Províncies i àmbits", "Municipis", "Districtes de Barcelona", "Contacte"],  # Dropdown menu
        icons=[None, None, "map", "house-fill", "house-fill", "envelope"],  # Icons for dropdown menu
        menu_icon="cast",  # optional
        default_index=0,  # optional
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fcefdc"},
            "icon": {"color": "#bf6002", "font-size": "17px"},
            "nav-link": {
                "font-size": "17px",
                "text-align": "center",
                "font-weight": "bold",
                "color":"#363534",
                "margin": "20px",
                "--hover-color": "#fcefdc",
                "background-color": "#fcefdc"},
            "nav-link-selected": {"background-color": "#de7207"},
            })


        
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
        
        maestro_mun = pd.read_excel("Maestro_MUN_COM_PROV.xlsx")
        maestro_dis = pd.read_excel("Maestro_dis_barris.xlsx")

        return([DT_terr, DT_terr_y, DT_mun, DT_mun_y, DT_dis, DT_dis_y, maestro_mun, maestro_dis])

    DT_terr, DT_terr_y, DT_mun, DT_mun_y, DT_dis, DT_dis_y, maestro_mun, maestro_dis = import_data()

    def tidy_Catalunya(data_ori, columns_sel, fecha_ini, fecha_fin, columns_output):
        output_data = data_ori[["Trimestre"] + columns_sel][(data_ori["Fecha"]>=fecha_ini) & (data_ori["Fecha"]<=fecha_fin)]
        output_data.columns = ["Trimestre"] + columns_output
        return(output_data.set_index("Trimestre").drop("Data", axis=1))
    def tidy_Catalunya_anual(data_ori, columns_sel, fecha_ini, fecha_fin, columns_output):
        output_data = data_ori[columns_sel][(data_ori["Fecha"]>=fecha_ini) & (data_ori["Fecha"]<=fecha_fin)]
        output_data.columns = columns_output
        output_data["Any"] = output_data["Any"].astype(str)
        return(output_data.set_index("Any"))    
    def concatenate_lists(list1, list2):
        result_list = []
        for i in list1:
            result_element = i+ list2
            result_list.append(result_element)
        return(result_list)
    def filedownload(df, filename):
        towrite = io.BytesIO()
        df.to_excel(towrite, encoding='latin-1', index=True, header=True)
        towrite.seek(0)
        b64 = base64.b64encode(towrite.read()).decode("latin-1")
        href = f"""<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">
        <button class="download-button">Descarregar</button></a>"""
        return href
    def line_plotly(table_n, selection_n, title_main, title_y):
        plot_cat = table_n[selection_n]
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
            title=title_main,
            xaxis=dict(title="Trimestre"),
            yaxis=dict(title=title_y)
        )
        fig = go.Figure(data=traces, layout=layout)
        return(fig)
    def bar_plotly(table_n, selection_n, title_main, title_y, year_ini):
        table_n = table_n.reset_index()
        table_n["Any"] = table_n["Any"].astype(int)
        plot_cat = table_n[table_n["Any"]>=year_ini][["Any"] + selection_n].set_index("Any")
        traces = []
        for col in plot_cat.columns:
            trace = go.Bar(
                x=plot_cat.index,
                y=plot_cat[col],
                name=col
            )
            traces.append(trace)
        layout = go.Layout(
            title=title_main,
            xaxis=dict(title="Any"),
            yaxis=dict(title=title_y)
        )
        fig = go.Figure(data=traces, layout=layout)
        return(fig)
    if selected == "Espanya":
        st.sidebar.header("Selecció")
        selected_type = st.sidebar.radio("", ("Indicadors macroeconòmics","Indicadors financers", "Sector residencial"))
        if selected_type=="Indicadors Macroeconòmics":
            st.sidebar.selectbox("", ["Producte Interior Brut per sectors", "Índex de Preus al Consum", "Ocupació per sectors", "Costos de construcció per tipologia", "Consum de Ciment"])
        if selected_type=="Indicadors financers":
            st.sidebar.selectbox("", ["Euribor", "Tipus d'interès dels prèstecs hipotecaris", "Nombre d'hipoteques", "Import d'hipoteques"])
        if selected_type=="Sector residencial":
            st.sidebar.selectbox("", ["Producció (MITMA)", "Compravendes (INE)", "Preu de l'habitatge (INE)"])
    if selected == "Catalunya":
        st.sidebar.header("Selecció")
        selected_indicator = st.sidebar.radio("", ("Indicadors macroeconòmics", "Indicadors financers", "Sector residencial"))
        if selected_indicator=="Indicadors macroeconòmics":
            selected_index = st.sidebar.selectbox("", ["Producte Interior Brut per sectors", "Índex de Preus al Consum", "Ocupació per sectors", "Consum de Ciment"])
        if selected_indicator=="Indicadors financers":
            selected_index = st.sidebar.selectbox("", ["Nombre d'hipoteques", "Import d'hipoteques"])
        if selected_indicator=="Sector residencial":
            selected_type = st.sidebar.radio("**Mercat de venda o lloguer**", ("Venda", "Lloguer"))
            if selected_type=="Venda":
                index_names = ["Producció", "Compravendes", "Preus", "Superfície"]
                selected_index = st.sidebar.selectbox("**Principals indicadors**", index_names)
                max_year=2022
                if selected_index=="Producció":
                    min_year=2008
                    st.subheader("PRODUCCIÓ D'HABITATGES A CATALUNYA")
                    st.markdown("La producció d'habitatge a Catalunya al 2022")
                    min_year, max_year = st.sidebar.slider("**Interval d'anys de la mostra**", value=[min_year, max_year], min_value=min_year, max_value=max_year)
                    table_Catalunya = tidy_Catalunya(DT_terr, ["Fecha", "iniviv_Catalunya", "finviv_Catalunya", "calprov_Cataluña", "caldef_Cataluña"], f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Habitatges Iniciats", "Habitatges acabats", "Qualificacions provisionals d'habitatge protegit", "Qualificacions definitives d'habitatge protegit"])
                    table_Catalunya_y = tidy_Catalunya_anual(DT_terr_y, ["Fecha", "iniviv_Catalunya", "finviv_Catalunya", "calprov_Cataluña", "caldef_Cataluña"], min_year, max_year,["Any", "Habitatges Iniciats", "Habitatges acabats", "Qualificacions provisionals d'habitatge protegit", "Qualificacions definitives d'habitatge protegit"])
                    selected_columns = st.multiselect("Selecciona el indicador: ", table_Catalunya.columns.tolist(), default=table_Catalunya.columns.tolist())
                    left_col, right_col = st.columns((1,1))
                    with left_col:
                        st.markdown("**Dades trimestrals**")
                        st.dataframe(table_Catalunya[selected_columns])
                        st.markdown(filedownload(table_Catalunya, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(line_plotly(table_Catalunya, selected_columns, "Oferta d'habitatges a Catalunya", "Indicador d'oferta en nivells"), use_container_width=True, responsive=True)
                    with right_col:
                        st.markdown("**Dades anuals**")
                        st.dataframe(table_Catalunya_y[selected_columns])
                        st.markdown(filedownload(table_Catalunya_y, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(bar_plotly(table_Catalunya_y, selected_columns, "Oferta d'habitatges a Catalunya", "Indicador d'oferta en nivells", 2019), use_container_width=True, responsive=True)
                if selected_index=="Compravendes":
                    min_year=2014
                    st.subheader("COMPRAVENDES D'HABITATGES A CATALUNYA")
                    st.markdown("Les compravendes d'habitatge a Catalunya al 2022")
                    min_year, max_year = st.sidebar.slider("**Interval d'anys de la mostra**", value=[min_year, max_year], min_value=min_year, max_value=max_year)
                    table_Catalunya = tidy_Catalunya(DT_terr, ["Fecha", "trvivt_Catalunya", "trvivs_Catalunya", "trvivn_Catalunya"], f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Compravendes d'habitatge total", "Compravendes d'habitatge de segona mà", "Compravendes d'habitatge nou"])
                    table_Catalunya_y = tidy_Catalunya_anual(DT_terr_y, ["Fecha", "trvivt_Catalunya", "trvivs_Catalunya", "trvivn_Catalunya"], min_year, max_year,["Any", "Compravendes d'habitatge total", "Compravendes d'habitatge de segona mà", "Compravendes d'habitatge nou"])
                    selected_columns = st.multiselect("Selecciona el indicador: ", table_Catalunya.columns.tolist(), default=table_Catalunya.columns.tolist())
                    left_col, right_col = st.columns((1,1))
                    with left_col:
                        st.markdown("**Dades trimestrals**")
                        st.dataframe(table_Catalunya[selected_columns])
                        st.markdown(filedownload(table_Catalunya, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(line_plotly(table_Catalunya, selected_columns, "Compravendes d'habitatge per tipologia d'habitatge", "Nombre de compravendes"), use_container_width=True, responsive=True)
                    with right_col:
                        st.markdown("**Dades anuals**")
                        st.dataframe(table_Catalunya_y[selected_columns])
                        st.markdown("")
                        st.markdown("")
                        st.markdown("")
                        st.markdown(filedownload(table_Catalunya_y, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(bar_plotly(table_Catalunya_y, selected_columns, "Compravendes d'habitatge per tipologia d'habitatge", "Nombre de compravendes", 2019), use_container_width=True, responsive=True)
                if selected_index=="Preus":
                    min_year=2014
                    st.subheader("PREUS PER M2 ÚTIL A CATALUNYA")
                    st.markdown("Els preus per m2 útil d'habitatge a Catalunya al 2022")
                    min_year, max_year = st.sidebar.slider("**Interval d'anys de la mostra**", value=[min_year, max_year], min_value=min_year, max_value=max_year)
                    table_Catalunya = tidy_Catalunya(DT_terr, ["Fecha", "prvivt_Catalunya", "prvivs_Catalunya", "prvivn_Catalunya"], f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Preu d'habitatge total", "Preus d'habitatge de segona mà", "Preus d'habitatge nou"])
                    table_Catalunya_y = tidy_Catalunya_anual(DT_terr_y, ["Fecha", "prvivt_Catalunya", "prvivs_Catalunya", "prvivn_Catalunya"], min_year, max_year,["Any", "Preu d'habitatge total", "Preus d'habitatge de segona mà", "Preus d'habitatge nou"])
                    selected_columns = st.multiselect("Selecciona el indicador: ", table_Catalunya.columns.tolist(), default=table_Catalunya.columns.tolist())
                    left_col, right_col = st.columns((1,1))
                    with left_col:
                        st.markdown("**Dades trimestrals**")
                        st.dataframe(table_Catalunya[selected_columns])
                        st.markdown(filedownload(table_Catalunya, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(line_plotly(table_Catalunya, selected_columns, "Preus per m2 per tipologia d'habitatge", "€/m2"), use_container_width=True, responsive=True)
                    with right_col:
                        st.markdown("**Dades anuals**")
                        st.dataframe(table_Catalunya_y[selected_columns])
                        st.markdown("")
                        st.markdown("")
                        st.markdown("")
                        st.markdown(filedownload(table_Catalunya_y, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(bar_plotly(table_Catalunya_y, selected_columns, "Preus per m2 per tipologia d'habitatge", "€/m2", 2019), use_container_width=True, responsive=True)
                if selected_index=="Superfície":
                    min_year=2014
                    st.subheader("SUPERFÍCIE EN M2 ÚTILS")
                    st.markdown("La superfície en m2 útils dels habitatges a Catalunya al 2022")
                    min_year, max_year = st.sidebar.slider("**Interval d'anys de la mostra**", value=[min_year, max_year], min_value=min_year, max_value=max_year)
                    table_Catalunya = tidy_Catalunya(DT_terr, ["Fecha", "supert_Catalunya", "supers_Catalunya", "supern_Catalunya"], f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Superfície mitjana total", "Superfície mitjana d'habitatge de segona mà", "Superfície mitjana d'habitatge nou"])
                    table_Catalunya_y = tidy_Catalunya_anual(DT_terr_y, ["Fecha", "supert_Catalunya", "supers_Catalunya", "supern_Catalunya"], min_year, max_year,["Any", "Superfície mitjana total", "Superfície mitjana d'habitatge de segona mà", "Superfície mitjana d'habitatge nou"])
                    selected_columns = st.multiselect("Selecciona el indicador: ", table_Catalunya.columns.tolist(), default=table_Catalunya.columns.tolist())
                    left_col, right_col = st.columns((1,1))
                    with left_col:
                        st.markdown("**Dades trimestrals**")
                        st.dataframe(table_Catalunya[selected_columns])
                        st.markdown(filedownload(table_Catalunya, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(line_plotly(table_Catalunya, selected_columns, "Superfície mitjana per tipologia d'habitatge", "m2 útils"), use_container_width=True, responsive=True)
                    with right_col:
                        st.markdown("**Dades anuals**")
                        st.dataframe(table_Catalunya_y[selected_columns])
                        st.markdown("")
                        st.markdown("")
                        st.markdown("")
                        st.markdown(filedownload(table_Catalunya_y, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(bar_plotly(table_Catalunya_y, selected_columns, "Superfície mitjana per tipologia d'habitatge", "m2 útils", 2019), use_container_width=True, responsive=True)   
            if selected_type=="Lloguer":
                index_names = ["Contractes", "Rendes mitjanes"]
                selected_index = st.sidebar.selectbox("**Principals indicadors**", index_names)
                max_year=2022
                if selected_index=="Contractes":
                    min_year=2005
                    st.subheader("CONTRACTES DE LLOGUER A CATALUNYA")
                    st.markdown("Els contractes de lloguer a Catalunya l'any 2022...")
                    min_year, max_year = st.sidebar.slider("**Interval d'anys de la mostra**", value=[min_year, max_year], min_value=min_year, max_value=max_year)
                    table_Catalunya = tidy_Catalunya(DT_terr, ["Fecha", "trvivalq_Catalunya"], f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Nombre de contractes"])
                    table_Catalunya_y = tidy_Catalunya_anual(DT_terr_y, ["Fecha", "trvivalq_Catalunya"], min_year, max_year,["Any", "Nombre de contractes"])
                    selected_columns = st.multiselect("Selecciona el indicador: ", table_Catalunya.columns.tolist(), default=table_Catalunya.columns.tolist())
                    left_margin, center_margin, right_margin = st.columns((0.5,10,0.5))
                    left_col, right_col = st.columns((1,1))
                    with left_col:
                        st.markdown("**Dades trimestrals**")
                        st.dataframe(table_Catalunya[selected_columns])
                        st.markdown(filedownload(table_Catalunya, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(line_plotly(table_Catalunya, selected_columns, "Contractes registrats d'habitatges en lloguer a Catalunya", "Nombre de contractes"), use_container_width=True, responsive=True)
                    with right_col:
                        st.markdown("**Dades anuals**")
                        st.dataframe(table_Catalunya_y[selected_columns])
                        st.markdown(filedownload(table_Catalunya_y, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(bar_plotly(table_Catalunya_y, selected_columns, "Contractes registrats d'habitatges en lloguer a Catalunya", "Nombre de contractes", 2005), use_container_width=True, responsive=True)   
                if selected_index=="Rendes mitjanes":
                    min_year=2005
                    st.subheader("RENDES MITJANES DE LLOGUER A CATALUNYA")
                    st.markdown("Les rendes mitjanes de lloguer a Catalunya al 2022")
                    min_year, max_year = st.sidebar.slider("**Interval d'anys de la mostra**", value=[min_year, max_year], min_value=min_year, max_value=max_year)
                    table_Catalunya = tidy_Catalunya(DT_terr, ["Fecha", "pmvivalq_Catalunya"], f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Rendes mitjanes de lloguer"])
                    table_Catalunya_y = tidy_Catalunya_anual(DT_terr_y, ["Fecha", "pmvivalq_Catalunya"], min_year, max_year,["Any", "Rendes mitjanes de lloguer"])
                    selected_columns = st.multiselect("Selecciona el indicador: ", table_Catalunya.columns.tolist(), default=table_Catalunya.columns.tolist())
                    left_col, right_col = st.columns((1,1))
                    with left_col:
                        st.markdown("**Dades trimestrals**")
                        st.dataframe(table_Catalunya[selected_columns])
                        st.markdown(filedownload(table_Catalunya, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(line_plotly(table_Catalunya, selected_columns, "Rendes mitjanes de lloguer a Catalunya", "€/mes"), use_container_width=True, responsive=True)
                    with right_col:
                        st.markdown("**Dades anuals**")
                        st.dataframe(table_Catalunya_y[selected_columns])
                        st.markdown(filedownload(table_Catalunya_y, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(bar_plotly(table_Catalunya_y, selected_columns, "Rendes mitjanes de lloguer a Catalunya", "€/mes", 2005), use_container_width=True, responsive=True)   
    if selected == "Províncies i àmbits":
        st.sidebar.header("Selecció")
        selected_type = st.sidebar.radio("**Mercat de venda o lloguer**", ("Venda", "Lloguer"))
        if selected_type=="Venda":
            st.sidebar.header("")
            prov_names = ["Barcelona", "Girona", "Tarragona", "Lleida"]
            ambit_names = ["Alt Pirineu i Aran","Camp de Tarragona","Comarques centrals","Comarques gironines","Metropolità","Penedès","Ponent","Terres de l'Ebre"]
            selected_option = st.sidebar.selectbox("**Selecciona una província o àmbit territorial**", ["Províncies", "Àmbits territorials"])
            if selected_option=="Àmbits territorials":
                selected_geo = st.sidebar.selectbox('', ambit_names, index= ambit_names.index("Metropolità"))
                index_indicator = ["Producció", "Compravendes", "Preus", "Superfície"]
                selected_index = st.sidebar.selectbox("**Selecciona un indicador**", index_indicator)
                max_year=2022
                if selected_index=="Producció":
                    min_year=2008
                    st.subheader(f"PRODUCCIÓ D'HABITATGES A L'ÀMBIT: {selected_geo.upper()}")
                    min_year, max_year = st.sidebar.slider("**Interval d'anys de la mostra**", value=[min_year, max_year], min_value=min_year, max_value=max_year)
                    table_province = tidy_Catalunya(DT_terr, ["Fecha"] + concatenate_lists(["iniviv_", "finviv_"], selected_geo), f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Habitatges Iniciats", "Habitatges acabats"])
                    table_province_y = tidy_Catalunya_anual(DT_terr_y, ["Fecha"] + concatenate_lists(["iniviv_", "finviv_"], selected_geo), min_year, max_year,["Any", "Habitatges Iniciats", "Habitatges acabats"])
                    selected_columns = st.multiselect("Selecciona el indicador: ", table_province.columns.tolist(), default=table_province.columns.tolist())
                    left_col, right_col = st.columns((1,1))
                    with left_col:
                        st.markdown("**Dades trimestrals**")
                        st.dataframe(table_province[selected_columns])
                        st.markdown(filedownload(table_province, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(line_plotly(table_province, selected_columns, "Oferta d'habitatges", "Nombre d'habitatges"), use_container_width=True, responsive=True)
                    with right_col:
                        st.markdown("**Dades anuals**")
                        st.dataframe(table_province_y[selected_columns])
                        st.markdown(filedownload(table_province_y, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(bar_plotly(table_province_y, selected_columns, "Oferta d'habitatges", "Nombre d'habitatges", 2005), use_container_width=True, responsive=True) 
                if selected_index=="Compravendes":
                    min_year=2014
                    st.subheader(f"COMPRAVENDES D'HABITATGE A L'ÀMBIT: {selected_geo.upper()}")
                    min_year, max_year = st.sidebar.slider("**Interval d'anys de la mostra**", value=[min_year, max_year], min_value=min_year, max_value=max_year)
                    table_province = tidy_Catalunya(DT_terr, ["Fecha"] + concatenate_lists(["trvivt_", "trvivs_", "trvivn_"], selected_geo), f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Compravendes d'habitatge total", "Compravendes d'habitatge de segona mà", "Compravendes d'habitatge nou"])
                    table_province_y = tidy_Catalunya_anual(DT_terr_y, ["Fecha"] + concatenate_lists(["trvivt_", "trvivs_", "trvivn_"], selected_geo), min_year, max_year,["Any", "Compravendes d'habitatge total", "Compravendes d'habitatge de segona mà", "Compravendes d'habitatge nou"])
                    selected_columns = st.multiselect("Selecciona el indicador: ", table_province.columns.tolist(), default=table_province.columns.tolist())
                    left_margin, center_margin, right_margin = st.columns((0.5,10,0.5))
                    left_col, right_col = st.columns((1,1))
                    with left_col:
                        st.markdown("**Dades trimestrals**")
                        st.dataframe(table_province[selected_columns])
                        st.markdown(filedownload(table_province, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(line_plotly(table_province, selected_columns, "Compravendes d'habitatge per tipologia d'habitatge", "Nombre de compravendes"), use_container_width=True, responsive=True)
                    with right_col:
                        st.markdown("**Dades anuals**")
                        st.dataframe(table_province_y[selected_columns])
                        st.markdown("")
                        st.markdown("")
                        st.markdown("")
                        st.markdown(filedownload(table_province_y, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(bar_plotly(table_province_y, selected_columns, "Compravendes d'habitatge per tipologia d'habitatge", "Nombre de compravendes", 2005), use_container_width=True, responsive=True) 
                if selected_index=="Preus":
                    min_year=2014
                    st.subheader(f"PREUS PER M2 ÚTIL D'HABITATGE A L'ÀMBIT: {selected_geo.upper()}")
                    min_year, max_year = st.sidebar.slider("**Interval d'anys de la mostra**", value=[min_year, max_year], min_value=min_year, max_value=max_year)
                    table_province = tidy_Catalunya(DT_terr, ["Fecha"] + concatenate_lists(["prvivt_", "prvivs_", "prvivn_"], selected_geo), f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Preu d'habitatge total", "Preus d'habitatge de segona mà", "Preus d'habitatge nou"])
                    table_province_y = tidy_Catalunya_anual(DT_terr_y, ["Fecha"] + concatenate_lists(["prvivt_", "prvivs_", "prvivn_"], selected_geo), min_year, max_year,["Any", "Preu d'habitatge total", "Preus d'habitatge de segona mà", "Preus d'habitatge nou"])
                    selected_columns = st.multiselect("Selecciona el indicador: ", table_province.columns.tolist(), default=table_province.columns.tolist())
                    left_col, right_col = st.columns((1,1))
                    with left_col:
                        st.markdown("**Dades trimestrals**")
                        st.dataframe(table_province[selected_columns])
                        st.markdown(filedownload(table_province, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(line_plotly(table_province, selected_columns, "Preus per m2 per tipologia d'habitatge", "€/m2 útil"), use_container_width=True, responsive=True)
                    with right_col:
                        st.markdown("**Dades anuals**")
                        st.dataframe(table_province_y[selected_columns])
                        st.markdown("")
                        st.markdown("")
                        st.markdown("")
                        st.markdown(filedownload(table_province_y, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(bar_plotly(table_province_y, selected_columns, "Preus per m2 per tipologia d'habitatge", "€/m2 útil", 2005), use_container_width=True, responsive=True) 
                if selected_index=="Superfície":
                    min_year=2014
                    st.subheader(f"SUPERFÍCIE EN M2 ÚTILS D'HABITATGE A L'ÀMBIT: {selected_geo.upper()}")
                    min_year, max_year = st.sidebar.slider("**Interval d'anys de la mostra**", value=[min_year, max_year], min_value=min_year, max_value=max_year)
                    table_province = tidy_Catalunya(DT_terr, ["Fecha"] + concatenate_lists(["supert_", "supers_", "supern_"], selected_geo), f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Superfície mitjana total", "Superfície mitjana d'habitatge de segona mà", "Superfície mitjana d'habitatge nou"])
                    table_province_y = tidy_Catalunya_anual(DT_terr_y, ["Fecha"] + concatenate_lists(["prvivt_", "prvivs_", "prvivn_"], selected_geo), min_year, max_year,["Any", "Preu d'habitatge total", "Preus d'habitatge de segona mà", "Preus d'habitatge nou"])
                    selected_columns = st.multiselect("Selecciona el indicador: ", table_province.columns.tolist(), default=table_province.columns.tolist())
                    left_col, right_col = st.columns((1,1))
                    with left_col:
                        st.markdown("**Dades trimestrals**")
                        st.dataframe(table_province[selected_columns])
                        st.markdown(filedownload(table_province, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(line_plotly(table_province, selected_columns, "Superfície mitjana en m2 útils per tipologia d'habitatge", "m2 útil"), use_container_width=True, responsive=True)
                    with right_col:
                        st.markdown("**Dades anuals**")
                        st.dataframe(table_province_y[selected_columns])
                        st.markdown("")
                        st.markdown("")
                        st.markdown("")
                        st.markdown(filedownload(table_province_y, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(bar_plotly(table_province_y, selected_columns, "Superfície mitjana en m2 útils per tipologia d'habitatge", 2005), use_container_width=True, responsive=True) 
            if selected_option=="Províncies":
                selected_geo = st.sidebar.selectbox('', prov_names, index= prov_names.index("Barcelona"))
                index_indicator = ["Producció", "Compravendes", "Preus", "Superfície"]
                selected_index = st.sidebar.selectbox("**Selecciona un indicador**", index_indicator)
                max_year=2022
                if selected_index=="Producció":
                    min_year=2008
                    st.subheader(f"PRODUCCIÓ D'HABITATGES A {selected_geo.upper()}")
                    min_year, max_year = st.sidebar.slider("**Interval d'anys de la mostra**", value=[min_year, max_year], min_value=min_year, max_value=max_year)
                    table_province = tidy_Catalunya(DT_terr, ["Fecha"] + concatenate_lists(["iniviv_", "finviv_"], selected_geo), f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Habitatges Iniciats", "Habitatges acabats"])
                    selected_columns = st.multiselect("Selecciona el indicador: ", table_province.columns.tolist(), default=table_province.columns.tolist())
                    left_margin, center_margin, right_margin = st.columns((0.5,10,0.5))
                    with center_margin:
                        st.dataframe(table_province[selected_columns])
                        st.markdown(filedownload(table_province, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(line_plotly(table_province, selected_columns, "Oferta d'habitatges", "Indicador d'oferta en nivells"), use_container_width=True, responsive=True)     
                if selected_index=="Compravendes":
                    min_year=2014
                    st.subheader(f"COMPRAVENDES D'HABITATGE A {selected_geo.upper()}")
                    min_year, max_year = st.sidebar.slider("**Interval d'anys de la mostra**", value=[min_year, max_year], min_value=min_year, max_value=max_year)
                    table_province = tidy_Catalunya(DT_terr, ["Fecha"] + concatenate_lists(["trvivt_", "trvivs_", "trvivn_"], selected_geo), f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Compravendes d'habitatge total", "Compravendes d'habitatge de segona mà", "Compravendes d'habitatge nou"])
                    selected_columns = st.multiselect("Selecciona el indicador: ", table_province.columns.tolist(), default=table_province.columns.tolist())
                    left_margin, center_margin, right_margin = st.columns((0.5,10,0.5))
                    with center_margin:
                        st.dataframe(table_province[selected_columns])
                        st.markdown(filedownload(table_province, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(line_plotly(table_province, selected_columns, "Compravendes d'habitatge per tipologia d'habitatge", "Nombre de compravendes"), use_container_width=True, responsive=True)     
                if selected_index=="Preus":
                    min_year=2014
                    st.subheader(f"PREUS PER M2 ÚTIL D'HABITATGE A {selected_geo.upper()}")
                    min_year, max_year = st.sidebar.slider("**Interval d'anys de la mostra**", value=[min_year, max_year], min_value=min_year, max_value=max_year)
                    table_province = tidy_Catalunya(DT_terr, ["Fecha"] + concatenate_lists(["prvivt_", "prvivs_", "prvivn_"], selected_geo), f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Preu d'habitatge total", "Preus d'habitatge de segona mà", "Preus d'habitatge nou"])
                    selected_columns = st.multiselect("Selecciona el indicador: ", table_province.columns.tolist(), default=table_province.columns.tolist())
                    left_margin, center_margin, right_margin = st.columns((0.5,10,0.5))
                    with center_margin:
                        st.dataframe(table_province[selected_columns])
                        st.markdown(filedownload(table_province, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(line_plotly(table_province, selected_columns, "Preus per m2 per tipologia d'habitatge", "€/m2 útil"), use_container_width=True, responsive=True)  
                if selected_index=="Superfície":
                    min_year=2014
                    st.subheader(f"SUPERFÍCIE EN M2 ÚTILS D'HABITATGE A {selected_geo.upper()}")
                    min_year, max_year = st.sidebar.slider("**Interval d'anys de la mostra**", value=[min_year, max_year], min_value=min_year, max_value=max_year)
                    table_province = tidy_Catalunya(DT_terr, ["Fecha"] + concatenate_lists(["supert_", "supers_", "supern_"], selected_geo), f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Superfície mitjana total", "Superfície mitjana d'habitatge de segona mà", "Superfície mitjana d'habitatge nou"])
                    selected_columns = st.multiselect("Selecciona el indicador: ", table_province.columns.tolist(), default=table_province.columns.tolist())
                    left_margin, center_margin, right_margin = st.columns((0.5,10,0.5))
                    with center_margin:
                        st.dataframe(table_province[selected_columns])
                        st.markdown(filedownload(table_province, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(line_plotly(table_province, selected_columns, "Superfície mitjana per tipologia d'habitatge", "m2 útil"), use_container_width=True, responsive=True)
        if selected_type=="Lloguer":
            st.sidebar.header("")
            prov_names = ["Barcelona", "Girona", "Tarragona", "Lleida"]
            ambit_names = ["Alt Pirineu i Aran","Camp de Tarragona","Comarques centrals","Comarques gironines","Metropolità","Penedès","Ponent","Terres de l'Ebre"]
            selected_option = st.sidebar.selectbox("**Selecciona una província o àmbit territorial**", ["Províncies", "Àmbits territorials"])
            max_year=2022
            if selected_option=="Àmbits territorials":
                selected_geo = st.sidebar.selectbox('', ambit_names, index= ambit_names.index("Metropolità"))
                selected_index = st.sidebar.selectbox("**Selecciona un indicador**", ["Contractes", "Rendes mitjanes"])
                if selected_index=="Contractes":
                    min_year=2014
                    st.subheader(f"CONTRACTES DE LLOGUER A L'ÀMBIT: {selected_geo.upper()}")
                    st.markdown("Els contractes de lloguer a Catalunya l'any 2022...")
                    table_province = tidy_Catalunya(DT_terr, ["Fecha"] + concatenate_lists(["trvivalq_"], selected_geo), f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Contractes de lloguer"])
                    selected_columns = st.multiselect("Selecciona el indicador: ", table_province.columns.tolist(), default=table_province.columns.tolist())
                    left_margin, center_margin, right_margin = st.columns((0.5,10,0.5))
                    with center_margin:
                        st.dataframe(table_province[selected_columns])
                        st.markdown(filedownload(table_province, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(line_plotly(table_province, selected_columns, "Contractes registrats d'habitatges en lloguer", "Nombre de contractes"), use_container_width=True, responsive=True)
                if selected_index=="Rendes mitjanes":
                    min_year=2014
                    st.subheader(f"RENDES MITJANES DE LLOGUER A L'ÀMBIT: {selected_geo.upper()}")
                    st.markdown("Les rendes mitjanes de lloguer a Catalunya al 2022")
                    table_province = tidy_Catalunya(DT_terr, ["Fecha"] + concatenate_lists(["pmvivalq_"], selected_geo), f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Rendes mitjanes de lloguer"])
                    selected_columns = st.multiselect("Selecciona el indicador: ", table_province.columns.tolist(), default=table_province.columns.tolist())
                    left_margin, center_margin, right_margin = st.columns((0.5,10,0.5))
                    with center_margin:
                        st.dataframe(table_province[selected_columns])
                        st.markdown(filedownload(table_province, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(line_plotly(table_province, selected_columns, "Rendes mitjanes de lloguer", "€/mes"), use_container_width=True, responsive=True)
            if selected_option=="Províncies":
                selected_geo = st.sidebar.selectbox('', prov_names, index= prov_names.index("Barcelona"))
                index_indicator = ["Contractes", "Rendes mitjanes"]
                selected_index = st.sidebar.selectbox("**Selecciona un indicador**", index_indicator)
                if selected_index=="Contractes":
                    min_year=2014
                    st.subheader(f"CONTRACTES DE LLOGUER A {selected_geo.upper()}")
                    st.markdown("Els contractes de lloguer a Catalunya l'any 2022...")
                    table_province = tidy_Catalunya(DT_terr, ["Fecha"] + concatenate_lists(["trvivalq_"], selected_geo), f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Contractes de lloguer"])
                    selected_columns = st.multiselect("Selecciona el indicador: ", table_province.columns.tolist(), default=table_province.columns.tolist())
                    left_margin, center_margin, right_margin = st.columns((0.5,10,0.5))
                    with center_margin:
                        st.dataframe(table_province[selected_columns])
                        st.markdown(filedownload(table_province, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(line_plotly(table_province, selected_columns, "Contractes registrats d'habitatges en lloguer", "Nombre de contractes"), use_container_width=True, responsive=True)
                if selected_index=="Rendes mitjanes":
                    min_year=2014
                    st.subheader(f"RENDES MITJANES DE LLOGUER A {selected_geo.upper()}")
                    st.markdown("Les rendes mitjanes de lloguer a Catalunya al 2022")                    
                    table_province = tidy_Catalunya(DT_terr, ["Fecha"] + concatenate_lists(["pmvivalq_"], selected_geo), f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Rendes mitjanes de lloguer"])
                    selected_columns = st.multiselect("Selecciona el indicador: ", table_province.columns.tolist(), default=table_province.columns.tolist())
                    left_margin, center_margin, right_margin = st.columns((0.5,10,0.5))
                    with center_margin:
                        st.dataframe(table_province[selected_columns])
                        st.markdown(filedownload(table_province, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                        st.plotly_chart(line_plotly(table_province, selected_columns, "Rendes mitjanes de lloguer", "€/mes"), use_container_width=True, responsive=True)
    
    if selected=="Municipis":
        st.sidebar.header("Selecció")
        selected_type = st.sidebar.radio("**Mercat de venda o lloguer**", ("Venda", "Lloguer"))
        if selected_type=="Venda":
            st.sidebar.header("Selecciona un municipi: ")
            selected_mun = st.sidebar.selectbox("", maestro_mun["Municipi"].unique(), index= maestro_mun["Municipi"].tolist().index("Barcelona"))
            index_names = ["Producció", "Compravendes", "Preus", "Superfície"]
            selected_index = st.sidebar.selectbox("", index_names)
            max_year=2022
            if selected_index=="Producció":
                min_year=2008
                st.subheader(f"PRODUCCIÓ D'HABITATGES A {selected_mun.upper()}")
                min_year, max_year = st.sidebar.slider("**Interval d'anys de la mostra**", value=[min_year, max_year], min_value=min_year, max_value=max_year)
                table_mun = tidy_Catalunya(DT_mun, ["Fecha"] + concatenate_lists(["iniviv_", "finviv_"], selected_mun), f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Habitatges Iniciats", "Habitatges acabats"])
                selected_columns = st.multiselect("Selecciona el indicador: ", table_mun.columns.tolist(), default=table_mun.columns.tolist())
                left_margin, center_margin, right_margin = st.columns((0.5,10,0.5))
                with center_margin:
                    st.dataframe(table_mun[selected_columns])
                    st.markdown(filedownload(table_mun, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                    st.plotly_chart(line_plotly(table_mun, selected_columns, "Oferta d'habitatges", "Indicador d'oferta en nivells"), use_container_width=True, responsive=True)
            if selected_index=="Compravendes":
                min_year=2014
                st.subheader(f"COMPRAVENDES D'HABITATGE A {selected_mun.upper()}")
                min_year, max_year = st.sidebar.slider("**Interval d'anys de la mostra**", value=[min_year, max_year], min_value=min_year, max_value=max_year)
                table_mun = tidy_Catalunya(DT_mun, ["Fecha"] + concatenate_lists(["trvivt_", "trvivs_", "trvivn_"], selected_mun), f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Compravendes d'habitatge total", "Compravendes d'habitatge de segona mà", "Compravendes d'habitatge nou"])
                selected_columns = st.multiselect("Selecciona el indicador: ", table_mun.columns.tolist(), default=table_mun.columns.tolist())
                left_margin, center_margin, right_margin = st.columns((0.5,10,0.5))
                with center_margin:
                    st.dataframe(table_mun[selected_columns])
                    st.markdown(filedownload(table_mun, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                    st.plotly_chart(line_plotly(table_mun, selected_columns, "Compravendes d'habitatge per tipologia d'habitatge", "Nombre de compravendes"), use_container_width=True, responsive=True)
            if selected_index=="Preus":
                min_year=2014
                st.subheader(f"PREUS PER M2 ÚTIL D'HABITATGE A {selected_mun.upper()}")
                min_year, max_year = st.sidebar.slider("**Interval d'anys de la mostra**", value=[min_year, max_year], min_value=min_year, max_value=max_year)
                table_mun = tidy_Catalunya(DT_mun, ["Fecha"] + concatenate_lists(["prvivt_", "prvivs_", "prvivn_"], selected_mun), f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Preu d'habitatge total", "Preus d'habitatge de segona mà", "Preus d'habitatge nou"])
                selected_columns = st.multiselect("Selecciona el indicador: ", table_mun.columns.tolist(), default=table_mun.columns.tolist())
                left_margin, center_margin, right_margin = st.columns((0.5,10,0.5))
                with center_margin:
                    st.dataframe(table_mun[selected_columns])
                    st.markdown(filedownload(table_mun, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                    st.plotly_chart(line_plotly(table_mun, selected_columns, "Preus per m2 per tipologia d'habitatge", "€/m2 útil"), use_container_width=True, responsive=True)
            if selected_index=="Superfície":
                min_year=2014
                st.subheader(f"SUPERFÍCIE EN M2 ÚTILS D'HABITATGE A {selected_mun.upper()}")
                min_year, max_year = st.sidebar.slider("**Interval d'anys de la mostra**", value=[min_year, max_year], min_value=min_year, max_value=max_year)
                table_mun = tidy_Catalunya(DT_mun, ["Fecha"] + concatenate_lists(["supert_", "supers_", "supern_"], selected_mun), f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Superfície mitjana total", "Superfície mitjana d'habitatge de segona mà", "Superfície mitjana d'habitatge nou"])
                selected_columns = st.multiselect("Selecciona el indicador: ", table_mun.columns.tolist(), default=table_mun.columns.tolist())
                left_margin, center_margin, right_margin = st.columns((0.5,10,0.5))
                with center_margin:
                    st.dataframe(table_mun[selected_columns])
                    st.markdown(filedownload(table_province, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                    st.plotly_chart(line_plotly(table_mun, selected_columns, "Superfície mitjana per tipologia d'habitatge", "m2 útil"), use_container_width=True, responsive=True)
        if selected_type=="Lloguer":
            st.sidebar.header("Selecciona un municipi: ")
            selected_mun = st.sidebar.selectbox("", maestro_mun["Municipi"].unique(), index= maestro_mun["Municipi"].tolist().index("Barcelona"))
            index_names = ["Contractes", "Rendes mitjanes"]
            selected_index = st.sidebar.selectbox("", index_names)
            max_year=2022
            if selected_index=="Contractes":
                min_year=2005
                st.subheader(f"CONTRACTES DE LLOGUER A {selected_mun.upper()}")
                min_year, max_year = st.sidebar.slider("**Interval d'anys de la mostra**", value=[min_year, max_year], min_value=min_year, max_value=max_year)
                table_mun = tidy_Catalunya(DT_mun, ["Fecha"] + concatenate_lists(["trvivalq_"], selected_mun), f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Contractes de lloguer"])
                selected_columns = st.multiselect("Selecciona el indicador: ", table_mun.columns.tolist(), default=table_mun.columns.tolist())
                left_margin, center_margin, right_margin = st.columns((0.5,10,0.5))
                with center_margin:
                    st.dataframe(table_mun[selected_columns])
                    st.markdown(filedownload(table_mun, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                    st.plotly_chart(line_plotly(table_mun, selected_columns, "Contractes registrats d'habitatges en lloguer", "Nombre de contractes"), use_container_width=True, responsive=True)
            if selected_index=="Rendes mitjanes":
                min_year=2005
                st.subheader(f"RENDES MITJANES DE LLOGUER A {selected_mun.upper()}")
                min_year, max_year = st.sidebar.slider("**Interval d'anys de la mostra**", value=[min_year, max_year], min_value=min_year, max_value=max_year)
                table_mun = tidy_Catalunya(DT_mun, ["Fecha"] + concatenate_lists(["pmvivalq_"], selected_mun), f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Rendes mitjanes"])
                selected_columns = st.multiselect("Selecciona el indicador: ", table_mun.columns.tolist(), default=table_mun.columns.tolist())
                left_margin, center_margin, right_margin = st.columns((0.5,10,0.5))
                with center_margin:
                    st.dataframe(table_mun[selected_columns])
                    st.markdown(filedownload(table_mun, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                    st.plotly_chart(line_plotly(table_mun, selected_columns, "Rendes mitjanes de lloguer", "€/mes"), use_container_width=True, responsive=True)
    if selected=="Districtes de Barcelona":
        st.sidebar.header("Selecció")
        selected_type = st.sidebar.radio("**Mercat de venda o lloguer**", ("Venda", "Lloguer"))
        if selected_type=="Venda":
            st.sidebar.header("")
            selected_dis = st.sidebar.selectbox("**Selecciona un districte de Barcelona:**", maestro_dis["Districte"].unique())
            index_names = ["Producció", "Compravendes", "Preus", "Superfície"]
            selected_index = st.sidebar.selectbox("**Selecciona un indicador**", index_names)
            max_year=2022
            if selected_index=="Producció":
                min_year=2011
                st.subheader(f"PRODUCCIÓ D'HABITATGES A {selected_dis.upper()}")
                min_year, max_year = st.sidebar.slider("**Interval d'anys de la mostra**", value=[min_year, max_year], min_value=min_year, max_value=max_year)
                table_dis = tidy_Catalunya(DT_dis, ["Fecha"] + concatenate_lists(["iniviv_", "finviv_"], selected_dis), f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Habitatges Iniciats", "Habitatges acabats"])
                selected_columns = st.multiselect("Selecciona el indicador: ", table_dis.columns.tolist(), default=table_dis.columns.tolist())
                left_margin, center_margin, right_margin = st.columns((0.5,10,0.5))
                with center_margin:
                    st.dataframe(table_dis[selected_columns])
                    st.markdown(filedownload(table_dis, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                    st.plotly_chart(line_plotly(table_dis, selected_columns, "Oferta d'habitatges", "Indicador d'oferta en nivells"), use_container_width=True, responsive=True)
            if selected_index=="Compravendes":
                min_year=2017
                st.subheader(f"COMPRAVENDES D'HABITATGE A {selected_dis.upper()}")
                min_year, max_year = st.sidebar.slider("**Interval d'anys de la mostra**", value=[min_year, max_year], min_value=min_year, max_value=max_year)
                table_dis = tidy_Catalunya(DT_dis, ["Fecha"] + concatenate_lists(["trvivt_", "trvivs_", "trvivn_"], selected_dis), f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Compravendes d'habitatge total", "Compravendes d'habitatge de segona mà", "Compravendes d'habitatge nou"])
                selected_columns = st.multiselect("Selecciona el indicador: ", table_dis.columns.tolist(), default=table_dis.columns.tolist())
                left_margin, center_margin, right_margin = st.columns((0.5,10,0.5))
                with center_margin:
                    st.dataframe(table_dis[selected_columns])
                    st.markdown(filedownload(table_dis, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                    st.plotly_chart(line_plotly(table_dis, selected_columns, "Compravendes d'habitatge per tipologia d'habitatge", "Nombre de compravendes"), use_container_width=True, responsive=True)
            if selected_index=="Preus":
                min_year=2017
                st.subheader(f"PREUS PER M2 ÚTIL D'HABITATGE A {selected_dis.upper()}")
                min_year, max_year = st.sidebar.slider("**Interval d'anys de la mostra**", value=[min_year, max_year], min_value=min_year, max_value=max_year)
                table_dis = tidy_Catalunya(DT_dis, ["Fecha"] + concatenate_lists(["prvivt_", "prvivs_", "prvivn_"], selected_dis), f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Preu d'habitatge total", "Preus d'habitatge de segona mà", "Preus d'habitatge nou"])
                selected_columns = st.multiselect("Selecciona el indicador: ", table_dis.columns.tolist(), default=table_dis.columns.tolist())
                left_margin, center_margin, right_margin = st.columns((0.5,10,0.5))
                with center_margin:
                    st.dataframe(table_dis[selected_columns])
                    st.markdown(filedownload(table_dis, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                    st.plotly_chart(line_plotly(table_dis, selected_columns, "Preus per m2 per tipologia d'habitatge", "€/m2 útil"), use_container_width=True, responsive=True)
            if selected_index=="Superfície":
                min_year=2017
                st.subheader(f"SUPERFÍCIE EN M2 ÚTILS D'HABITATGE A {selected_dis.upper()}")
                min_year, max_year = st.sidebar.slider("**Interval d'anys de la mostra**", value=[min_year, max_year], min_value=min_year, max_value=max_year)
                table_dis = tidy_Catalunya(DT_dis, ["Fecha"] + concatenate_lists(["supert_", "supers_", "supern_"], selected_dis), f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Superfície mitjana total", "Superfície mitjana d'habitatge de segona mà", "Superfície mitjana d'habitatge nou"])
                selected_columns = st.multiselect("Selecciona el indicador: ", table_dis.columns.tolist(), default=table_dis.columns.tolist())
                left_margin, center_margin, right_margin = st.columns((0.5,10,0.5))
                with center_margin:
                    st.dataframe(table_dis[selected_columns])
                    st.markdown(filedownload(table_dis, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                    st.plotly_chart(line_plotly(table_dis, selected_columns, "Superfície mitjana per tipologia d'habitatge", "m2 útil"), use_container_width=True, responsive=True)
        if selected_type=="Lloguer":
            st.sidebar.header("")
            selected_dis = st.sidebar.selectbox("**Selecciona un districte de Barcelona:**", maestro_dis["Districte"].unique())
            index_names = ["Contractes", "Rendes mitjanes"]
            selected_index = st.sidebar.selectbox("**Selecciona un indicador**", index_names)
            max_year=2022
            if selected_index=="Contractes":
                min_year=2005
                st.subheader(f"CONTRACTES DE LLOGUER A {selected_dis.upper()}")
                min_year, max_year = st.sidebar.slider("**Interval d'anys de la mostra**", value=[min_year, max_year], min_value=min_year, max_value=max_year)
                table_dis = tidy_Catalunya(DT_dis, ["Fecha"] + concatenate_lists(["trvivalq_"], selected_dis), f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Contractes de lloguer"])
                selected_columns = st.multiselect("Selecciona el indicador: ", table_dis.columns.tolist(), default=table_dis.columns.tolist())
                left_margin, center_margin, right_margin = st.columns((0.5,10,0.5))
                with center_margin:
                    st.dataframe(table_dis[selected_columns])
                    st.markdown(filedownload(table_dis, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                    st.plotly_chart(line_plotly(table_dis, selected_columns, "Contractes registrats d'habitatges en lloguer", "Nombre de contractes"), use_container_width=True, responsive=True)
            if selected_index=="Rendes mitjanes":
                min_year=2005
                st.subheader(f"RENDES MITJANES DE LLOGUER A {selected_dis.upper()}")
                min_year, max_year = st.sidebar.slider("**Interval d'anys de la mostra**", value=[min_year, max_year], min_value=min_year, max_value=max_year)
                table_dis = tidy_Catalunya(DT_dis, ["Fecha"] + concatenate_lists(["pmvivalq_"], selected_dis), f"{str(min_year)}-01-01", f"{str(max_year+1)}-01-01",["Data", "Rendes mitjanes"])
                selected_columns = st.multiselect("Selecciona el indicador: ", table_dis.columns.tolist(), default=table_dis.columns.tolist())
                left_margin, center_margin, right_margin = st.columns((0.5,10,0.5))
                with center_margin:
                    st.dataframe(table_dis[selected_columns])
                    st.markdown(filedownload(table_dis, f"{selected_index}.xlsx"), unsafe_allow_html=True)
                    st.plotly_chart(line_plotly(table_dis, selected_columns, "Rendes mitjanes de lloguer", "€/mes"), use_container_width=True, responsive=True)
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


