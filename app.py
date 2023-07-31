import streamlit as st
import dicionario_prescricao
import utilidades
from datetime import datetime, timedelta



tab1, tab2, tab3 = st.tabs(["Introdução", "Calculadora", "Em construção"])


with tab1:
    st.title("Boas Vindas!")
    st.write("""Disponibilizamos ferramentas úteis ao trabalho do Ministério Público na esfera criminal!""")
    st.write("""O objetivo deste espaço é tornar mais eficiente a persecução penal, por meio de 
                tecnologias que auxliem o trabalho dos membros do Parquet.""")


with tab2:
    st.title("Calculadora Prescrição")


    dicionario_final = {}

    processo = st.text_input(label='Processo', max_chars=30)
    reu = st.text_input(label='Réu', max_chars=30)

    data_minima = datetime.today() - timedelta(days=60 * 365)
    data_fato = st.date_input(label='Data do Fato', value=None, format="DD/MM/YYYY", min_value=data_minima)
    dicionario_final['data_fato'] = data_fato

    legislacao = st.radio('Legislação', ['Código Penal', 'Lei Maria da Penha', 'Lei 11.343/06 - Lei de Drogas'])

    if legislacao == 'Código Penal':

        crimes = [crime for crime in dicionario_prescricao.dic_prescricao.keys() ]
        crimes_ordenados = sorted(crimes)
        tipo_penal = st.selectbox('Código ', crimes_ordenados)
        dicionario_final['crime'] = tipo_penal

    elif legislacao == 'Lei Maria da Penha':
        crimes = [ crime for crime in dicionario_prescricao.dic_prescricao_maria.keys()]
        tipo_penal = st.selectbox('Crime', crimes)
        dicionario_final['crime'] = tipo_penal

    elif legislacao == 'Lei 11.343/06 - Lei de Drogas':
        crimes = [ crime for crime in dicionario_prescricao.dic_trafico.keys()]
        tipo_penal = st.selectbox('Crime', crimes)
        dicionario_final['crime'] = tipo_penal

    recebimento_denuncia = st.checkbox('Recebimento da Denúncia')
    dicionario_final['recebimento_denuncia_bool'] = recebimento_denuncia


    if recebimento_denuncia:
        data_minima = datetime.today() - timedelta(days=30 * 365)

        dt_denuncia = st.date_input('Data do recebimento da Denúncia', format="DD/MM/YYYY", min_value=data_minima)
        dicionario_final['Dt_Denuncia'] = dt_denuncia

    suspensao_prescricao = st.checkbox('Suspensão da Prescrição')
    dicionario_final['suspensao_prescricao_bool'] = suspensao_prescricao

    if suspensao_prescricao:
        data_minima = datetime.today() - timedelta(days=30 * 365)

        dt_inicio_suspensao = st.date_input('Data do Início da Suspensão', value=None, format="DD/MM/YYYY", min_value=data_minima)
        dt_fim_suspensao = st.date_input('Data do Fim da Suspensão', value=None, format="DD/MM/YYYY", min_value=data_minima)

        dicionario_final['Dt_inicio_suspensao'] = dt_inicio_suspensao
        dicionario_final['Dt_fim_suspensao'] = dt_fim_suspensao



    verificacao_idade = st.checkbox('Verificar Idade do Autor')
    dicionario_final['verificacao_idade'] = verificacao_idade

    if verificacao_idade:
        # Calcule a data de 90 anos atrás
        data_minima = datetime.today() - timedelta(days=100 * 365)

        # Agora você pode usar 'data_minima' como o valor de 'min_value'
        idade_autor = st.date_input('Data de nascimento do Autor', value=None, format="DD/MM/YYYY",
                                    min_value=data_minima)

        dicionario_final['idade_autor'] = idade_autor
        dicionario_final['verificacao_idade']: True


    if st.button('Calcular'):

        if  dicionario_final['suspensao_prescricao_bool']:

            if dicionario_final['Dt_inicio_suspensao'] > dicionario_final['Dt_fim_suspensao']:
                st.error('Data do início da suspensão não pode ser posterior à Data do fim da suspensão', icon="🚫")

            elif dicionario_final['Dt_inicio_suspensao'] > dicionario_final['Dt_fim_suspensao']:
                st.error('Data do início da suspensão não pode ser posterior à Data do fim da suspensão', icon="🚫")

            elif dicionario_final['Dt_inicio_suspensao'] < dicionario_final['Dt_Denuncia']:
                st.error('Data do início da suspensão não pode ser anterior à Data do recebimento da Denúncia', icon="🚫")

            elif dicionario_final['Dt_fim_suspensao'] < dicionario_final['Dt_Denuncia']:
                st.error('Data do fim da suspensão não pode ser anterior à Data do recebimento da Denúncia', icon="🚫")

            elif dicionario_final['Dt_inicio_suspensao'] < dicionario_final['data_fato']:
                st.error('Data do início da suspensão não pode ser anterior à Data do Fato', icon="🚫")

            elif dicionario_final['Dt_fim_suspensao'] < dicionario_final['data_fato']:
                st.error('Data do fim da suspensão não pode ser anterior à Data do Fato', icon="🚫")


        if  dicionario_final['verificacao_idade']:
            if dicionario_final['idade_autor'] > dicionario_final['data_fato']:
                st.error('Data de nascimento do autor do fato não pode ser posterior à data do fato', icon="🚫")

            if dicionario_final['suspensao_prescricao_bool']:

                if dicionario_final['idade_autor'] > dicionario_final['Dt_inicio_suspensao']:
                    st.error(
                        'Data de nascimento do autor do fato não pode ser posterior à data do início da suspensão do prazo prescricional',
                        icon="🚫")

                elif dicionario_final['idade_autor'] > dicionario_final['Dt_fim_suspensao']:
                    st.error(
                        'Data de nascimento do autor do fato não pode ser posterior à data do fim da suspensão do prazo prescricional',
                        icon="🚫")

        if dicionario_final['recebimento_denuncia_bool']:
            if  dicionario_final['verificacao_idade']:
                if dicionario_final['idade_autor'] > dicionario_final['Dt_Denuncia']:
                    st.error('Data de nascimento do autor do fato não pode ser posterior à data de recebimento da denúncia', icon="🚫")

            if dicionario_final['data_fato'] > dicionario_final['Dt_Denuncia']:
                st.error('Data do Fato não pode ser posterior à Data do recebimento da Denúncia', icon="🚫")


        st.header('Dados informados')

        st.table(utilidades.converte_dic_dataframe_vertical(dicionario_final))


        dic_resultado, parecer = utilidades.analisa_prescricao(dicionario_final)

        st.header('Dados calculados')

        st.table(utilidades.converte_dic_dataframe_vertical(dic_resultado))

        st.header('Parecer')

        st.write(parecer)











