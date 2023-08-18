import streamlit as st
import dicionario_legislacao
import utilidades
from utilidades import *
from datetime import datetime, timedelta, date
import copy
import inspect
import dicionario_legislacao as dl

def calc_prescricao_executoria():
    st.title("Calculadora de Prescrição Executória")

    dic_execucao = {}
    data_prescricao_final = 0

    processo = st.text_input(label='Processo', key='processo_executoria', max_chars=30)
    dic_execucao['Nº do Processo'] = processo
    reu = st.text_input(label='Réu', key='reu_executoria', max_chars=30)
    dic_execucao['Réu'] = reu

    st.write("Escolha a Pena definitiva")

    # Criação de colunas
    col1, col2 = st.columns(2)

    # Adicionando widgets em colunas específicas
    with col1:
        ano_pena = st.number_input('Ano', key='ano_pena_executoria', min_value=0, max_value=200, value=0, step=1)

    with col2:
        mes_pena = st.number_input('Mês', key='mes_pena_executoria', min_value=0, max_value=12, value=0, step=1)

    dic_execucao['Pena in concreto (anos, meses)'] = (ano_pena, mes_pena)

    dic_execucao['Prazo prescricional'] = calcula_tempo_prescricao_retroativa(
        dic_execucao['Pena in concreto (anos, meses)'])

    verificar_detracao = st.checkbox('Decotar tempo de pena a título de detração?', key="verificacao_detração")
    dic_execucao['Decotar tempo de pena a título de detração?'] = verificar_detracao

    if verificar_detracao:
        col1, col2 = st.columns(2)

        with col1:
            ano_pena_detracao = st.number_input('Ano', key='ano_pena_detracao_executoria', min_value=0, max_value=200,
                                                value=0, step=1)

        with col2:
            mes_pena_detracao = st.number_input('Mês', key='mes_pena_detracao_executoria', min_value=0, max_value=12,
                                                value=0, step=1)

        dic_execucao['Tempo de detração (anos, meses)'] = ano_pena_detracao, mes_pena_detracao

        dic_execucao['Pena in concreto com a detração (anos, meses)'] = calcula_decote_detratacao(
            dic_execucao['Pena in concreto (anos, meses)'],

            dic_execucao['Tempo de detração (anos, meses)'])

        dic_execucao['Prazo prescricional'] = calcula_tempo_prescricao_retroativa(
            dic_execucao['Pena in concreto com a detração (anos, meses)'])

    data_minima = datetime.today() - timedelta(days=20 * 365)

    # Agora você pode usar 'data_minima' como o valor de 'min_value'
    data_termo_inicial_prescricao = st.date_input('Termo Inicial da Contagem',
                                                  key="termo_inicial_contagem",
                                                  value=None, format="DD/MM/YYYY",
                                                  min_value=data_minima,
                                                  help='O termo inicial da contagem do prazo da prescrição da pretensão executória é o trânsito em julgado para ambas as partes. STJ. 3ª Seção. AgRg no REsp 1.983.259-PR, Rel. Min. Sebastião Reis Júnior, julgado 26/10/2022 (Info 755)'
                                                       'Art. 113 - No caso de evadir-se o condenado ou de revogar-se o livramento condicional, a prescrição é regulada pelo tempo que resta da pena.')

    dic_execucao['Termo Inicial da Prescrição'] = data_termo_inicial_prescricao

    verificacao_idade = st.checkbox('Verificar Idade do Autor', key="verificacao_idade_executoria",
                                    help='Art. 115 - São reduzidos de metade os prazos de prescrição quando o criminoso era, '
                                         'ao tempo do crime, menor de 21 (vinte e um) anos, ou, na data da sentença, '
                                         'maior de 70 (setenta) anos.')
    dic_execucao['Houve verificação da idade do autor?'] = verificacao_idade

    if verificacao_idade:
        # Calcule a data de 90 anos atrás
        data_minima = datetime.today() - timedelta(days=100 * 365)

        # Agora você pode usar 'data_minima' como o valor de 'min_value'
        dt_nascimento_autor_executoria = st.date_input('Data de nascimento do Autor do fato',
                                                       key="idade_autor_executoria",
                                                       value=None, format="DD/MM/YYYY",
                                                       min_value=data_minima)

        dic_execucao['Data de nascimento do autor'] = dt_nascimento_autor_executoria

        dt_fatos_executoria = st.date_input("Data dos fatos", key="data_fatos_executoria", value=None,
                                            format="DD/MM/YYYY",
                                            min_value=data_minima, )

        dic_execucao[
            'Autor é menor de 21 anos na data dos fatos?'] = utilidades.calcula_se_e_menor_21_tempo_crime(
            dt_nascimento_autor_executoria, dt_fatos_executoria)

        dic_execucao['Idade do autor na data dos fatos:'] = utilidades.calcular_idade_na_data(
            dt_nascimento_autor_executoria, dt_fatos_executoria)

        dt_sentenca_executoria = st.date_input("Data da sentença", key="data_sentença_executoria", value=None,
                                               format="DD/MM/YYYY",
                                               min_value=data_minima, )

        dic_execucao[
            'Autor é maior de 70 anos na sentença?'] = utilidades.calcula_se_e_maior_de_setenta_anos_na_sentenca(
            dt_nascimento_autor_executoria, dt_sentenca_executoria)

        dic_execucao['Idade do autor na data da sentença:'] = utilidades.calcular_idade_na_data(
            dt_nascimento_autor_executoria, dt_sentenca_executoria)

        dic_execucao[
            'Autor é maior de 70 anos na presente data?'] = utilidades.calcula_se_e_maior_de_setenta_anos(
            dt_nascimento_autor_executoria)

        dic_execucao[
            'Idade do autor na presente data?'] = utilidades.calcular_idade_na_data(dt_nascimento_autor_executoria,

                                                                                    datetime.today())

    verificar_reincidencia = st.checkbox('Réu reincidente?', key="verificacao_reincidencia",
                                         help="Art. 110 - A prescrição depois de transitar em julgado a sentença condenatória regula-se pela pena aplicada e verifica-se nos prazos fixados no artigo anterior, os quais se aumentam de um terço, se o condenado é reincidente.")
    dic_execucao['Réu reincidente?'] = verificar_reincidencia

    if verificar_reincidencia:
        prazo_prescricao_com_reincidencia = dic_execucao[
            'Prazo prescricional com reincidência (anos, meses)'] = calcula_aumento_prazo_prescricao_reincidencia(
            dic_execucao['Prazo prescricional'])

        if verificar_reincidencia and verificacao_idade:
            if dic_execucao[
                'Autor é menor de 21 anos na data dos fatos?'] or dic_execucao[
                'Autor é maior de 70 anos na sentença?']:
                dic_execucao[
                    'Prazo prescricional com reincidência pela metade em razão da idade do autor (anos, meses)'] = calcula_metade_tempo(
                    prazo_prescricao_com_reincidencia[0], prazo_prescricao_com_reincidencia[1]
                )

    dic_execucao['Data de prescrição'] = soma_ano_calcula_nova_prescricao(
        dic_execucao['Prazo prescricional'],
        dic_execucao['Termo Inicial da Prescrição'])

    dic_execucao['DATA DE PRESCRIÇÃO FINAL'] = dic_execucao['Data de prescrição']

    if verificacao_idade:

        if dic_execucao['Autor é menor de 21 anos na data dos fatos?'] or dic_execucao[
            'Autor é maior de 70 anos na sentença?']:

            dic_execucao[
                'Data de prescrição pela metade em razão da idade do autor'] = soma_ano_calcula_nova_prescricao(
                dic_execucao['Prazo prescricional'] / 2,
                dic_execucao['Termo Inicial da Prescrição'])

            if dic_execucao[
                'Data de prescrição pela metade em razão da idade do autor'] > dic_execucao['DATA DE PRESCRIÇÃO FINAL']:
                dic_execucao['DATA DE PRESCRIÇÃO FINAL'] = dic_execucao[
                    'Data de prescrição pela metade em razão da idade do autor']

    if verificar_reincidencia:
        dic_execucao['Data de prescrição acrescida de reincidência'] = soma_ano_mes_e_calcula_nova_prescricao(
            dic_execucao['Prazo prescricional com reincidência (anos, meses)'],
            dic_execucao['Termo Inicial da Prescrição'])

        if dic_execucao[
            'Data de prescrição acrescida de reincidência'] > dic_execucao['DATA DE PRESCRIÇÃO FINAL']:
            dic_execucao['DATA DE PRESCRIÇÃO FINAL'] = dic_execucao[
                'Data de prescrição acrescida de reincidência']

    if verificar_reincidencia and verificacao_idade:
        if dic_execucao['Autor é menor de 21 anos na data dos fatos?'] or dic_execucao[
            'Autor é maior de 70 anos na sentença?']:

            dic_execucao[
                'Data de prescrição acrescida de reincidência reduzida pela metade em razão da idade do autor'] = soma_ano_mes_e_calcula_nova_prescricao(
                dic_execucao[
                    'Prazo prescricional com reincidência pela metade em razão da idade do autor (anos, meses)'],
                dic_execucao['Termo Inicial da Prescrição'])

            if dic_execucao[
                'Data de prescrição acrescida de reincidência reduzida pela metade em razão da idade do autor'] > \
                    dic_execucao['DATA DE PRESCRIÇÃO FINAL']:
                dic_execucao['DATA DE PRESCRIÇÃO FINAL'] = dic_execucao[
                    'Data de prescrição acrescida de reincidência reduzida pela metade em razão da idade do autor']

    chave = dic_execucao.pop('DATA DE PRESCRIÇÃO FINAL')
    dic_execucao['DATA DE PRESCRIÇÃO FINAL'] = chave

    if st.button('Calcular', key='buttao_calcular_executoria'):
        # converte date objetc in string

        dic_executoria = {}
        for key, valor in dic_execucao.items():
            # Check if it's a date
            if isinstance(valor, date):
                dic_executoria[key] = valor.strftime('%d/%m/%Y')
            # Check if it's a boolean True or False
            elif valor is True:
                dic_executoria[key] = "Sim"
            elif valor is False:
                dic_executoria[key] = "Não"
            # Else, just assign the original value
            else:
                dic_executoria[key] = valor

        st.table(utilidades.converte_dic_dataframe_vertical(dic_executoria))

        if dic_execucao['DATA DE PRESCRIÇÃO FINAL'] > datetime.now().date():
            st.success('NÃO PRESCREVEU', icon="✅")
        else:
            st.error('PRESCREVEU', icon='🚫')

