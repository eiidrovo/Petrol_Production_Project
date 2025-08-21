import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import pandas as pd
import plotly.express as px
import numpy as np
from utilities import IPR_Curve,IPR_curve_methods
import matplotlib.pyplot as plt

def production_plots():
    file = st.file_uploader("Upload data to plot", type=["xlsx"])
    if file is not None:
        Well_Data=pd.read_excel(file,sheet_name='Monthly Production Data',skiprows=[1])
        st.success("File Loaded!")
    else:
        st.success('Waiting For File')
        st.stop()
    

    Well_Data['date']=pd.to_datetime(Well_Data[['Year','Month']].assign(day=1))

    Selected_Well=st.selectbox(
        'Choose Well',
        options=Well_Data['Wellbore name'].unique()
    )
    fig = px.line(
        Well_Data[Well_Data['Wellbore name'] ==Selected_Well],
        x='date',
        y=['Oil','Water','Water'],
        labels={'value': 'Production', 'date': 'Time'},
        title='Productivity'
    )
    fig.update_layout(legend_title_text='Production [Sm3]')        
    st.plotly_chart(fig, use_container_width=True)

def ipr_interface():
    pr=st.number_input('Psia reservoir PR')
    pb=st.number_input('Psia bubble point')
    pwf_test=st.number_input('Psia test')
    q_test=st.number_input('stb/d test')
    subdivisions=st.number_input('subdivisions',max_value=1000,min_value=5,step=1,format="%d")
    pwf=np.linspace(pr,0,subdivisions)
    if not all([pr, pb, pwf_test, q_test]):
        st.stop()
    EF_validate = st.checkbox("EF1")
    ef1 = 1
    if EF_validate:
        ef1 = st.number_input(
            "Wrte the first EF value if known:",
            min_value=0.0,
            max_value=3.0,
            step=0.1
        )
    EF2_validate = st.checkbox("EF2")
    ef2 = None
    if EF2_validate:
        ef2 = st.number_input(
            "Write the second EF value if known:",
            min_value=0.0,
            max_value=3.0,
            step=0.1
        )
    if ef2==0:
        ef2=None

    method = st.selectbox(
        "Mthod to graph",
        ["Darcy", "Vogel", "IPR_compuesto","Standing","Using a function"]
    )
    if method == 'Using a function':
        IPR_Curve(q_test, pwf_test, pr, pwf, pb, ef1, ef2)
    else:
        IPR_curve_methods(q_test, pwf_test, pr, pwf, pb, method, ef1, ef2)

icon= Image.open('Resources/Logo.png')
st.set_page_config(page_title="Proyecto", page_icon=icon)
FIMCM_Logo = Image.open('Resources/FIMCM_logo.png')
FICT_Logo = Image.open('Resources/FICT_logo.png')


with st.sidebar:
    seleccion = option_menu(
        "Main Menu",
        ["Home","Production Plots", "IPR curves", "Nodal Analysis"],
        icons=["house", "bar-chart-line-fill", "graph-up-arrow","option"],
        menu_icon="list",
        default_index=0
    )
st.title(seleccion)

st.title("📊 Producción Petrolera")
st.write("""
         El siguiente programa fue desarrollado por Esaú Idrovo, estudiante de la carrera
         de Ingeniería Naval en FIMCM-ESPOL para la materia de Softwares en Ingeniería de
         Petróleo PETG1029 en FICT-ESPOL.
""")
st.image(FIMCM_Logo)
st.caption("FIMC - Facultad de Ing. Marítima y Ciencias del Mar")
st.image(FICT_Logo)
st.caption("FICT - Facultad de Ing. en Ciencias de la Tierra")

st.markdown('''
Este programa tiene las siguientes funcionalidades:

- Graficación de la producción de petróleo en el tiempo de distintos pozos del campo Volve
- Integra una calculadora para la estimación de parámetros de potencial de yacimiento y curvas IPR
- Ofrece herramientas de análisis Nodal
''')

def nodal():
    pr=st.number_input('reservoir PR, Psia')
    pb=st.number_input('bubble point, Psia')
    pthp = st.number_input('Pthp, Psia')
    Qt=st.number_input('Qt, bdp')
    pwtf=st.number_input('pwtf, Psia')
    TVD = st.number_input('TVD, ft')
    MD = st.number_input(' MD, ft')
    c = st.number_input('C')
    IdTubing = st.number_input('IdTubing, in')
    if not all([pr, pb, Qt, pwtf]):
        st.stop()
    IP=Qt/(pr-pwtf)
    Qmax=IP*pr
    st.success(f"Qmax = {Qmax}")

    wc =  st.number_input('Wc')
    sgh2o = st.number_input('Sgh2o')
    API = st.number_input('API')
    sgoil = 141.5/(API+131.5)
    st.success(f"Qmax = {sgoil}")
    sgav=wc*sgh2o+(1-wc)*sgoil
    sigmaav=sgav*0.433
    subdivisions = st.number_input('subdivisions', max_value=1000, min_value=5, step=1, format="%d")
    qbdp=np.linspace(0,Qmax,subdivisions)
    pwf=pr-qbdp/IP
    pgrav=sigmaav*TVD
    f=2.083*(100*qbdp/(34.3*c))**1.85*(1/IdTubing)**4.8655
    F=f*MD*0.001
    Pf=F*sigmaav
    Po=pthp+pgrav+Pf
    Psys=Po-pwf
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.set_xlabel('Qo(bpd)', fontsize=14)
    ax.set_ylabel('Pwf(psia)', fontsize=14)
    ax.set_title('Nodal Analysis', fontsize=18)
    ax.plot(qbdp,pwf,label='Pwf', color='r')
    ax.plot(qbdp, Po, label='Po', color='b')
    ax.plot(qbdp, Psys, label='Psys', color='g')
    ax.grid()
    st.pyplot(fig)
    

if seleccion=='Production Plots':
    production_plots()
elif seleccion=='IPR curves':
    ipr_interface()
elif seleccion == 'Nodal Analysis':
    nodal()
