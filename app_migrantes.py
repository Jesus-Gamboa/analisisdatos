import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st


# ============================
# CARGA DE DATOS
# ============================

df = pd.read_excel('data/Colombianos_registrados_en_el_exterior_20251113 (1).xlsx', engine='openpyxl')

# ============================
# DICCIONARIOS DE REEMPLAZO
# ============================

remplasos_area = {
    'ECONOM�A': 'ECONOMIA',
    'ADMINISTRACI�N': 'ADMINISTRACION',
    'INGENIER�A': 'INGENIERIA',
    'AGRONOM�A': 'AGRONOMIA',
    'CIENCIAS DE LA EDUCACI�N': 'CIENCIAS DE LA EDUCACION',
    'CIENCIAS SOCIALES, PERIODISMO E INFORMACI�N': 'CIENCIAS SOCIALES, PERIODISMO E INFORMACION',
    'MATEM�TICAS': 'MATEMATICAS',
    'TECNOLOG�AS': 'TECNOLOGIAS',
    'PROGRAMAS Y CERTIFICACIONES GEN�RICAS': 'PROGRAMAS Y CERTIFICACIONES GENERICAS',
    'ESTAD�STICA': 'ESTADISTICA',
    'AVIACI�N': 'AVIACION',
    'EDUCACI�N': 'EDUCACION',
    'DISE�O': 'DISENO',
    'F�SICA': 'FISICA',
    'M�SICA': 'MUSICA',
    'NUTRICI�N': 'NUTRICION',
    'ANTROPOLOG�A': 'ANTROPOLOGIA',
    'LING��STICA': 'LINGUISTICA',
    'QU�MICA': 'QUIMICA',
    'ODONTOLOG�A': 'ODONTOLOGIA',
    'GEOLOG�A': 'GEOLOGIA',
    'FILOSOF�A': 'FILOSOFIA',
    'INSTRUMENTACI�N': 'INSTRUMENTACION',
    'SALUD P�BLICA': 'SALUD PUBLICA',
    'OPTOMETR�A': 'OPTOMETRIA',
    'TECNOLOGIAS DE LA INFORMACI�N Y LA COMUNICACI�N (TIC)': 'TECNOLOGIAS DE LA INFORMACION Y LA COMUNICACION (TIC)',
    'INGENIERIA, INDUSTRIA Y CONSTRUCCI�N': 'INGENIERIA, INDUSTRIA Y CONSTRUCCION'
}

