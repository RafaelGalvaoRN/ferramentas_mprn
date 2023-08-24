import streamlit as st
import pygwalker as pyg
import pandas as pd

import streamlit.components.v1 as components



def evidencias():


    # Adicionar título
    st.title("Análise de Evidências")

    uploaded_file = st.file_uploader("Selecione um arquivo Excel", type=['xlsx'])

    if uploaded_file:
        df = pd.read_excel(uploaded_file)

        # Preenchendo os valores NaN usando o método forward fill
        df_filled = df.fillna(method='ffill')

        # Gerar o HTML usando o PyGWalker
        pyg_html = pyg.walk(df_filled, return_html=True)

        # Incorporar o HTML no aplicativo Streamlit
        components.html(pyg_html, height=1000, scrolling=True)
    else:
        st.write("Por favor, faça o upload de um arquivo Excel.")



