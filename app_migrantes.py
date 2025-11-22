import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import numpy as np

# ============================
# CARGA DE DATOS
# ============================

Df_final = pd.read_parquet("data/migrantes.parquet")

# =====================================
# VARIABLES PARA MÉTRICAS
# =====================================

variables = Df_final.shape[1]
filas = Df_final.shape[0]
paises = Df_final['País'].nunique()
list_paises = Df_final['País'].dropna().unique().tolist()
numero_etnias = Df_final['Etnia de la persona'].nunique()
list_areas = Df_final['Área Conocimiento'].dropna().unique().tolist()
list_etnia = Df_final['Etnia de la persona'].dropna().unique().tolist()

registros = Df_final['Año de Registro'].value_counts().sort_index()
registros.index = registros.index.astype(int)

# ============================================
# Cálculo de Totales y Deltas 
# ============================================

tot_13 = registros[2013]
tot_14 = registros[2014]
tot_15 = registros[2015]
tot_16 = registros[2016]
tot_17 = registros[2017]
tot_18 = registros[2018]
tot_19 = registros[2019]
tot_20 = registros[2020]
tot_21 = registros[2021]
tot_22 = registros[2022]
tot_23 = registros[2023]
tot_24 = registros[2024]
tot_25 = registros[2025]

delta_14 = (tot_14 - tot_13)/tot_13*100
delta_15 = (tot_15 - tot_14)/tot_14*100
delta_16 = (tot_16 - tot_15)/tot_15*100
delta_17 = (tot_17 - tot_16)/tot_16*100
delta_18 = (tot_18 - tot_17)/tot_17*100
delta_19 = (tot_19 - tot_18)/tot_18*100
delta_20 = (tot_20 - tot_19)/tot_19*100
delta_21 = (tot_21 - tot_20)/tot_20*100
delta_22 = (tot_22 - tot_21)/tot_21*100
delta_23 = (tot_23 - tot_22)/tot_22*100
delta_24 = (tot_24 - tot_23)/tot_23*100
delta_25 = (tot_25 - tot_24)/tot_24*100

# ============================
# CONFIGURACIÓN STREAMLIT
# ============================

st.set_page_config(
    page_title='Registros de Migrantes Colombianos en el Exterior',
    layout='centered',
    initial_sidebar_state='collapsed'
)

st.markdown("""
<style>
    .block-container {
        max-width: 1200px;
    }
</style>
""", unsafe_allow_html=True)

st.image('img/Registro migratorio (2).jpg')
st.caption('Aplicación desarrollada por Jesus Cañas y Mariana Trujillo')

# ============================
# MÉTRICAS
# ============================

st.markdown('<a id="inicio"></a><br><br>', unsafe_allow_html=True)
with st.container(border=True):
    st.html('<font size=5><font color=#3D6E85>Acerca del Conjunto de Datos</font>')

    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Número de Variables', variables)
    col2.metric('Total de migrantes', filas)
    col3.metric('Número de países', paises)
    col4.metric('Número de etnias', numero_etnias)

    if st.checkbox('Mostrar detalles del Dataset'):
        st.write('Conjunto de datos obtenido del Portal de Datos Abiertos del Gobierno de Colombia.')

# ============================
# TOP 5 DEPARTAMENTOS
# ============================

st.markdown('<a id="5dep"></a><br><br>', unsafe_allow_html=True)
with st.expander('Top 5 departamentos con más migrantes'):
    departamento = Df_final['departamento de origen'].value_counts().head(7)
    df_plot = departamento.reset_index()
    df_plot.columns = ['Departamento', 'Migrantes']

    fig2 = px.bar(
        df_plot.head(5),
        x='Migrantes', y='Departamento',
        color='Departamento',
        title='Top 5 departamentos con mayor número de migrantes',
        height=500
    )
    st.plotly_chart(fig2, use_container_width=True)

# ============================
# TOP 5 AREAS DE CONOCIMIENTO
# ============================

st.markdown('<a id="5area"></a><br><br>', unsafe_allow_html=True)
with st.expander('Top 5 Areas de conocimiento'):
    area = Df_final['Área Conocimiento'].value_counts().head(7)
    df_plot = area.reset_index()
    df_plot.columns = ['Área de conocimento', 'Migrantes']

    fig2 = px.bar(
        df_plot.head(5),
        x='Migrantes', y='Area de conocimiento',
        color='Departamento',
        title='Top 5 departamentos con mayor número de migrantes',
        height=500
    )
    st.plotly_chart(fig2, use_container_width=True)


