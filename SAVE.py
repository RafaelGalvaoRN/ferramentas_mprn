import streamlit as st





def main():
    st.title("Boas Vindas")
    st.write("""Disponibilizamos ferramentas úteis ao trabalho do Ministério Público na esfera criminal!""")
    st.write("""O objetivo deste espaço é tornar mais eficiente a persecução penal, por meio de 
                tecnologias que auxliem o trabalho dos membros do Parquet.""")


def calculator():
    st.title("Calculadora Prescrição")

    with st.form(key='my_form', clear_on_submit=True):
        processo = st.text_input(label='Processo', max_chars=30)
        reu = st.text_input(label='Réu', max_chars=30)
        data_fato = st.date_input(label='Data do Fato', format="DD/MM/YYYY")
        legislacao = st.radio('Legislação', ['Código Penal', 'Lei Maria da Penha'])

        if legislacao == 'Código Penal':
            crimes = st.selectbox('Código ', ['Homicídio', 'Roubo'])

        else:
            crimes = st.selectbox('Crime', ['uga', 'aff'])

        recebimento_denuncia = st.checkbox('Recebimento da Denúncia')
        dt_denuncia = st.date_input('Data do recebimento da Denúncia', format="DD/MM/YYYY")
        suspensao_prescricao = st.checkbox('Suspensão da Prescrição')
        dt_inicio_suspensao = st.date_input('Data do Início da Suspensão', value=None, format="DD/MM/YYYY")
        dt_fim_suspensao = st.date_input('Data do Fim da Suspensão', value=None, format="DD/MM/YYYY")
        verificacao_idade = st.checkbox('Verificar Idade do Autor')
        idade_autor = st.date_input('Data de nascimento do Autor', value=None,  format="DD/MM/YYYY")
        submit_button = st.form_submit_button(label='Enviar')

        if submit_button:
            # O formulário foi submetido.
            # Agora você pode fazer algo com as entradas do usuário.
            # Aqui estamos apenas imprimindo-os como um exemplo.
            st.write(f'Processo: {processo}')
            st.write(f'Réu: {reu}')
            # ...


with st.sidebar:
    st.sidebar.header("MENU")
    inicio = st.sidebar.button("Inicio")
    calculadora = st.sidebar.button("Calculadora Prescrição")

if inicio:
    main()
if calculadora:
    calculator()



