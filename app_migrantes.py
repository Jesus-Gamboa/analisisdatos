import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st


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
list_paises = Df_final['País'].unique().tolist()
numero_etnias = Df_final['Etnia de la persona'].nunique()
list_areas = Df_final['Área Conocimiento'].dropna().unique().tolist()
list_etnia = Df_final['Etnia de la persona'].dropna().unique().tolist()

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
# GRUPO DE EDAD POR PAÍS
# ============================
st.markdown('<a id="edad"></a><br><br>', unsafe_allow_html=True)
with st.container(border=True):
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
# GRUPO DE etnia POR PAÍS
# ============================

st.markdown('<a id="etnia"></a><br><br>', unsafe_allow_html=True)
with st.container(border=True):
    st.html('<font size=5><font color=#3D6E85>Etnia cada país</font>')
    
    etnia_selec = st.selectbox('Selecciona un país:', list_etnia)

    condicion = Df_final['Etnia de la persona'] == etnia_selec
    df_pais = Df_final.groupby('País')['Etnia de la persona'].value_counts().unstack().fillna(0)
    df_etnia = df_pais[etnia_selec]

    fig_barras = go.Figure()
    fig_barras.add_trace(go.Bar(
        x=df_etnia.values,
        y=df_etnia.index,
        orientation='h',
        marker_color='#4E7F96'
    ))

    fig_barras.update_layout(
        height=400,
        xaxis_title='Migrantes',
        yaxis_title='País',
        showlegend=False
    )
    st.plotly_chart(fig_barras, use_container_width=True)


# ============================
# SUBÁREA DE CONOCIMIENTO
# ============================

st.markdown('<a id="subarea"></a><br><br>', unsafe_allow_html=True)
with st.container(border=True):
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
# REGISTROS POR AÑO
# ============================

st.markdown('<a id="registros"></a><br><br>', unsafe_allow_html=True)
with st.container(border=True):
    st.html('<font size=5><font color=#3D6E85>Número de registros por año</font>')

    registros_ano = Df_final['Año de Registro'].value_counts().sort_index()

    fig3 = px.line(
        x=registros_ano.index,
        y=registros_ano.values,
        markers=True,
        title='Número de registros por año',
        labels={'x': 'Año', 'y': 'Registros'},
        height=500
    )
    st.plotly_chart(fig3, use_container_width=True)


# ============================
# NIVEL ACADÉMICO Y GÉNERO
# ============================
st.markdown('<a id="genero"></a><br><br>', unsafe_allow_html=True)
with st.container(border=True):
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
# DISTRIBUCIÓN POR PAÍS
# ============================
st.markdown('<a id="tortas"></a><br><br>', unsafe_allow_html=True)
with st.container(border=True):
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
    st.markdown('[Top 5 departamentos con migrantes](#5dep)')
    st.markdown('[Migrantes por grupo de edad](#edad)')
    st.markdown('[Subárea de conocimiento](#subarea)')
    st.markdown('[Registros por año](#registros)')
    st.markdown('[Nivel académico por género](#genero)')
    st.markdown('[Distribución por país](#tortas)')
    st.markdown('---')
    st.caption('jarmando.canas@udea.edu.co --- mariana.trujillo2@udea.edu.co')
    