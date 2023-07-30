import streamlit as st


def main():
    st.title("Boas Vindas")
    st.write("""Disponibilizamos ferramentas úteis ao trabalho do Ministério Público na esfera criminal!""")
    st.write("""O objetivo deste espaço é tornar mais eficiente a persecução penal, por meio de 
                tecnologias que auxliem o trabalho dos membros do Parquet.""")


def calculator():
    st.title("Calculadora Prescrição")

    with st.form(key='my_form', clear_on_submit=True):
        processo = st.text_input(label='Processo')
        reu = st.text_input(label='Réu')
        data_fato = st.date_input(label='Data do Fato', format="DD/MM/YYYY")
        legislacao = st.selectbox('Legislação', ['', 'Código Penal', 'Lei Maria da Penha'])
        crimes = st.selectbox('Crimes', ['Homicídio', 'Roubo'])
        recebimento_denuncia = st.checkbox('Recebimento da Denúncia')
        dt_denuncia = st.date_input('Data da Denúncia', format="DD/MM/YYYY")
        suspensao_prescricao = st.checkbox('Suspensão da Prescrição')
        dt_inicio_suspensao = st.date_input('Data do Início da Suspensão', value=None, format="DD/MM/YYYY")
        dt_fim_suspensao = st.date_input('Data do Fim da Suspensão', value=None, format="DD/MM/YYYY")
        verificacao_idade = st.checkbox('Verificar Idade do Autor')
        idade_autor = st.date_input('Data para Verificar Idade do Autor', value=None,  format="DD/MM/YYYY")
        submit_button = st.form_submit_button(label='Enviar')


with st.sidebar:
    inicio = st.sidebar.button("Inicio")
    calculadora = st.sidebar.button("Calculadora Prescrição")

if inicio:
    main()
if calculadora:
    calculator()
