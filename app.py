import streamlit as st
import dicionario_legislacao
import utilidades
from utilidades import *
from datetime import datetime, timedelta, date
import copy
import inspect
import dicionario_legislacao as dl

st.header('Calculadoras')
tab1, tab2, tab3, tab4 = st.tabs(["Intro", "Prescrição Punitiva",
                                  "Prescrição Retroativa",
                                  "Prescrição Executória"])

with tab1:
    st.title("Boas Vindas!")
    st.write("""Disponibilizamos ferramentas úteis ao trabalho do Ministério Público na esfera criminal!""")
    st.write("""O objetivo deste espaço é tornar mais eficiente a persecução penal, por meio de 
                tecnologias que auxliem o trabalho dos membros do Parquet.""")
    st.write(
        "Objetivando imprimir celeridade aos trabalhos, iniciamos por desenvolver calculadoras de prescrição para análise dos processos penais.")
    st.write("Sugestões e ajustes podem ser feitas pelo e-mail: rafaelgalvaorn@hotmail.com")

with tab2:
    st.title("Calculadora Prescrição")

    dicionario_final = {}

    processo = st.text_input(label='Processo', max_chars=30)
    reu = st.text_input(label='Réu', max_chars=30)

    data_minima = datetime.today() - timedelta(days=60 * 365)
    data_fato = st.date_input(label='Data do Fato', value=None, format="DD/MM/YYYY", min_value=data_minima,
                              help="Art. 111 - A prescrição, antes de transitar em julgado a sentença final, começa a correr: I - do dia em que o crime se consumou; II - no caso de tentativa, do dia em que cessou a atividade criminosa; III - nos crimes permanentes, do dia em que cessou a permanência; IV - nos de bigamia e nos de falsificação ou alteração de assentamento do registro civil, da data em que o fato se tornou conhecido. V - nos crimes contra a dignidade sexual ou que envolvam violência contra a criança e o adolescente, previstos neste Código ou em legislação especial, da data em que a vítima completar 18 (dezoito) anos, salvo se a esse tempo já houver sido proposta a ação penal.")

    dicionario_final['data_fato'] = data_fato

    legislacao = st.radio('Legislação', ['Código Penal', 'Lei Maria da Penha',
                                         'Lei 11.343/06 - Lei de Drogas',
                                         'Lei 10.826/03 - Estatuto do Desarmamento',
                                         "Decreto_Lei nº 3.688 - Lei das Contravenções Penais",
                                         "Lei 9.503/97 - Código de Trânsito Brasileiro",
                                         "Lei 9.605/98 - Lei de Crimes Ambientais"])

    if legislacao == 'Código Penal':

        crimes = [crime for crime in dicionario_legislacao.codigo_penal.keys()]
        crimes_ordenados = sorted(crimes)
        tipo_penal = st.selectbox('Tipo Penal', crimes_ordenados)
        dicionario_final['crime'] = tipo_penal

    elif legislacao == 'Lei Maria da Penha':
        crimes = [crime for crime in dicionario_legislacao.maria_da_penha.keys()]
        tipo_penal = st.selectbox('Tipo Penal', crimes)
        dicionario_final['crime'] = tipo_penal

    elif legislacao == 'Lei 11.343/06 - Lei de Drogas':
        crimes = [crime for crime in dicionario_legislacao.trafico.keys()]
        tipo_penal = st.selectbox('Tipo Penal', crimes)
        dicionario_final['crime'] = tipo_penal


    elif legislacao == 'Lei 10.826/03 - Estatuto do Desarmamento':
        crimes = [crime for crime in dicionario_legislacao.estatuto_desarmamento.keys()]
        tipo_penal = st.selectbox('Tipo Penal', crimes)
        dicionario_final['crime'] = tipo_penal

    elif legislacao == 'Decreto_Lei nº 3.688 - Lei das Contravenções Penais':
        crimes = [crime for crime in dicionario_legislacao.lcp.keys()]
        tipo_penal = st.selectbox('Tipo Penal', crimes)
        dicionario_final['crime'] = tipo_penal

    elif legislacao == 'Lei 9.503/97 - Código de Trânsito Brasileiro':
        crimes = [crime for crime in dicionario_legislacao.ctb.keys()]
        tipo_penal = st.selectbox('Tipo Penal', crimes)
        dicionario_final['crime'] = tipo_penal

    elif legislacao == 'Lei 9.605/98 - Lei de Crimes Ambientais':
        crimes = [crime for crime in dicionario_legislacao.ambiental.keys()]
        tipo_penal = st.selectbox('Tipo Penal', crimes)
        dicionario_final['crime'] = tipo_penal

    recebimento_denuncia = st.checkbox('Recebimento da Denúncia')
    dicionario_final['recebimento_denuncia_bool'] = recebimento_denuncia

    if recebimento_denuncia:
        data_minima = datetime.today() - timedelta(days=30 * 365)

        dt_denuncia = st.date_input('Data do recebimento da Denúncia', format="DD/MM/YYYY", min_value=data_minima,
                                    help='CP. Art. 117 - O curso da prescrição interrompe-se: I - pelo recebimento da denúncia ou da queixa;')

        dicionario_final['Dt_Denuncia'] = dt_denuncia

    suspensao_prescricao = st.checkbox('Suspensão da Prescrição')
    dicionario_final['suspensao_prescricao_bool'] = suspensao_prescricao

    if suspensao_prescricao:
        data_minima = datetime.today() - timedelta(days=30 * 365)

        dt_inicio_suspensao = st.date_input('Data do Início da Suspensão', value=None, format="DD/MM/YYYY",
                                            min_value=data_minima)
        dt_fim_suspensao = st.date_input('Data do Fim da Suspensão', value=None, format="DD/MM/YYYY",
                                         min_value=data_minima)

        dicionario_final['Dt_inicio_suspensao'] = dt_inicio_suspensao
        dicionario_final['Dt_fim_suspensao'] = dt_fim_suspensao

    verificacao_idade = st.checkbox('Verificar Idade do Autor',
                                    help='Art. 115 - São reduzidos de metade os prazos de prescrição quando o criminoso era, '
                                         'ao tempo do crime, menor de 21 (vinte e um) anos, ou, na data da sentença, '
                                         'maior de 70 (setenta) anos.')
    dicionario_final['verificacao_idade'] = verificacao_idade

    if verificacao_idade:
        # Calcule a data de 90 anos atrás
        data_minima = datetime.today() - timedelta(days=100 * 365)

        # Agora você pode usar 'data_minima' como o valor de 'min_value'
        idade_autor = st.date_input('Data de nascimento do Autor do fato', value=None, format="DD/MM/YYYY",
                                    min_value=data_minima)

        dicionario_final['idade_autor'] = idade_autor
        dicionario_final['verificacao_idade']: True

    if st.button('Calcular'):
        prosseguir = True

        if dicionario_final['suspensao_prescricao_bool']:
            if dicionario_final['Dt_inicio_suspensao'] > dicionario_final['Dt_fim_suspensao']:
                st.error('Data do início da suspensão não pode ser posterior à Data do fim da suspensão', icon="🚫")
                prosseguir = False

            if dicionario_final.get('Dt_Denuncia', False):
                if dicionario_final['Dt_inicio_suspensao'] < dicionario_final['Dt_Denuncia']:
                    st.error('Data do início da suspensão não pode ser anterior à Data do recebimento da Denúncia',
                             icon="🚫")
                    prosseguir = False


                elif dicionario_final['Dt_fim_suspensao'] < dicionario_final['Dt_Denuncia']:
                    st.error('Data do fim da suspensão não pode ser anterior à Data do recebimento da Denúncia',
                             icon="🚫")
                    prosseguir = False

            if dicionario_final['Dt_inicio_suspensao'] < dicionario_final['data_fato']:
                st.error('Data do início da suspensão não pode ser anterior à Data do Fato', icon="🚫")
                prosseguir = False


            elif dicionario_final['Dt_fim_suspensao'] < dicionario_final['data_fato']:
                st.error('Data do fim da suspensão não pode ser anterior à Data do Fato', icon="🚫")
                prosseguir = False

        if dicionario_final.get('verificacao_idade', False):
            if dicionario_final['idade_autor'] > dicionario_final['data_fato']:
                st.error('Data de nascimento do autor do fato não pode ser posterior à data do fato', icon="🚫")
                prosseguir = False

            if dicionario_final['suspensao_prescricao_bool']:

                if dicionario_final['idade_autor'] > dicionario_final['Dt_inicio_suspensao']:
                    st.error(
                        'Data de nascimento do autor do fato não pode ser posterior à data do início da suspensão do prazo prescricional',
                        icon="🚫")
                    prosseguir = False


                elif dicionario_final['idade_autor'] > dicionario_final['Dt_fim_suspensao']:
                    st.error(
                        'Data de nascimento do autor do fato não pode ser posterior à data do fim da suspensão do prazo prescricional',
                        icon="🚫")
                    prosseguir = False

        if dicionario_final.get('recebimento_denuncia_bool', False):
            if dicionario_final['verificacao_idade']:
                if dicionario_final['idade_autor'] > dicionario_final['Dt_Denuncia']:
                    st.error(
                        'Data de nascimento do autor do fato não pode ser posterior à data de recebimento da denúncia',
                        icon="🚫")
                    prosseguir = False

            if dicionario_final['data_fato'] > dicionario_final['Dt_Denuncia']:
                st.error('Data do Fato não pode ser posterior à Data do recebimento da Denúncia', icon="🚫")
                prosseguir = False

        if prosseguir:

            with st.expander("Dados informados"):

                # inicia campo dados informados
                st.header('Dados informados')
                # faz uma copia do dicionario para o novo dicionario
                dic_dados_informados = copy.deepcopy(dicionario_final)

                # pega idade do autor informada, para calcular idade do autor em outro campo do streamlit
                dt_nascimento_autor = dic_dados_informados.get('idade_autor', None)
                dt_fato = dic_dados_informados.get('data_fato', None)
                # corrige keys
                dic_dados_informados = utilidades.normaliza_key_dic_dados_informados(dic_dados_informados)
                # corrige values
                dic_dados_informados = utilidades.normaliza_value_dic_dados_informados(dic_dados_informados)
                # imprime tabela
                st.table(utilidades.converte_dic_dataframe_vertical(dic_dados_informados))

            # inicia campo dados calculados
            st.header('Dados calculados')

            # pega prescricao legal do crime, antes do dict original ser alterado
            prescricao_legal = utilidades.dic_prescricao[tipo_penal]

            # pega resultado e parecer gerado pela funcao analisa prescricao
            dic_resultado, parecer = utilidades.analisa_prescricao(dicionario_final, processo, reu)

            # adiciona prescriçao legal in abstracto no dicionário
            dic_resultado['Prescrição Legal in abstracto'] = prescricao_legal

            # adiciona data de nascimento e calculo da idade do autor no dic
            if dt_nascimento_autor:
                dic_resultado['Idade atual do autor (anos)'] = utilidades.calcular_idade(dt_nascimento_autor)

                dic_resultado['Idade do autor na data do fato (anos)'] = utilidades.calcular_idade_na_data(
                    dt_nascimento_autor,
                    dt_fato)

            dic_dados_informados = copy.deepcopy(dic_resultado)

            dic_dados_informados = utilidades.normaliza_key_dic_dados_calculados(dic_dados_informados)

            dic_dados_informados = utilidades.normaliza_value_dic_dados_calculados(dic_dados_informados)

            st.table(utilidades.converte_dic_dataframe_vertical(dic_dados_informados))

            if dic_dados_informados['Crime prescreveu?'] == 'Não':
                st.success("NÃO PRESCREVEU", icon="✅")
            elif dic_dados_informados['Crime prescreveu?'] == 'Sim':
                st.error("PRESCREVEU", icon="🚫")

            with st.expander('Parecer'):
                st.header('Parecer')
                st.write(parecer)