# ============================
# EXPLORADOR
# ============================

st.markdown('<a id="explorador"></a><br><br>', unsafe_allow_html=True)
with st.container(border=True):

    st.html('<font size=6><font color=#3D6E85>Explorador</font>')
    col5, col6 = st.columns(2)

    # ============================
    # GRUPO DE EDAD POR PAÍS
    # ============================
    with col5:
        st.html('<font size=5><font color=#3D6E85>Migrantes por grupo de edad en cada país</font>')

        pais_selec = st.selectbox('Selecciona un país:', list_paises)

        df_edad = Df_final.groupby('Grupo edad')['País'].value_counts().unstack().fillna(0)
        df_pais = df_edad[pais_selec]

        fig_barras = go.Figure()
        fig_barras.add_trace(go.Bar(
            x=df_pais.values,
            y=df_pais.index,
            orientation='h',
            marker_color='#4E7F96'
        ))

        fig_barras.update_layout(
            height=400,
            xaxis_title='Migrantes',
            yaxis_title='Grupo de edad',
            showlegend=False
        )
        st.plotly_chart(fig_barras, use_container_width=True)

    # ============================
    # ETNIA POR PAÍS (CORREGIDO)
    # ============================

    with col6:
        st.html('<font size=5><font color=#3D6E85>Etnia por país</font>')

        pais_selec2 = st.selectbox('Selecciona un país:', list_paises, key='etnia_pais')

        df_temp = Df_final[Df_final['País'] == pais_selec2]
        etnia_data = df_temp['Etnia de la persona'].value_counts()

        fig_barras = go.Figure()
        fig_barras.add_trace(go.Bar(
            x=etnia_data.values,
            y=etnia_data.index,
            orientation='h',
            marker_color='#4E7F96'
        ))

        fig_barras.update_layout(
            height=400,
            xaxis_title='Migrantes',
            yaxis_title='Etnia',
            showlegend=False
        )
        st.plotly_chart(fig_barras, use_container_width=True)

    col7, col8 = st.columns(2)

    # ============================
    # SUBÁREA DE CONOCIMIENTO
    # ============================
    with col7:
        st.html('<font size=5><font color=#3D6E85>Migrantes por subárea de conocimiento</font>')

        area = st.selectbox('Selecciona un área:', list_areas)
        subadmin = Df_final[Df_final['Área Conocimiento'] == area]['Sub Area Conocimiento'].value_counts()

        fig_barras2 = go.Figure()
        fig_barras2.add_trace(go.Bar(
            x=subadmin.values,
            y=subadmin.index,
            orientation='h',
            marker_color='#4E7F96'
        ))

        fig_barras2.update_layout(
            height=400,
            xaxis_title='Migrantes por subárea',
            yaxis_title='Subárea de conocimiento',
            showlegend=False
        )
        st.plotly_chart(fig_barras2, use_container_width=True)

    # ============================
    # TOP 5 REGIONES DE CADA PAÍS CON MÁS MIGRANTES
    # ============================
    with col8:
        st.html('<font size=5><font color=#3D6E85>Migrantes establecidos en región</font>')

        pais_select = st.selectbox('Selecciona un país:', list_paises, key='region')

        nombre = 'Estados' if pais_select in ['AUSTRALIA', 'ESTADOS UNIDOS'] else 'Provincias'

        df_pais1 = Df_final[Df_final['País'] == pais_select]
        regiones = df_pais1['Estado de residencia'].value_counts().head(5)

        fig_barras2 = go.Figure()
        fig_barras2.add_trace(go.Bar(
            x=regiones.values,
            y=regiones.index,
            orientation='h',
            marker_color='#4E7F96'
        ))

        fig_barras2.update_layout(
            height=400,
            xaxis_title='Migrantes por región',
            yaxis_title=nombre,
            showlegend=False
        )
        st.plotly_chart(fig_barras2, use_container_width=True)




# ============================================
# INDICADORES
# ============================================

st.markdown('<a id="indicadores"></a><br><br>', unsafe_allow_html=True)

