import streamlit as st


def boas_vindas():
    st.title("Boas Vindas!")
    st.markdown("""Disponibilizamos ferramentas úteis ao trabalho do Ministério Público na esfera criminal!""")
    st.markdown("""O objetivo deste espaço é tornar mais eficiente a persecução penal, por meio de 
                    tecnologias que auxliem o trabalho dos membros do Parquet.""")
    st.markdown(
        "Objetivando imprimir celeridade aos trabalhos, iniciamos por desenvolver calculadoras de prescrição para análise dos processos penais.")
    st.markdown("Sugestões e ajustes podem ser feitas pelo e-mail: rafaelgalvaorn@hotmail.com")
    st.markdown("")
    st.markdown("")
    st.markdown("")


def atualizacoes():
    st.subheader("Atualizações 🚀")  # Adicionando emoji para dar destaque
    st.markdown("---")  # Linha horizontal para separar o conteúdo

    # Estilizando a data com negrito
    st.markdown("**21/09/2023**")
    # Adicionando bullet point manualmente para destaque
    st.markdown(
        "- Verificação se a data do fato foi após 05/05/2010, na calculadora da prescrição retroativa, de modo a vedar a análise da prescrição pela pena in concreto entre a data do fato e a data do recebimento da denúncia.")
    # Você pode continuar adicionando outras atualizações da mesma forma

    st.markdown("---")  # Outra linha horizontal