remplazos_subarea = {
    'PERIODISMO, COMUNICACI�N SOCIAL Y AFINES': 'PERIODISMO, COMUNICACION SOCIAL Y AFINES',
    'ADMINISTRACI�N': 'ADMINISTRACION',
    'INGENIER�A INDUSTRIAL Y AFINES': 'INGENIERIA INDUSTRIAL Y AFINES',
    'SOCIOLOG�A, TRABAJO SOCIAL Y AFINES': 'SOCIOLOGIA, TRABAJO SOCIAL Y AFINES',
    'CONTADUR�A P�BLICA': 'CONTADURIA PUBLICA',
    'ENFERMER�A': 'ENFERMERIA',
    'INGENIER�A CIVIL Y AFINES': 'INGENIERIA CIVIL Y AFINES',
    'AGRONOM�A': 'AGRONOMIA',
    'INGENIER�A MEC�NICA Y AFINES': 'INGENIERIA MECANICA Y AFINES',
    'PSICOLOG�A Y AFINES': 'PSICOLOGIA Y AFINES',
    'ECONOM�A': 'ECONOMIA',
    'DISE�O': 'DISENO',
    'INGENIER�A EL�CTRICA Y AFINES': 'INGENIERIA ELECTRICA Y AFINES',
    'INGENIER�A ELECTR�NICA, TELECOMUNICACIONES Y AFINES': 'INGENIERIA ELECTRONICA, TELECOMUNICACIONES Y AFINES',
    'INGENIER�A EN SISTEMAS, TELEM�TICA Y AFINES': 'INGENIERIA EN SISTEMAS, TELEMATICA Y AFINES',
    'CIENCIA POL�TICA Y/O RELACIONES INTERNACIONALES': 'CIENCIA POLITICA Y/O RELACIONES INTERNACIONALES',
    'EDUCACI�N': 'EDUCACION',
    'FILOSOF�A, TEOLOG�A Y AFINES': 'FILOSOFIA, TEOLOGIA Y AFINES',
    'GEOLOG�A': 'GEOLOGIA',
    'ODONTOLOG�A': 'ODONTOLOGIA',
    'INGENIER�A QU�MICA Y AFINES': 'INGENIERIA QUIMICA Y AFINES',
    'ARTES DRAM�TICAS Y REPRESENTATIVAS': 'ARTES DRAMATICAS Y REPRESENTATIVAS',
    'BACTERIOLOG�A': 'BACTERIOLOGIA',
    'SALUD P�BLICA': 'SALUD PUBLICA',
    'MATEM�TICAS, ESTAD�STICA Y AFINES': 'MATEMATICAS, ESTADISTICA Y AFINES',
    'ARTES PL�STICAS, VISUALES Y AFINES': 'ARTES PLASTICAS, VISUALES Y AFINES',
    'INSTRUMENTACI�N QUIR�RGICA': 'INSTRUMENTACION QUIRURGICA',
    'BIOLOG�A, MICROBIOLOG�A Y AFINES': 'BIOLOGIA, MICROBIOLOGIA Y AFINES',
    'INGENIER�A DE MINAS, METALURGIA Y AFINES': 'INGENIERIA DE MINAS, METALURGIA Y AFINES',
    'INGENIER�A ADMINISTRATIVA Y AFINES': 'INGENIERIA ADMINISTRATIVA Y AFINES',
    'INGENIER�A AGR�COLA, FORESTAL Y AFINES': 'INGENIERIA AGRICOLA, FORESTAL Y AFINES',
    'DEPORTES, EDUCACI�N F�SICA Y RECREACI�N': 'DEPORTES, EDUCACION FISICA Y RECREACION',
    'INGENIER�A AMBIENTAL, SANITARIA Y AFINES': 'INGENIERIA AMBIENTAL, SANITARIA Y AFINES',
    'NUTRICI�N Y DIET�TICA': 'NUTRICION Y DIETETICA',
    'ANTROPOLOG�A O ARTES LIBERALES': 'ANTROPOLOGIA O ARTES LIBERALES',
    'LENGUAS MODERNAS, FILOLOG�A, LING��STICA Y AFINES': 'LENGUAS MODERNAS, FILOLOGIA, LINGUISTICA Y AFINES',
    'INGENIER�A AGROINDUSTRIAL, ALIMENTOS Y AFINES': 'INGENIERIA AGROINDUSTRIAL, ALIMENTOS Y AFINES',
    'M�SICA': 'MUSICA',
    'INGENIER�A BIOM�DICA Y AFINES': 'INGENIERIA BIOMEDICA Y AFINES',
    'QU�MICA Y AFINES': 'QUIMICA Y AFINES',
    'INGENIER�A DE PETR�LEOS': 'INGENIERIA DE PETROLEOS',
    'F�SICA': 'FISICA',
    'OPTOMETR�A': 'OPTOMETRIA',
    'INGENIER�A AGRON�MICA, PECUARIA Y AFINES': 'INGENIERIA AGRONOMICA, PECUARIA Y AFINES',
    'OTRAS INGENIER�AS': 'OTRAS INGENIERIAS',
    'FORMACI�N MILITAR': 'FORMACION MILITAR',
    'BIBLIOTECOLOG�A': 'BIBLIOTECOLOGIA',
    'TECNOLOG�AS DE LA INFORMACI�N Y LA COMUNICACI�N (TIC)': 'TECNOLOGIAS DE LA INFORMACION Y LA COMUNICACION (TIC)',
    'GEOGRAF�A O HISTORIA': 'GEOGRAFIA O HISTORIA',
    'EDUCACION FISICA Y RECREACION': 'EDUCACION FISICA Y RECREACION',
    'AVIACI�N': 'AVIACION'
}