with tab3:
    st.title("Calculadora de Prescrição Retroativa")

    dicionario_retroativa = {}

    processo = st.text_input(label='Processo', key='processo', max_chars=30)
    dicionario_retroativa['Nº do Processo'] = processo
    reu = st.text_input(label='Réu', key='reu', max_chars=30)
    dicionario_retroativa['Réu'] = reu

    st.write("Escolha a Pena estabelecida na sentença")

    # Criação de colunas
    col1, col2 = st.columns(2)

    # Adicionando widgets em colunas específicas
    with col1:
        ano_pena = st.number_input('Ano', min_value=0, max_value=200, value=0, step=1)

    with col2:
        mes_pena = st.number_input('Mês', min_value=0, max_value=12, value=0, step=1)

    dicionario_retroativa['Pena in concreto (anos, meses)'] = (ano_pena, mes_pena)

    data_fato_retroativa = st.date_input(label='Data do Fato', format="DD/MM/YYYY", min_value=data_minima,
                                         key="data_fato_retroativa",
                                         help="Art. 111 - A prescrição, antes de transitar em julgado a sentença final, começa a correr: I - do dia em que o crime se consumou; II - no caso de tentativa, do dia em que cessou a atividade criminosa; III - nos crimes permanentes, do dia em que cessou a permanência; IV - nos de bigamia e nos de falsificação ou alteração de assentamento do registro civil, da data em que o fato se tornou conhecido. V - nos crimes contra a dignidade sexual ou que envolvam violência contra a criança e o adolescente, previstos neste Código ou em legislação especial, da data em que a vítima completar 18 (dezoito) anos, salvo se a esse tempo já houver sido proposta a ação penal.")

    dicionario_retroativa['Data do fato'] = data_fato_retroativa

    dt_denuncia_retroativa = st.date_input('Data do recebimento da Denúncia', key="dt_denuncia_retroativa",
                                           format="DD/MM/YYYY", min_value=data_minima,
                                           help='CP. Art. 117 - O curso da prescrição interrompe-se: I - pelo recebimento da denúncia ou da queixa;')

    dicionario_retroativa['Data da Denúncia'] = dt_denuncia_retroativa

    verificar_rito_juri = st.checkbox('Analisar prescrição no rito do Júri?', key="verificacao_rito_juri")
    dicionario_retroativa['Processo submetido ao rito do Júri?'] = verificar_rito_juri

    if verificar_rito_juri:
        # Calcule a data de 20 anos atrás
        data_minima = datetime.today() - timedelta(days=20 * 365)

        # Agora você pode usar 'data_minima' como o valor de 'min_value'
        data_pronuncia = st.date_input('Data da Pronúncia',
                                       key="data_pronuncia",
                                       value=None, format="DD/MM/YYYY",
                                       min_value=data_minima,
                                       help='Art. 117 - O curso da prescrição interrompe-se: (...) II - pela pronúncia;')

        data_decisao_confirmatoria_pronuncia = st.date_input('Data da decisão confirmatória da Pronúncia',
                                                             key="data_decisaao_confirmatoria_pronuncia",
                                                             value=None, format="DD/MM/YYYY",
                                                             min_value=data_minima,
                                                             help='Art. 117 - O curso da prescrição interrompe-se: (...) III - pela decisão confirmatória da pronúncia;')

        dicionario_retroativa['Data da pronúncia'] = data_pronuncia
        dicionario_retroativa['Data da decisão confirmatória de pronúncia'] = data_decisao_confirmatoria_pronuncia

        dt_recebimento_denuncia_x_dt_pronuncia = utilidades.calcula_diferenca_entre_duas_datas(
            dt_denuncia_retroativa, data_pronuncia)

        dt_pronuncia_x_dt_decisao_confirmatoria_pronuncia = utilidades.calcula_diferenca_entre_duas_datas(
            data_pronuncia, data_decisao_confirmatoria_pronuncia)

    dt_sentenca = st.date_input('Data da sentença', key="dt_sentenca",
                                format="DD/MM/YYYY", min_value=data_minima)

    dicionario_retroativa['Data da Sentença'] = dt_sentenca

    suspensao_prescricao = st.checkbox('Suspensão da Prescrição', key='suspensao_prescricao_retroativa')
    dicionario_retroativa['Suspensão da Prescrição?'] = suspensao_prescricao

    dicionario_retroativa['Período de Suspensão (dias)'] = timedelta(days=0).days

    tempo_suspensao_dias = 0
    if suspensao_prescricao:
        data_minima = datetime.today() - timedelta(days=30 * 365)

        dt_inicio_suspensao_retroativa = st.date_input('Data do Início da Suspensão',
                                                       key="dt_inicio_suspensao_retroativa", value=None,
                                                       format="DD/MM/YYYY",
                                                       min_value=data_minima)
        dt_fim_suspensao_retroativa = st.date_input('Data do Fim da Suspensão', key="dt_fim_suspensao_retroativa",
                                                    value=None, format="DD/MM/YYYY",
                                                    min_value=data_minima)

        dicionario_retroativa['Data de Início da Suspensão'] = dt_inicio_suspensao_retroativa
        dicionario_retroativa['Data de Fim da Suspensão'] = dt_fim_suspensao_retroativa

        tempo_suspensao_dias = dicionario_retroativa['Data de Fim da Suspensão'] - dicionario_retroativa[
            'Data de Início da Suspensão']
        dicionario_retroativa['Qtd de dias de suspensão do processo'] = tempo_suspensao_dias.days
        dicionario_retroativa['Período de Suspensão (dias)'] = (
                dt_fim_suspensao_retroativa - dt_inicio_suspensao_retroativa).days

    verificacao_idade = st.checkbox('Verificar Idade do Autor', key="verificacao_idade_retroativa",
                                    help='Art. 115 - São reduzidos de metade os prazos de prescrição quando o criminoso era, '
                                         'ao tempo do crime, menor de 21 (vinte e um) anos, ou, na data da sentença, '
                                         'maior de 70 (setenta) anos.')
    dicionario_retroativa['Houve verificação da idade do autor?'] = verificacao_idade

    if verificacao_idade:
        # Calcule a data de 90 anos atrás
        data_minima = datetime.today() - timedelta(days=100 * 365)

        # Agora você pode usar 'data_minima' como o valor de 'min_value'
        dt_nascimento_autor_retroativa = st.date_input('Data de nascimento do Autor do fato',
                                                       key="idade_autor_retroativa",
                                                       value=None, format="DD/MM/YYYY",
                                                       min_value=data_minima
                                                       )

        dicionario_retroativa['Data de nascimento do autor'] = dt_nascimento_autor_retroativa

        dicionario_retroativa[
            'Autor é menor de 21 anos na data dos fatos?'] = utilidades.calcula_se_e_menor_21_tempo_crime(
            dt_nascimento_autor_retroativa, data_fato_retroativa)

        dicionario_retroativa['Idade do autor na data dos fatos:'] = utilidades.calcular_idade_na_data(
            dt_nascimento_autor_retroativa, data_fato_retroativa)

        dicionario_retroativa[
            'Autor é maior de 70 anos na sentença?'] = utilidades.calcula_se_e_maior_de_setenta_anos_na_sentenca(
            dt_nascimento_autor_retroativa, dt_sentenca)

        dicionario_retroativa['Idade do autor na data da sentença:'] = utilidades.calcular_idade_na_data(
            dt_nascimento_autor_retroativa, dt_sentenca)

        dicionario_retroativa[
            'Autor é maior de 70 anos na presente data?'] = utilidades.calcula_se_e_maior_de_setenta_anos(
            dt_nascimento_autor_retroativa)

        dicionario_retroativa[
            'Idade do autor na presente data?'] = utilidades.calcular_idade_na_data(dt_nascimento_autor_retroativa,
                                                                                    datetime.today())

    verificar_data_acordao = st.checkbox('Analisar prescrição entre a data da sentença e a data do Acórdão',
                                         key="verificacao_data_acordao")
    dicionario_retroativa['Houve verificação da data do Acórdão?'] = verificar_data_acordao

    if verificar_data_acordao:
        # Calcule a data de 20 anos atrás
        data_minima = datetime.today() - timedelta(days=20 * 365)

        # Agora você pode usar 'data_minima' como o valor de 'min_value'
        data_acordao = st.date_input('Data do Acórdão',
                                     key="data_acórdão",
                                     value=None, format="DD/MM/YYYY",
                                     min_value=data_minima,
                                     help='Art. 117 - O curso da prescrição interrompe-se: (...) IV - pela publicação da sentença ou acórdão condenatórios recorríveis;')

        dicionario_retroativa['Data do Acórdão condenatório recorrível'] = data_acordao

        dt_sentenca_x_dt_acordao = utilidades.calcula_diferenca_entre_duas_datas(dt_sentenca, data_acordao)
        dicionario_retroativa[
            'Decurso do prazo entre a data da sentença e a data do Acórdão'] = utilidades.calcula_diferenca_entre_duas_datas_em_anos_meses_dias(
            dt_sentenca, data_acordao)

    if st.button('Calcular', key='buttao_calcular_retroativa'):
        continuar = True

        if data_fato_retroativa > dt_denuncia_retroativa:
            st.error("Data de recebimento da denúncia não pode ser inferior a data do fato")
            continuar = False

        if data_fato_retroativa > dt_sentenca:
            st.error("Data do fato não pode ser posterior a data do fato")
            continuar = False

        if dt_denuncia_retroativa > dt_sentenca:
            st.error("Data de recebimento da denúncia  não pode ser inferior a data do fato")
            continuar = False

        if suspensao_prescricao:
            if dt_inicio_suspensao_retroativa > dt_fim_suspensao_retroativa:
                st.error("Data de início da suspensão não pode ser posterior à data final da suspensão da prescrição")
                continuar = False

        if verificar_data_acordao:
            if data_acordao < data_fato_retroativa:
                st.error("Data do Acórdão não pode ser anterior à data do fato")
                continuar = False

            if data_acordao < dt_denuncia_retroativa:
                st.error("Data do Acórdão não pode ser anterior à data do recebimento da denúncia")
                continuar = False

            if data_acordao < dt_sentenca:
                st.error("Data do Acórdão não pode ser anterior à data da sentença")
                continuar = False

            if suspensao_prescricao:
                if data_acordao <= dt_inicio_suspensao_retroativa:
                    st.error("Data do Acórdão não pode ser anterior à data de início da suspensão da prescrição")
                    continuar = False

                if data_acordao <= dt_fim_suspensao_retroativa:
                    st.error("Data do Acórdão não pode ser anterior à data de fim da suspensão da prescrição")
                    continuar = False

        if verificar_rito_juri:
            if data_pronuncia < data_fato_retroativa:
                st.error("Data da pronúncia não pode ser anterior à data do fato")
                continuar = False

            if data_pronuncia < dt_denuncia_retroativa:
                st.error("Data da pronúncia não pode ser anterior à data do recebimento da denúncia")
                continuar = False

            if data_pronuncia > dt_sentenca:
                st.error("Data da pronúncia não pode ser posterior à data da sentença")
                continuar = False

            if data_pronuncia > data_decisao_confirmatoria_pronuncia:
                st.error("Data da pronúncia não pode ser posterior à data da decisão confirmatória da pronúncia")
                continuar = False

            if data_decisao_confirmatoria_pronuncia < data_fato_retroativa:
                st.error("Data da decisão confirmatória da pronúncia não pode ser anterior à data do fato")
                continuar = False

            if data_decisao_confirmatoria_pronuncia < dt_denuncia_retroativa:
                st.error(
                    "Data da decisão confirmatória da pronúncia não pode ser anterior à data do recebimento da denúncia")
                continuar = False

            if data_decisao_confirmatoria_pronuncia > dt_sentenca:
                st.error("Data da decisão confirmatória da pronúncia não pode ser posterior à data da sentença")
                continuar = False

        if continuar:
            prescricao_in_concreto = utilidades.calcula_tempo_prescricao_retroativa(
                dicionario_retroativa['Pena in concreto (anos, meses)'])

            dicionario_retroativa['Prazo Prescrição Retroativa decorrente da Pena in abstrato'] = prescricao_in_concreto
            dicionario_retroativa['Prazo Prescrição Retroativa decorrente da Pena in concreto'] = prescricao_in_concreto

            if verificacao_idade:
                if dicionario_retroativa[
                    'Autor é menor de 21 anos na data dos fatos?'] or dicionario_retroativa[
                    'Autor é maior de 70 anos na sentença?']:
                    dicionario_retroativa[
                        'Prazo Prescrição Retroativa decorrente da Pena in concreto'] = prescricao_in_concreto * 1 / 2
                    prescricao_in_concreto = prescricao_in_concreto * 1 / 2

            dicionario_retroativa[
                'Decurso do prazo entre a data do fato e a data atual'] = utilidades.calcula_diferenca_entre_duas_datas_em_anos_meses_dias(
                data_fato_retroativa, date.today())

            dt_fato_x_dt_atual = utilidades.calcula_diferenca_entre_data_ate_atual(
                data_fato_retroativa)

            dicionario_retroativa[
                'Decurso do prazo entre a data fato e data do recebimento da denúncia'] = utilidades.calcula_diferenca_entre_duas_datas_em_anos_meses_dias(
                data_fato_retroativa, dt_denuncia_retroativa)

            dt_fato_x_dt_denuncia = utilidades.calcula_diferenca_entre_duas_datas(
                data_fato_retroativa,
                dt_denuncia_retroativa)

            dt_denuncia_x_dt_sentenca = utilidades.calcula_diferenca_entre_duas_datas(
                dt_denuncia_retroativa, dt_sentenca)

            if verificar_rito_juri:
                dicionario_retroativa[
                    'Decurso do prazo entre a data do recebimento da denúncia e data da pronúncia'] = utilidades.calcula_diferenca_entre_duas_datas_em_anos_meses_dias(
                    dt_denuncia_retroativa, data_pronuncia)

                dicionario_retroativa[
                    'Decurso do prazo entre a data da pronúncia e da data da decisão confirmatória da pronúncia'] = utilidades.calcula_diferenca_entre_duas_datas_em_anos_meses_dias(
                    data_pronuncia, data_decisao_confirmatoria_pronuncia)

                dicionario_retroativa[
                    'Decurso do prazo entre a data da pronúncia e a data da sentença'] = utilidades.calcula_diferenca_entre_duas_datas_em_anos_meses_dias(
                    data_pronuncia, dt_sentenca)

                dt_pronuncia_x_dt_sentenca = utilidades.calcula_diferenca_entre_duas_datas(data_pronuncia, dt_sentenca)

            if not verificar_rito_juri:
                dicionario_retroativa[
                    'Decurso do prazo entre a data do recebimento da denúncia e a data da sentença sem suspensão'] = utilidades.calcula_diferenca_entre_duas_datas_em_anos_meses_dias(
                    dt_denuncia_retroativa, dt_sentenca)

            if suspensao_prescricao:
                dicionario_retroativa[
                    'Decurso do prazo entre a data do recebimento da denúncia e a data da sentença com suspensão'] = utilidades.calcula_diferenca_entre_duas_datas_em_anos_meses_dias(
                    dt_denuncia_retroativa, dt_sentenca, tempo_suspensao_dias)

            # converte date objetc in string
            dic_novo = {key: (valor.strftime('%d/%m/%Y') if isinstance(valor, date) else valor) for key, valor in
                        dicionario_retroativa.items()}

            # converte True e False in Sim e Não
            dic_novo = {key: ("Sim" if valor is True else ("Não" if valor is False else valor)) for key, valor in
                        dic_novo.items()}

            # with st.expander("Dados e Cálculos"):
            #     st.table(utilidades.converte_dic_dataframe_vertical(dic_novo))

            st.table(utilidades.converte_dic_dataframe_vertical(dic_novo))

            prescreveu = False

            # if dt_fato_x_dt_atual >= prescricao_in_concreto:
            #     st.error("PRESCREVEU ENTRE A DATA DO FATO E A DATA ATUAL", icon="🚫")
            #     prescreveu = True

            if dt_fato_x_dt_denuncia >= prescricao_in_concreto:
                st.error("PRESCREVEU ENTRE A DATA DO FATO E A DATA DE RECEBIMENTO DA DENÚNCIA", icon="🚫")
                prescreveu = True

            if not verificar_rito_juri:
                if dt_denuncia_x_dt_sentenca >= prescricao_in_concreto:
                    st.error("PRESCREVEU ENTRE A DATA DE RECEBIMENTO DA DENÚNCIA E A DATA DA SENTENÇA", icon="🚫")
                    prescreveu = True

            if verificar_rito_juri:
                if dt_recebimento_denuncia_x_dt_pronuncia >= prescricao_in_concreto:
                    st.error("PRESCREVEU ENTRE A DATA DO RECEBIMENTO DA DENÚNCIA E A PRONÚNCIA", icon="🚫")
                    prescreveu = True

                if dt_pronuncia_x_dt_decisao_confirmatoria_pronuncia >= prescricao_in_concreto:
                    st.error("PRESCREVEU ENTRE A DATA DA PRONÚNCIA E A DATA DA DECISÃO CONFIRMATÓRIA DA PRONÚNCIA",
                             icon="🚫")
                    prescreveu = True

                if dt_pronuncia_x_dt_sentenca >= prescricao_in_concreto:
                    st.error("PRESCREVEU ENTRE A DATA DA PRONÚNCIA E A DATA DA SENTENÇA",
                             icon="🚫")
                    prescreveu = True

            if verificar_data_acordao:
                if dt_sentenca_x_dt_acordao >= prescricao_in_concreto:
                    st.error("PRESCREVEU ENTRE A DATA DA SENTENÇA E A DATA DO ACÓRDÃO", icon="🚫")
                    prescreveu = True

            if not prescreveu:
                st.success("NÃO PRESCREVEU", icon="✅")

with tab4:
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
    dicionario_retroativa['Decotar tempo de pena a título de detração?'] = verificar_rito_juri

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
                                                  help='O termo inicial da contagem do prazo da prescrição da pretensão executória é o trânsito em julgado para ambas as partes. STJ. 3ª Seção. AgRg no REsp 1.983.259-PR, Rel. Min. Sebastião Reis Júnior, julgado 26/10/2022 (Info 755)')

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

    dic_execucao['DATA DE PRESCRIÇÃO FINAL'] =  dic_execucao['Data de prescrição']

    if verificacao_idade:
        print('oi oi oi ')
        print(dic_execucao)
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

            dic_execucao['Data de prescrição acrescida de reincidência reduzida pela metade em razão da idade do autor'] = soma_ano_mes_e_calcula_nova_prescricao(
                dic_execucao['Prazo prescricional com reincidência pela metade em razão da idade do autor (anos, meses)'],
                dic_execucao['Termo Inicial da Prescrição'])

            if dic_execucao[
                'Data de prescrição acrescida de reincidência reduzida pela metade em razão da idade do autor'] > dic_execucao['DATA DE PRESCRIÇÃO FINAL']:
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

