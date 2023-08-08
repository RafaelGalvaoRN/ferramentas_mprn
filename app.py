import streamlit as st
import dicionario_legislacao
import utilidades
from datetime import datetime, timedelta, date
import copy
import inspect
import dicionario_legislacao as dl

tab1, tab2, tab3 = st.tabs(["Introdução", "Calculadora de Prescrição",
                            "Calculadora de Prescrição Retroativa"])

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
    data_fato = st.date_input(label='Data do Fato', value=None, format="DD/MM/YYYY", min_value=data_minima,
                              help="Art. 111 - A prescrição, antes de transitar em julgado a sentença final, começa a correr: I - do dia em que o crime se consumou; II - no caso de tentativa, do dia em que cessou a atividade criminosa; III - nos crimes permanentes, do dia em que cessou a permanência; IV - nos de bigamia e nos de falsificação ou alteração de assentamento do registro civil, da data em que o fato se tornou conhecido. V - nos crimes contra a dignidade sexual ou que envolvam violência contra a criança e o adolescente, previstos neste Código ou em legislação especial, da data em que a vítima completar 18 (dezoito) anos, salvo se a esse tempo já houver sido proposta a ação penal.")

    dicionario_final['data_fato'] = data_fato

    legislacao = st.radio('Legislação', ['Código Penal', 'Lei Maria da Penha',
                                         'Lei 11.343/06 - Lei de Drogas',
                                         'Lei 10.826/03 - Estatuto do Desarmamento',
                                         "Decreto_Lei nº 3.688 - Lei das Contravenções Penais"])

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

    verificacao_idade = st.checkbox('Verificar Idade do Autor')
    dicionario_final['verificacao_idade'] = verificacao_idade

    if verificacao_idade:
        # Calcule a data de 90 anos atrás
        data_minima = datetime.today() - timedelta(days=100 * 365)

        # Agora você pode usar 'data_minima' como o valor de 'min_value'
        idade_autor = st.date_input('Data de nascimento do Autor do fato', value=None, format="DD/MM/YYYY",
                                    min_value=data_minima,
                                    help='Art. 115 - São reduzidos de metade os prazos de prescrição quando o criminoso era, '
                                         'ao tempo do crime, menor de 21 (vinte e um) anos, ou, na data da sentença, '
                                         'maior de 70 (setenta) anos.')

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

    dt_sentenca = st.date_input('Data da sentença', key="dt_sentenca",
                                format="DD/MM/YYYY", min_value=data_minima)

    dicionario_retroativa['Data da Sentença'] = dt_sentenca

    suspensao_prescricao = st.checkbox('Suspensão da Prescrição', key='suspensao_prescricao_retroativa')
    dicionario_retroativa['Suspensão da Prescrição?'] = suspensao_prescricao

    dicionario_retroativa['Período de Suspensão'] = timedelta(days=0)

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
        dicionario_retroativa['Período de Suspensão'] = dt_fim_suspensao_retroativa - dt_inicio_suspensao_retroativa

    verificacao_idade = st.checkbox('Verificar Idade do Autor', key="verificacao_idade_retroativa")
    dicionario_retroativa['Houve verificação da idade do autor?'] = verificacao_idade

    if verificacao_idade:
        # Calcule a data de 90 anos atrás
        data_minima = datetime.today() - timedelta(days=100 * 365)

        # Agora você pode usar 'data_minima' como o valor de 'min_value'
        dt_nascimento_autor_retroativa = st.date_input('Data de nascimento do Autor do fato',
                                                       key="idade_autor_retroativa",
                                                       value=None, format="DD/MM/YYYY",
                                                       min_value=data_minima,
                                                       help='Art. 115 - São reduzidos de metade os prazos de prescrição quando o criminoso era, '
                                                            'ao tempo do crime, menor de 21 (vinte e um) anos, ou, na data da sentença, '
                                                            'maior de 70 (setenta) anos.')

        dicionario_retroativa['Data de nascimento do autor'] = dt_nascimento_autor_retroativa

        dicionario_retroativa[
            'Autor é menor de 21 anos na data dos fatos?'] = utilidades.calcula_se_e_menor_21_tempo_crime(
            dt_nascimento_autor_retroativa, data_fato_retroativa)

        dicionario_retroativa['Idade do autor na data dos fatos:'] = utilidades.calcular_idade_na_data(
            dt_nascimento_autor_retroativa, data_fato_retroativa)

        dicionario_retroativa[
            'Autor é maior de 70 anos na data da sentença?'] = utilidades.calcula_se_e_menor_21_tempo_crime(
            dt_nascimento_autor_retroativa, data_fato_retroativa)

        dicionario_retroativa['Idade do autor na data da sentença:'] = utilidades.calcular_idade_na_data(
            dt_nascimento_autor_retroativa, dt_sentenca)

    if st.button('Calcular', key='buttao_calcular_retroativa'):
        print(dicionario_retroativa)

        prescricao_in_concreto = utilidades.calcula_tempo_prescricao_retroativa(
            dicionario_retroativa['Pena in concreto (anos, meses)'])
        dicionario_retroativa['Prazo Prescrição Retroativa decorrente da Pena in concreto'] = prescricao_in_concreto

        dicionario_retroativa[
            'Decurso do prazo entre a data do fato e a data atual'] = utilidades.calcula_diferenca_entre_data_ate_atual(
            data_fato_retroativa)
        dt_fato_x_dt_atual =  dicionario_retroativa[
            'Decurso do prazo entre a data do fato e a data atual']

        dicionario_retroativa[
            'Decurso do prazo entre a data fato e data do recebimento da denuncia'] = utilidades.calcula_diferenca_entre_duas_datas(
            data_fato_retroativa,
            dt_denuncia_retroativa)
        dt_fato_x_dt_denuncia = dicionario_retroativa[
             'Decurso do prazo entre a data fato e data do recebimento da denuncia']

        dicionario_retroativa[
            'Decurso do prazo entre a data do recebimento da denuncia e a data da sentença'] = utilidades.calcula_diferenca_entre_duas_datas(
            dt_denuncia_retroativa, dt_sentenca)
        dt_denuncia_x_dt_sentenca = dicionario_retroativa[
            'Decurso do prazo entre a data do recebimento da denuncia e a data da sentença']

        dic_novo = {key: (valor.strftime('%d/%m/%Y') if isinstance(valor, date) else valor) for key, valor in
                    dicionario_retroativa.items()}

        st.table(utilidades.converte_dic_dataframe_vertical(dic_novo))

        prescreveu = False

        if dt_fato_x_dt_atual >= prescricao_in_concreto:
            st.error("PRESCREVEU ENTRE A DATA DO FATO E A DATA ATUAL")
            prescreveu = True

        if dt_fato_x_dt_denuncia >= prescricao_in_concreto:
            st.error("PRESCREVEU ENTRE A DATA DO FATO E A DATA DE RECEBIMENTO DA DENÚNCIA")
            prescreveu = True

        if dt_denuncia_x_dt_sentenca  >= prescricao_in_concreto:
            st.error("PRESCREVEU ENTRE A DATA DE RECEBIMENTO DA DENÚNCIA E A DATA DA SENTENÇA")
            prescreveu = True

        if not prescreveu:
            st.success("NÃO PRESCREVEU", icon="✅")



