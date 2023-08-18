import streamlit as st
import dicionario_legislacao
import utilidades
from utilidades import *
from datetime import datetime, timedelta, date
import copy
import inspect
import dicionario_legislacao as dl


def calc_prescricao_retroativa():
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

    data_minima = datetime.today() - timedelta(days=60 * 365)

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