with st.container(border=True):

    st.html('<font size=5><font color=#3D6E85>Indicadores de Registros por año</font>')

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label='2014', value=tot_14, delta=f'{round(delta_14,2)}%', border=True)
    col2.metric(label='2015', value=tot_15, delta=f'{round(delta_15,2)}%', border=True)
    col3.metric(label='2016', value=tot_16, delta=f'{round(delta_16,2)}%', border=True)
    col4.metric(label='2017', value=tot_17, delta=f'{round(delta_17,2)}%', border=True)

    # --- FILA 2: 2018–2021 ---
    col5, col6, col7, col8 = st.columns(4)
    col5.metric(label='2018', value=tot_18, delta=f'{round(delta_18,2)}%', border=True)
    col6.metric(label='2019', value=tot_19, delta=f'{round(delta_19,2)}%', border=True)
    col7.metric(label='2020', value=tot_20, delta=f'{round(delta_20,2)}%', border=True)
    col8.metric(label='2021', value=tot_21, delta=f'{round(delta_21,2)}%', border=True)

    # --- FILA 3: 2022–2025 ---
    col9, col10, col11, col12 = st.columns(4)
    col9.metric(label='2022', value=tot_22, delta=f'{round(delta_22,2)}%', border=True)
    col10.metric(label='2023', value=tot_23, delta=f'{round(delta_23,2)}%', border=True)
    col11.metric(label='2024', value=tot_24, delta=f'{round(delta_24,2)}%', border=True)
    col12.metric(label='2025', value=tot_25, delta=f'{round(delta_25,2)}%', border=True)

    with st.container(border=True):
        df_plot = pd.DataFrame({
            "Año": [
                2013, 2014, 2015, 2016, 2017, 2018,
                2019, 2020, 2021, 2022, 2023, 2024, 2025
            ],
            "Registros": [
                tot_13, tot_14, tot_15, tot_16, tot_17, tot_18,
                tot_19, tot_20, tot_21, tot_22, tot_23, tot_24, tot_25
            ]
        }).set_index("Año")

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df_plot.index,
                y=df_plot["Registros"],
                mode='lines+markers',
                line=dict(color="#4E7F96")
            )
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, config={'scrollZoom': False})

        st.caption('*Fuente: Datos Abiertos del Gobierno Nacional de Colombia*')

# ============================
# NIVEL ACADÉMICO Y GÉNERO / TORTAS
# ============================

st.markdown('<a id="adicionales"></a><br><br>', unsafe_allow_html=True)
with st.container(border=True):

    col13, col14 = st.columns(2)

    # ============================
    # NIVEL ACADÉMICO POR GÉNERO
    # ============================
    with col13:
        st.html('<font size=5><font color=#3D6E85>Nivel académico por género</font>')

        df_gen = Df_final[Df_final['Género'].isin(['FEMENINO', 'MASCULINO'])]
        nivel_genero = df_gen.groupby('Nivel Académico')['Género'].value_counts().unstack().fillna(0)

        fig4 = px.bar(
            nivel_genero,
            x=nivel_genero.index,
            y=['FEMENINO', 'MASCULINO'],
            barmode='stack',
            title='Migrantes por nivel académico y género',
            height=500
        )
        st.plotly_chart(fig4, use_container_width=True)

    # ============================
    # TORTA PAÍSES
    # ============================
    with col14:
        st.html('<font size=5><font color=#3D6E85>Distribución de migrantes por país</font>')

        paises_migrantes = Df_final['País'].value_counts()

        fig5 = px.pie(
            names=paises_migrantes.index,
            values=paises_migrantes.values,
            title='Distribución de migrantes por país',
            height=500
        )
        st.plotly_chart(fig5, use_container_width=True)

# ============================
# SIDEBAR
# ============================

with st.sidebar:
    st.markdown('''
                <style>
                [data-testid="stSidebar"] a {
                    display: block;
                    color: #3D6E85;
                    text-decoration: none;
                    padding: 10px 5px;
                    border-radius: 6px;
                }
                [data-testid="stSidebar"] a:hover {
                    background-color: #FFFFFF;
                }
                </style>
                ''',
                unsafe_allow_html=True)

    st.html('<font size=4><font color=#3D6E85>Menú de Navegación</font>')
    st.markdown('[Acerca del Dataset](#inicio)')
    st.markdown('[Top 5 departamentos con migrantes](#5area)')
    st.markdown('[Top 5 Areas con migrantes](#5dep)')
    st.markdown('[Explorador](#explorador)')
    st.markdown('[Indicadores](#indicadores)')
    st.markdown('[Adicionales](#adicionales)')
    st.markdown('---')
    st.caption('jarmando.canas@udea.edu.co \n mariana.trujillo2@udea.edu.co')
