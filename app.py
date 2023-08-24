import streamlit as st
from calculadoras import prescricao_punitiva, prescricao_retroativa, prescricao_executoria
from painel.controle_caso import evidencias

st.set_page_config(
    page_title="Usar PyGWalker no Streamlit",
    layout="wide"
)



st.header('Calculadoras')
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Intro", "Prescrição Punitiva",
                                  "Prescrição Retroativa",
                                  "Prescrição Executória", "Visualizador"])

with tab1:
    st.title("Boas Vindas!")
    st.write("""Disponibilizamos ferramentas úteis ao trabalho do Ministério Público na esfera criminal!""")
    st.write("""O objetivo deste espaço é tornar mais eficiente a persecução penal, por meio de 
                tecnologias que auxliem o trabalho dos membros do Parquet.""")
    st.write(
        "Objetivando imprimir celeridade aos trabalhos, iniciamos por desenvolver calculadoras de prescrição para análise dos processos penais.")
    st.write("Sugestões e ajustes podem ser feitas pelo e-mail: rafaelgalvaorn@hotmail.com")


with tab2:
    submenu = st.radio("",
                       ["Escolha o tipo de calculadora de prescrição punitiva", "Rito Ordinário", "Rito Tributário", "Rito do Júri"], index=0)

    if submenu == "Rito Ordinário":
        prescricao_punitiva.calc_prescricao_punitiva()
    elif submenu == "Rito Tributário":
        prescricao_punitiva.calc_prescricao_punitiva_tributaria()

    elif submenu == "Rito do Júri":
        prescricao_punitiva.calc_prescricao_punitiva_juri()

with tab3:
    prescricao_retroativa.calc_prescricao_retroativa()


with tab4:
    prescricao_executoria.calc_prescricao_executoria()

with tab5:
    evidencias()
