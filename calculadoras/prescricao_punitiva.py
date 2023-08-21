import streamlit as st
import dicionario_legislacao
import utilidades
from utilidades import *
from datetime import datetime, timedelta, date
import copy
import inspect
import dicionario_legislacao as dl
from dateutil.relativedelta import relativedelta


def calc_prescricao_punitiva():
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


def calc_prescricao_punitiva_tributaria():
    tributario_consolidado = {}

    processo = st.text_input(label='Processo', max_chars=30, key="tributario")
    tributario_consolidado['Número do Processo'] = processo
    reu = st.text_input(label='Réu', max_chars=30, key="tributario1")
    tributario_consolidado['Nome do Contribuinte'] = reu
    data_minima = datetime.today() - timedelta(days=60 * 365)

    data_fato = st.date_input(label='Data do Fato', value=None, format="DD/MM/YYYY", min_value=data_minima,
                              help="Data da consumação do crime. Nos crimes tributários sujeitos a pagamentos de exações, a data do fato ocorre 90 dias após o último vencimento, onde se opera a perempção")

    tributario_consolidado['Data do fato'] = data_fato

    legislacao_tributaria = st.radio('Legislação', [
        "Lei 8.137/90 - Lei dos crimes contra a ordem tributária, econômica e contra as relações de consumo"])

    if legislacao_tributaria == 'Lei 8.137/90 - Lei dos crimes contra a ordem tributária, econômica e contra as relações de consumo':
        tributario_consolidado['Legislação'] = legislacao_tributaria
        crimes = [crime for crime in dicionario_legislacao.tributario.keys()]
        tipo_penal = st.selectbox('Tipo Penal', crimes)
        tributario_consolidado['Tipo Penal'] = tipo_penal
        tributario_consolidado['Prescrição in abstrato (anos)'] = dl.tributario[tipo_penal]
        tributario_consolidado['Prescrição in abstrato considerando a data do fato'] = data_fato + relativedelta(
            years=tributario_consolidado['Prescrição in abstrato (anos)'])

    suspensao_parcelamento = st.checkbox("Houve suspensão pelo parcelamento tributário")
    tributario_consolidado['Houve suspensão pelo parcelamento tributário'] = suspensao_parcelamento

    if suspensao_parcelamento:
        qtd_suspensao = st.number_input('Quantidade de suspensões:', min_value=1, max_value=3)
        tributario_consolidado['Quantidade de suspensões por parcelamento tributário'] = qtd_suspensao

    if suspensao_parcelamento:
        qtd_dias_suspensos_total = 0
        for i in range(qtd_suspensao):
            data_inicio = st.date_input(label=f'Data de início do parcelamento {i + 1}', value=None,
                                        format="DD/MM/YYYY", min_value=data_minima)

            data_fim = st.date_input(label=f'Data de fim do parcelamento {i + 1}', value=None, format="DD/MM/YYYY",
                                     min_value=data_minima)

            tributario_consolidado[f'Data início da Suspensão do parcelamento {i + 1}'] = data_inicio
            tributario_consolidado[f'Data fim da Suspensão do parcelamento {i + 1}'] = data_fim
            tributario_consolidado[f'Quantidade de dias suspensos no parcelamento {i + 1}'] = (
                    data_fim - data_inicio).days
            qtd_dias_suspensos_total += tributario_consolidado[f'Quantidade de dias suspensos no parcelamento {i + 1}']

            st.markdown("---")

        tributario_consolidado['Quantidade total de dias suspensos no parcelamento'] = qtd_dias_suspensos_total
        tributario_consolidado['Data da Prescrição in abstrato considerando os dias de suspensão do parcelamento'] = \
            tributario_consolidado['Prescrição in abstrato considerando a data do fato'] + relativedelta(
                days=qtd_dias_suspensos_total)

    # funcao que sintetiza parte do código
    utilidades.streamlit_denuncia_x_suspensao_prescricao_x_verificar_idade(
        tributario_consolidado)

    tributario_consolidado["Prescrição final"] = get_latest_datetime(tributario_consolidado)



    if st.button('Calcular', key="tributario12"):
        current_date = datetime.now().date()

        prescricao_date = tributario_consolidado.get("Prescrição in abstrato considerando a data do fato")
        if prescricao_date:
            if tributario_consolidado.get("Prescrição in abstrato considerando a data do fato") < current_date:
                st.error('PRESCREVEU ENTRE A DATA DO FATO E A PRESENTE DATA', icon='🚫')
            else:
                st.success('NÃO PRESCREVEU ENTRE A DATA DO FATO E A PRESENTE DATA', icon="✅")

        if suspensao_parcelamento:
            if tributario_consolidado[
                'Data da Prescrição in abstrato considerando os dias de suspensão do parcelamento'] < current_date:
                st.error('PRESCREVEU ENTRE A DATA DO FATO E A PRESENTE DATA CONSIDERADO A SUSPENSÃO PELO PARCELAMENTO',
                         icon='🚫')
            else:
                st.success(
                    'NÃO PRESCREVEU ENTRE A DATA DO FATO E A PRESENTE DATA CONSIDERANDO A SUSPENSÃO PELO PARCELAMENTO',
                    icon="✅")

        if tributario_consolidado.get('Houve recebimento da denúncia?'):
            if tributario_consolidado['Data da prescrição considerando a data do fato até a data de recebimento da denúncia'] < current_date:
                st.error('PRESCREVEU ENTRE A DATA DO FATO E A DATA DE RECEBIMENTO DA DENÚNCIA',
                         icon='🚫')
            else:
                st.success(
                    'NÃO PRESCREVEU ENTRE A DATA DO FATO E A DATA DE RECEBIMENTO DA DENÚNCIA',
                    icon="✅")

        if tributario_consolidado.get('Houve suspensão da prescricão pela citação editalícia?') and tributario_consolidado.get('Houve recebimento da denúncia?'):
            if tributario_consolidado[
                'Data da prescrição considerando a data do recebimento da denúncia até a presente data e o período de dias de suspensão pela citação editalícia'] < current_date:

                st.error('PRESCREVEU ENTRE A DATA DO RECEBIMENTO DA DENÚNCIA E A PRESENTE DATA CONSIDERANDO A SUSPENSÃO PELA CITAÇÃO EDITALÍCIA',
                         icon='🚫')
            else:
                st.success(
                    'NÃO PRESCREVEU ENTRE A DATA DO RECEBIMENTO DA DENÚNCIA E A PRESENTE DATA CONSIDERANDO A SUSPENSÃO PELA CITAÇÃO EDITALÍCIA',
                    icon="✅")

        if tributario_consolidado.get('Houve verificação da idade do autor?'):

            if tributario_consolidado[
            'Autor é menor de 21 anos na data dos fatos?'] or tributario_consolidado[
            'Autor é maior de 70 anos?']:
                if tributario_consolidado.get('Data da Prescrição in abstrato considerando a reduçao pela metade pela idade e a data do fato') < current_date:
                    st.error('PRESCREVEU ENTRE A DATA DO FATO E A PRESENTE DATA CONSIDERANDO A REDUÇÃO PELA IDADE', icon='🚫')
                else:
                    st.success('NÃO PRESCREVEU ENTRE A DATA DO FATO E A PRESENTE DATA CONSIDERANDO A REDUÇÃO PELA IDADE', icon="✅")

                if tributario_consolidado.get('Houve suspensão pelo parcelamento tributário'):
                    if tributario_consolidado.get('Prescrição in abstrato considerando a reduçao pela metade pela idade e os dias de suspensao do parcelamento') < current_date:
                        st.error('PRESCREVEU ENTRE A DATA DO FATO E A PRESENTE DATA CONSIDERANDO A REDUÇÃO PELA IDADE E OS DIAS DE PARCELAMENTO',
                                 icon='🚫')
                    else:
                        st.success(
                        'NÃO PRESCREVEU ENTRE A DATA DO FATO E A PRESENTE DATA CONSIDERANDO A REDUÇÃO PELA IDADE E OS DIAS DE PARCELAMENTO',
                        icon="✅")

                if tributario_consolidado.get('Houve recebimento da denúncia?'):
                    if tributario_consolidado.get(
                            'Prescrição in abstrato considerando a reduçao pela metade pela idade e o recebimento da denúncia') < current_date:
                        st.error(
                            'PRESCREVEU ENTRE A DATA DO RECEBIMENTO DA DENÚNCIA ATÉ A PRESENTE DATA CONSIDERANDO A REDUÇÃO PELA IDADE',
                            icon='🚫')
                    else:
                        st.success(
                        'NÃO PRESCREVEU ENTRE A DATA DO RECEBIMENTO DA DENÚNCIA ATÉ A PRESENTE DATA CONSIDERANDO A REDUÇÃO PELA IDADE',
                        icon="✅")

                if tributario_consolidado.get('Houve recebimento da denúncia?') and tributario_consolidado['Houve suspensão pelo parcelamento tributário']:
                    if tributario_consolidado[
                    'Prescrição in abstrato considerando a reduçao pela metade pela idade e os dias de suspensao do parcelamento'] < current_date:
                        st.error(
                            'PRESCREVEU ENTRE A DATA DO RECEBIMENTO DA DENÚNCIA ATÉ A PRESENTE DATA CONSIDERANDO A REDUÇÃO PELA IDADE E A SUISPENSÃO EDITALÍCIA',
                            icon='🚫')
                    else:
                        st.success(
                            'NÃO PRESCREVEU ENTRE A DATA DO RECEBIMENTO DA DENÚNCIA ATÉ A PRESENTE DATA CONSIDERANDO A REDUÇÃO PELA IDADE E A SUSPENSÃO EDITALÍCIA',
                            icon="✅")





        # converte date objetc in string

        dic_executoria = {}
        for key, valor in tributario_consolidado.items():
            # Check if it's a date
            if isinstance(valor, date):
                tributario_consolidado[key] = valor.strftime('%d/%m/%Y')
            # Check if it's a boolean True or False
            elif valor is True:
                tributario_consolidado[key] = "Sim"
            elif valor is False:
                tributario_consolidado[key] = "Não"
            # Else, just assign the original value
            else:
                tributario_consolidado[key] = valor

        st.table(converte_dic_dataframe_vertical(tributario_consolidado))