remplasos_nivel = {
    'NO INDICA': 'NO REGISTRA',
    'PREGRADO - PROFESIONAL': 'PREGRADO',
    'PREGRADO PROFESIONAL': 'PREGRADO',
    'BACHILLERATO': 'BACHILLERATO',
    'POSTGRADO - ESPECIALIZACION': 'ESPECIALIZACION',
    'POSTGRADO - ESPECIALIZACI�N': 'ESPECIALIZACION',
    'NO REGISTRA': 'NO REGISTRA',
    'SIN PROFESION': 'SIN PROFESION',
    'SIN PROFESI�N': 'SIN PROFESION',
    'UNIVERSITARIO': 'PREGRADO',
    'TECNICA PROFESIONAL': 'TECNICO PROFESIONAL',
    'T�CNICA PROFESIONAL': 'TECNICO PROFESIONAL',
    'ESPECIALIZACI�N': 'ESPECIALIZACION',
    'TECNOLÓGICA': 'TECNICO PROFESIONAL',
    'TECNOL�GICA': 'TECNICO PROFESIONAL',
    'POSTGRADO POSTGRADO POSTGRADO POSTGRADO ESPECIALIZACION': 'ESPECIALIZACION',
    'POSTGRADO POSTGRADO POSTGRADO POSTGRADO POSTGRADO MAESTRIA': 'MAESTRIA',
    'POSTGRADO POSTGRADO POSTGRADO POSTGRADO POSTGRADO DOCTORADO': 'DOCTORADO',
    'POSTGRADO POSTGRADO POSTGRADO POSTGRADO MAESTRIA': 'MAESTRIA',
    'POSTGRADO POSTGRADO POSTGRADO POSTGRADO DOCTORADO': 'DOCTORADO',
    '(NO REGISTRA)': 'NO REGISTRA',
    'SIN PROFESION':'NO REGISTRA',
    'NO INDICA':'NO REGISTRA',
    '(NINGUNO)':'NO REGISTRA'
}

# APLICAR REEMPLAZOS
df['Nivel Académico'] = df['Nivel Académico'].replace(remplasos_nivel, regex=True)
df['Área Conocimiento'] = df['Área Conocimiento'].replace(remplasos_area, regex=True)
df['Sub Area Conocimiento'] = df['Sub Area Conocimiento'].replace(remplazos_subarea, regex=True)

# ============================  
# LIMPIEZA  
# ============================  

df[['pais de origen', 'departamento de origen', 'Ciudad de Nacimiento']] = df['Ciudad de Nacimiento'].str.split('/', expand=True)
df = df[df['pais de origen'] == 'COLOMBIA']

df[['Ciudad de residencia', 'Estado de residencia']] = df['Ciudad de Residencia'].str.split('/', expand=True)
df[['Año de Registro', 'Hora de Registro']] = df['Fecha de Registro'].str.split('-', expand=True)

df['Etnia de la persona'] = df['Etnia de la persona'].replace('IND�GENA', 'INDIGENA')
df = df[df['Año de Registro'] != '1900']

df = df.drop(columns=[
    'Código ISO país', 'Oficina de registro', 'Hora de Registro', 'Cantidad de personas',
    'Estado civil', 'Edad (años)', 'Estatura (CM)', 'Localización',
    'Fecha de Registro', 'Ciudad de Residencia'
])

Df_final = df.copy()

# =====================================
# VARIABLES PARA MÉTRICAS
# =====================================

variables = Df_final.shape[1]
filas = Df_final.shape[0]
paises = Df_final['País'].nunique()
list_paises = Df_final['País'].unique().tolist()
numero_etnias = Df_final['Etnia de la persona'].nunique()
list_areas = Df_final['Área Conocimiento'].dropna().unique().tolist()

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

with st.container(border=True):
    st.html('<font size=5><font color=#3D6E85>Migrantes por grupo de edad en cada país</font>')

    pais_selec = st.selectbox('Selecciona un país:', list_paises)

    df_edad = Df_final.groupby(['País', 'Grupo edad']).size().unstack().T.fillna(0)
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
# SUBÁREA DE CONOCIMIENTO
# ============================

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
    st.markdown('## Navegación')
    st.markdown('- [Acerca del Dataset](#)')
    st.markdown('- Top 5 departamentos con migrantes')
    st.markdown('- Migrantes por grupo de edad')
    st.markdown('- Subárea de conocimiento')
    st.markdown('- Registros por año')
    st.markdown('- Nivel académico por género')
    st.markdown('- Distribución por país')
    st.caption('jarmando.canas@udea.edu.co - mariana.trujillo2@udea.edu.co')
# ============================
    