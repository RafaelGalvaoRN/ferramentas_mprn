import pprint
from datetime import datetime, date, timedelta
import pandas as pd
import dicionario_legislacao
from dateutil.relativedelta import relativedelta
import streamlit as st
import pprint

dic_prescricao = {**dicionario_legislacao.codigo_penal, **dicionario_legislacao.maria_da_penha,
                  **dicionario_legislacao.trafico, **dicionario_legislacao.estatuto_desarmamento,
                  **dicionario_legislacao.lcp, **dicionario_legislacao.ctb, **dicionario_legislacao.ambiental,
                  **dicionario_legislacao.tributario}


def streamlit_denuncia_x_suspensao_prescricao_x_verificar_idade(tributario_consolidado) -> dict:
    dic_resultado = {}

    recebimento_denuncia = st.checkbox('Recebimento da Denúncia')
    dic_resultado['Houve recebimento da denúncia?'] = recebimento_denuncia

    if recebimento_denuncia:
        data_minima = datetime.today() - timedelta(days=30 * 365)

        dt_denuncia = st.date_input('Data do recebimento da Denúncia', format="DD/MM/YYYY", min_value=data_minima,
                                    help='CP. Art. 117 - O curso da prescrição interrompe-se: I - pelo recebimento da denúncia ou da queixa;')

        dic_resultado['Data de recebimento da Denuncia'] = dt_denuncia

        dic_resultado['Data da prescrição considerando o recebimento da denúncia'] = dt_denuncia + relativedelta(
            years=tributario_consolidado['Prescrição in abstrato (anos)'])

    suspensao_prescricao = st.checkbox('Suspensão da Prescrição')
    dic_resultado['Houve suspensão da prescricão pela citação editalícia?'] = suspensao_prescricao

    if suspensao_prescricao:
        data_minima = datetime.today() - timedelta(days=30 * 365)

        dt_inicio_suspensao = st.date_input('Data do Início da Suspensão', value=None, format="DD/MM/YYYY",
                                            min_value=data_minima)
        dt_fim_suspensao = st.date_input('Data do Fim da Suspensão', value=None, format="DD/MM/YYYY",
                                         min_value=data_minima)

        dic_resultado['Data de inicio da suspensão pela citação editalícia'] = dt_inicio_suspensao
        dic_resultado['Data de fim da suspensão pela citação editalícia'] = dt_fim_suspensao

        dic_resultado['Tempo em dias da suspensão pela citação editalícia'] = (
                dt_fim_suspensao - dt_inicio_suspensao).days

        if recebimento_denuncia:
            dic_resultado[
                'Data da prescrição considerando o recebimento da denúncia e o período de dias de suspensão pela citação editalícia'] = dt_denuncia + relativedelta(
                years=tributario_consolidado['Prescrição in abstrato (anos)']) + relativedelta(
                days=dic_resultado['Tempo em dias da suspensão pela citação editalícia'])

    verificacao_idade = st.checkbox('Verificar Idade do Autor',
                                    help='Art. 115 - São reduzidos de metade os prazos de prescrição quando o criminoso era, '
                                         'ao tempo do crime, menor de 21 (vinte e um) anos, ou, na data da sentença, '
                                         'maior de 70 (setenta) anos.')
    dic_resultado['Houve verificação da idade do autor? '] = verificacao_idade

    if verificacao_idade:
        # Calcule a data de 90 anos atrás
        data_minima = datetime.today() - timedelta(days=100 * 365)

        # Agora você pode usar 'data_minima' como o valor de 'min_value'
        dt_nascimento_autor = st.date_input('Data de nascimento do Autor do fato', value=None, format="DD/MM/YYYY",
                                            min_value=data_minima)

        dic_resultado['Data de nascimento do autor'] = dt_nascimento_autor

        dt_fato = tributario_consolidado['Data do fato']

        dic_resultado['Idade do autor na data do fato (anos)'] = calcular_idade_na_data(
            dt_nascimento_autor,
            dt_fato)

        dic_resultado[
            'Autor é menor de 21 anos na data dos fatos?'] = calcula_se_e_menor_21_tempo_crime(
            dt_nascimento_autor, dt_fato)

        dic_resultado['Idade atual do autor (anos)'] = calcular_idade(dt_nascimento_autor)

        dic_resultado[
            'Autor é maior de 70 anos?'] = calcula_se_e_maior_de_setenta_anos_na_sentenca(
            dt_nascimento_autor, datetime.today())

        if dic_resultado[
            'Autor é menor de 21 anos na data dos fatos?'] or dic_resultado[
            'Autor é maior de 70 anos?']:

            dic_resultado[
                'Prescrição in abstrato considerando a reduçao pela metade pela idade'] = novo_prazo_prescricao = int(
                tributario_consolidado['Prescrição in abstrato (anos)'] / 2)

            dic_resultado[
                'Data da Prescrição in abstrato considerando a reduçao pela metade pela idade e a data do fato'] = \
                tributario_consolidado['Data do fato'] + relativedelta(years=novo_prazo_prescricao)

            if tributario_consolidado['Houve suspensão pelo parcelamento tributário']:
                dic_resultado[
                    'Prescrição in abstrato considerando a reduçao pela metade pela idade e os dias de suspensao do parcelamento'] = \
                    tributario_consolidado['Data do fato'] + relativedelta(years=novo_prazo_prescricao) + relativedelta(
                        days=tributario_consolidado['Quantidade total de dias suspensos no parcelamento'])

            if recebimento_denuncia:
                dic_resultado[
                    'Prescrição in abstrato considerando a reduçao pela metade pela idade e o recebimento da denúncia'] = \
                    dic_resultado['Data de recebimento da Denuncia'] + relativedelta(years=novo_prazo_prescricao)

                if suspensao_prescricao:
                    dic_resultado[
                        'Prescrição in abstrato considerando a reduçao pela metade pela idade e o recebimento da denúncia e a suspensão da prescrição editalícia'] = \
                        dic_resultado['Data de recebimento da Denuncia'] + relativedelta(
                            years=novo_prazo_prescricao) + relativedelta(
                            days=dic_resultado['Tempo em dias da suspensão pela citação editalícia'])

                    # print('aqio aqio')
            # dic_resultado['Nova prescrição in abstrato (anos e meses)' ] = tributario_consolidado

    return dic_resultado


def streamlit_calcular_corrige_dic_imprime_tabela(tributario, dic):
    if st.button('Calcular', key=tributario):
        # converte date objetc in string

        dic_executoria = {}
        for key, valor in dic.items():
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

        st.table(converte_dic_dataframe_vertical(dic_executoria))


def get_latest_datetime(d):
    # Filtra todos os valores que são instâncias de datetime

    print('oiosiosiadosiodi')
    print(d)

    datetimes = [value for value in d.values() if isinstance(value, (date, datetime))]

    print(datetimes)
    # Retorna o datetime mais recente, se houver algum
    if datetimes:
        return max(datetimes)



def soma_ano_mes_e_calcula_nova_prescricao(ano_mes: tuple, termo_inicial: datetime) -> datetime:
    ano = ano_mes[0]
    mes = ano_mes[1]

    nova_data = termo_inicial + relativedelta(years=ano)
    nova_data = nova_data + relativedelta(months=mes)

    return nova_data


def reduz_metade_prescricao_in_abstrato_pela_idade(prescricao: int) -> tuple:
    if prescricao == 3:
        return (1, 6)
    elif prescricao == 4:
        return (2, 0)
    elif prescricao == 8:
        return (2, 0)
    elif prescricao == 12:
        return (6, 0)
    elif prescricao == 16:
        return (8, 0)
    elif prescricao == 20:
        return (10, 0)


def soma_ano_calcula_nova_prescricao(ano: int, termo_inicial: datetime) -> datetime:
    nova_data = termo_inicial + relativedelta(years=ano)

    return nova_data


def calcula_diferenca_entre_data_ate_atual(data: date) -> int:
    # convert data string in dic in datetime object
    data_fato = data
    # pega data atual
    data_atual = date.today()

    # calcula a diferenca entre a data do fato e a data atual
    diferenca_dt_fato_x_dt_atual = (data_atual - data_fato)

    # converte em anos e dias a diferenca
    anos, dias_restantes = divmod(diferenca_dt_fato_x_dt_atual.days, 365)

    if anos < 0:
        anos = 0

    # verifica se passou de um ano, ou seja, se há dias sobressalentes no ano subsequente
    if dias_restantes > 0:
        # acrescenta um ano para calcular a comparacao com a prescricao
        tempo_decorrido_para_prescricao = anos + 1
        return tempo_decorrido_para_prescricao

    else:
        return anos


def calcula_diferenca_entre_data_ate_atual_em_dias(data: datetime) -> int:
    # convert data string in dic in datetime object
    data_fato = data

    # pega data atual
    data_atual = date.today()

    # calcula a diferenca entre a data do fato e a data atual
    diferenca_dt_fato_x_dt_atual_dias = (data_atual - data_fato).days

    return diferenca_dt_fato_x_dt_atual_dias


def calcula_diferenca_entre_duas_datas_em_anos_meses_dias(data_preterita: datetime, data_posterior: date,
                                                          tempo_suspensao_dias=0):
    # Calcula a diferença entre a data do fato e a data atual
    diferenca_total = (data_posterior - data_preterita)

    if tempo_suspensao_dias != 0:
        diferenca_total = diferenca_total - tempo_suspensao_dias

    # Considerando que um ano tem 365.25 dias (contabilizando anos bissextos) e um mês tem 30.44 dias em média
    anos = diferenca_total.days // 365.25
    meses_restantes = (diferenca_total.days % 365.25) // 30.44
    dias_restantes = diferenca_total.days - (anos * 365.25 + meses_restantes * 30.44)

    return f' {int(anos)} ano(s),  {int(meses_restantes)} mê(ses) e {int(dias_restantes)} dia(s)'


def calcula_diferenca_entre_duas_datas(data_antiga: date, data_nova: date) -> int:
    # calcula a diferença entre as duas datas
    anos = data_nova.year - data_antiga.year - (
            (data_nova.month, data_nova.day) < (data_antiga.month, data_antiga.day))

    # se a diferença for negativa, retorna 0
    if anos < 0:
        return 0

    # verifica se passou de um ano, ou seja, se há dias sobressalentes no ano subsequente
    if data_nova.replace(year=data_antiga.year + anos) < data_antiga:
        # acrescenta um ano para calcular a comparação com a prescrição
        return anos + 1

    return anos


def converte_dias_para_anos_mais_um(tempo: int) -> int:
    # converte em anos e dias a diferenca
    anos, dias_restantes = divmod(tempo, 365)

    if anos < 0:
        anos = 0

    # verifica se passou de um ano, ou seja, se há dias sobressalentes no ano subsequente
    if dias_restantes > 0:
        # acrescenta um ano para calcular a comparacao com a prescricao
        tempo_decorrido_para_prescricao = anos + 1
        return tempo_decorrido_para_prescricao

    else:
        return anos


def calcula_se_e_menor_21_tempo_crime(data_nascimento: date, data_fato: date) -> bool:
    # convert idade para datetime:

    # calcula a idade quando da data do fato
    # calcula a idade na data do fato
    idade_na_data_fato = data_fato.year - data_nascimento.year - (
            (data_fato.month, data_fato.day) < (
        data_nascimento.month, data_nascimento.day))

    # verifica se a pessoa tinha 21 anos na data do fato

    return idade_na_data_fato < 21


def calcula_se_e_maior_de_setenta_anos(data_nascimento: date) -> bool:
    # pega data fato
    data_atual = datetime.today()

    # calcula a idade na data atual
    idade_na_data_atual = data_atual.year - data_nascimento.year - (
            (data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day))

    setenta_anos = 70 * 365

    # verifica se a pessoa tem 70 anos ou mais
    return idade_na_data_atual >= 70


def calcula_se_e_maior_de_setenta_anos_na_sentenca(data_nascimento: date, data_sentenca: date) -> bool:
    # calcula a idade na data atual
    idade_na_data_sentenca = data_sentenca.year - data_nascimento.year - (
            (data_sentenca.month, data_sentenca.day) < (data_nascimento.month, data_nascimento.day))

    return idade_na_data_sentenca >= 70


def calcula_data_prescricao(data_do_fato, tempo_prescricao_crime, reduz_metade=1, periodo_suspenso=0):
    # Convertendo a string da data para um objeto datetime

    # Se reduz_metade for diferente de 1, o tempo de prescrição é ajustado
    tempo_prescricao_crime *= reduz_metade

    # Converte periodo_suspenso para valor absoluto, garantindo que seja positivo
    periodo_suspenso = abs(periodo_suspenso)

    # Convertendo anos para meses
    tempo_prescricao_crime_meses = int(tempo_prescricao_crime * 12)

    data_prescricao = data_do_fato + relativedelta(months=+tempo_prescricao_crime_meses) + relativedelta(
        days=+periodo_suspenso)

    data_prescricao = data_prescricao.strftime('%d/%m/%Y')

    return data_prescricao


def calcula_decote_detratacao(pena_definitiva: tuple, tempo_detracao: tuple) -> tuple:
    tempo_meses_pena_definitiva = pena_definitiva[0] * 12 + pena_definitiva[1]

    tempo_meses_detracao = tempo_detracao[0] * 12 + tempo_detracao[1]

    pena_final_meses = tempo_meses_pena_definitiva - tempo_meses_detracao

    anos = pena_final_meses // 12

    meses = pena_final_meses - (anos * 12)

    return anos, meses


def calcula_aumento_prazo_prescricao_reincidencia(prazo_prescricional_anos: int) -> tuple:
    anos_acrescido_um_terco = prazo_prescricional_anos

    anos_acrescido_um_terco *= 4 / 3

    anos = int(anos_acrescido_um_terco)  # Parte inteira dos anos

    meses = (anos_acrescido_um_terco - anos) * 12  # Converte a parte decimal em meses

    return int(anos), int(round(meses))


def calcula_metade_tempo(anos: int, meses: int) -> tuple:
    # Converte tudo para meses
    total_meses = anos * 12 + meses

    # Calcula a metade
    metade_meses = total_meses / 2

    # Converte de volta para anos e meses
    anos_metade = int(metade_meses // 12)  # Usa a divisão de piso para obter a parte inteira (anos)
    meses_metade = int(round(metade_meses % 12))  # Usa o módulo para obter a parte restante (meses)

    return anos_metade, meses_metade


# def calcula_diferenca_duas_datas_em_dias(data_antiga: str, data_nova: str) -> int:
#     # convert data string in dic in datetime object
#     data_antiga = datetime.strptime(data_antiga, "%Y-%m-%d").date()
#     # pega data atual
#     data_nova = datetime.strptime(data_nova, "%Y-%m-%d").date()
#
#     # calcula a diferenca entre a data do fato e a data atual
#     diferenca_em_dias = (data_nova - data_antiga).days
#
#     # converte em anos e dias a diferenca
#     return diferenca_em_dias


def calcula_tempo_prescricao_retroativa(tupla):
    anos = tupla[0]
    meses = tupla[1]

    if anos == 0 and meses == 0:
        return 0
    elif anos > 0 and meses == 0:
        tempo = anos
    elif meses > 0 and anos > 0:
        tempo = anos + 1

    elif meses > 0 and anos == 0:
        tempo = 0.5

    if tempo < 1:
        return 3

    elif tempo <= 2:
        return 4

    elif tempo <= 4:
        return 8

    elif tempo <= 8:
        return 12

    elif tempo <= 12:
        return 16

    elif tempo > 12:
        return 20


def corrige_ordem_da_data_str(data) -> str:
    """
    Corrige o formato de uma string ou objeto datetime.date para ficar na data brasileira
    :param data: str or datetime.date
    :return: str
    """
    if isinstance(data, str):
        data_obj = datetime.strptime(data, '%Y-%m-%d')
    else:  # assuming it's a datetime.date object
        data_obj = data

    data_formatada = data_obj.strftime("%d-%m-%Y")
    return data_formatada


def calcular_idade(data_de_nascimento):
    hoje = datetime.now()
    idade = hoje.year - data_de_nascimento.year

    if (hoje.month, hoje.day) < (data_de_nascimento.month, data_de_nascimento.day):
        idade -= 1

    return idade


def calcular_idade_na_data(data_de_nascimento, data_do_fato):
    idade = data_do_fato.year - data_de_nascimento.year

    if (data_do_fato.month, data_do_fato.day) < (data_de_nascimento.month, data_de_nascimento.day):
        idade -= 1

    return idade





def analisa_prescricao(dicionario: dict, processo: str = None, reu: str = None):
    if not processo:
        processo = "Não informado"
    if not reu:
        reu = "Não informado"

    resultado = {}
    reducao_da_prescricao_metade = 1

    if dicionario['verificacao_idade'] == True:

        if calcula_se_e_menor_21_tempo_crime(dicionario['idade_autor'],
                                             dicionario['data_fato']) or calcula_se_e_maior_de_setenta_anos(
            dicionario['idade_autor']):
            reducao_da_prescricao_metade = 1 / 2

            crime_analisado = dicionario['crime']

            dic_prescricao[crime_analisado] = dic_prescricao[crime_analisado] * reducao_da_prescricao_metade

            resultado['Redução da Prescrição pela metade?'] = True
        else:
            resultado['Redução da Prescrição pela metade?'] = False

    if dicionario['suspensao_prescricao_bool'] == False:

        # analisa sem ter havido recebimento da denuncia
        if dicionario['recebimento_denuncia_bool'] == False:

            # seta tempo decorrido, considerando a data do fato
            tempo_decorrido_para_prescricao = calcula_diferenca_entre_data_ate_atual(
                dicionario['data_fato'])

            crime_analisado = dicionario['crime']

            if tempo_decorrido_para_prescricao > dic_prescricao[crime_analisado]:
                parecer = f'''
                Ref. ao processo: {processo}\n 
                Investigado(a): {reu}        
                \n\n          
                
                MM. Juíza,\n\n            
                In casu, verifica-se que o(s) delito(s) investigado(s) possui(em) prazo prescricional máximo de {dic_prescricao[crime_analisado]} anos ({crime_analisado}), considerando a idade da parte autora (CP, Art. 115).\n
                Uma vez que os fatos datam de {corrige_ordem_da_data_str(dicionario['data_fato'])}, forçoso reconhecer a incidência da prescrição.\n            
                Insta pontuar que não se operou nenhuma causa de suspensão da prescrição da data do fato até a presente data.\n            
                Ante o exposto, o MP requer o reconhecimento da extinção da punibilidade, nos termos do art. 107, inciso IV, do CP.\n            
                Pede deferimento.\n            
                '''

                resultado['Decurso de prazo prescricional (arredondado em anos)'] = tempo_decorrido_para_prescricao
                resultado['prazo_prescricao'] = dic_prescricao[crime_analisado]
                resultado['resultado'] = True
                resultado['Data da prescrição'] = calcula_data_prescricao(dicionario['data_fato'],
                                                                          dic_prescricao[crime_analisado],
                                                                          reduz_metade=reducao_da_prescricao_metade)

                return resultado, parecer


            else:
                parecer = f'''
                           Ref. ao processo: {processo}\n 
                           Investigado(a): {reu}    
                           \n\n         
                                
                           MM. Juíza,\n\n            
                           In casu, verifica-se que o(s) delito(s) investigado(s) possui(em) prazo prescricional máximo de {dic_prescricao[crime_analisado]} anos ({crime_analisado}), considerando a idade da parte autora (CP, Art. 115)\n
                           Uma vez que os fatos datam de {corrige_ordem_da_data_str(dicionario['data_fato'])}, forçoso reconhecer que não houve a incidência da prescrição.\n            
                           Insta pontuar que não se operou nenhuma causa de suspensão ou interrupção da prescrição da data do fato até a presente data.\n
                           Não houve oferecimento de denúncia e regular recebimento da peça acusatória, apto à interrupção do prazo prescricional.\n             
                           Ante o exposto, o MP requer o prosseguimento do feito.\n            
                           Pede deferimento.\n            
                           '''

                resultado['Decurso de prazo prescricional (arredondado em anos)'] = tempo_decorrido_para_prescricao
                resultado['prazo_prescricao'] = dic_prescricao[crime_analisado]
                resultado['resultado'] = False
                resultado['Data da prescrição'] = calcula_data_prescricao(dicionario['data_fato'],
                                                                          dic_prescricao[crime_analisado],
                                                                          reduz_metade=reducao_da_prescricao_metade)
                return resultado, parecer

        # analisa tendo havido recebimento da denuncia
        elif dicionario['recebimento_denuncia_bool'] == True:

            # seta tempo decorrido, considerando a data do fato
            print('Inicializando análise')
            crime_analisado = dicionario['crime']

            print('Analisando entre data do fato e data recebimento da denuncia:')
            tempo_decorrido_para_prescricao = calcula_diferenca_entre_duas_datas(dicionario['data_fato'],
                                                                                 dicionario[
                                                                                     'Dt_Denuncia'])

            # analisa entre a data do fato e o recebimento da denúncia
            if tempo_decorrido_para_prescricao > dic_prescricao[crime_analisado]:
                parecer = f'''
                Ref. ao processo: {processo}\n 
                Investigado(a): {reu}
                \n\n  

                MM. Juíza,\n\n            
                In casu, verifica-se que o(s) delito(s) investigado(s) possui(em) prazo prescricional máximo de {dic_prescricao[crime_analisado]} anos ({crime_analisado}), considerando a idade da parte autora (CP, Art. 115).\n
                Uma vez que os fatos datam de {corrige_ordem_da_data_str(dicionario['data_fato'])}, forçoso reconhecer a incidência da prescrição.\n            
                Insta pontuar que a denúncia foi recebida em {corrige_ordem_da_data_str(dicionario['Dt_Denuncia'])} mas antes desta causa interruptiva, o jus puniendi estatal já se encontrava prescrito, uma vez ter decorrido {tempo_decorrido_para_prescricao} anos após a data do fato.\n            
                Ante o exposto, o MP requer o reconhecimento da extinção da punibilidade, nos termos do art. 107, inciso IV, do CP.\n            
                Pede deferimento.\n           
                
                '''

                resultado['Decurso de prazo prescricional (arredondado em anos)'] = tempo_decorrido_para_prescricao
                resultado['prazo_prescricao'] = dic_prescricao[crime_analisado]
                resultado['resultado'] = True
                resultado['Data da prescrição'] = calcula_data_prescricao(dicionario['data_fato'],
                                                                          dic_prescricao[crime_analisado],
                                                                          reduz_metade=reducao_da_prescricao_metade)

                return resultado, parecer

            print('Analisando entre data do recebimento da denuncia e a data atual:')
            tempo_decorrido_para_prescricao = calcula_diferenca_entre_data_ate_atual(
                dicionario['Dt_Denuncia'])

            # analisa entre a data do recebimento da denúncia e a data atual
            if tempo_decorrido_para_prescricao > dic_prescricao[crime_analisado]:
                parecer = f'''
                           Ref. ao processo: {processo}\n 
                           Investigado(a): {reu}
                           \n\n  

                           MM. Juíza,\n\n            
                           In casu, verifica-se que o(s) delito(s) investigado(s) possui(em) prazo prescricional máximo de {dic_prescricao[crime_analisado]} anos ({crime_analisado}), considerando a idade da parte autora (CP, Art. 115). \n
                           Uma vez que os fatos datam de {corrige_ordem_da_data_str(dicionario['data_fato'])}, forçoso reconhecer a incidência da prescrição.\n            
                           Insta pontuar que a denúncia foi recebida em {dicionario['Dt_Denuncia']} tendo, após esta causa interruptiva se operado a prescrição do jus puniendi estatal, uma vez ter decorrido {tempo_decorrido_para_prescricao} anos após tal causa interruptiva.\n            
                           Ante o exposto, o MP requer o reconhecimento da extinção da punibilidade, nos termos do art. 107, inciso IV, do CP.\n            
                           Pede deferimento.\n            
                           '''

                resultado['Decurso de prazo prescricional (arredondado em anos)'] = tempo_decorrido_para_prescricao
                resultado['prazo_prescricao'] = dic_prescricao[crime_analisado]
                resultado['resultado'] = True
                resultado['Data da prescrição'] = calcula_data_prescricao(dicionario['Dt_Denuncia'],
                                                                          dic_prescricao[crime_analisado],
                                                                          reduz_metade=reducao_da_prescricao_metade)

                return resultado, parecer


            else:
                parecer = f'''
                Ref. ao processo: {processo}\n 
                Investigado(a): {reu} 
                \n\n  
                
                MM. Juíza,\n\n            
                In casu, verifica-se que o(s) delito(s) investigado(s) possui(em) prazo prescricional máximo de {dic_prescricao[crime_analisado]} anos, uma vez a 
                 conduta se subsumir ao tipo penal de {crime_analisado}, considerando a idade da parte autora (CP, Art. 115).\n
                Uma vez que os fatos datam de {corrige_ordem_da_data_str(dicionario['data_fato'])}, forçoso reconhecer que não se operou a prescrição.\n            
                Insta pontuar que fora analisado o marco interruptivo atinente ao recebimento da denúncia quando da análise do procedimento (CP, Art. 117, Inc. I).\n            
                Ante o exposto, o MP requer o prosseguimento do feito.\n            
                Pede deferimento.\n     
                   '''
                resultado['Decurso de prazo prescricional (arredondado em anos)'] = tempo_decorrido_para_prescricao
                resultado['prazo_prescricao'] = dic_prescricao[crime_analisado]
                resultado['resultado'] = False
                resultado['Data da prescrição'] = calcula_data_prescricao(dicionario['Dt_Denuncia'],
                                                                          dic_prescricao[crime_analisado],
                                                                          reduz_metade=reducao_da_prescricao_metade)
                return resultado, parecer


    elif dicionario['suspensao_prescricao_bool'] == True:
        tempo_suspensao_dias = dicionario['Dt_inicio_suspensao'] - dicionario['Dt_fim_suspensao']
        tempo_suspensao_dias = tempo_suspensao_dias.days

        print(f'Tempo de suspensao calculado em dias: {tempo_suspensao_dias}')

        # analisa sem ter havido recebimento da denuncia
        if dicionario['recebimento_denuncia_bool'] == False:

            # seta tempo decorrido, considerando a data do fato
            tempo_decorrido_para_prescricao = calcula_diferenca_entre_data_ate_atual_em_dias(
                dicionario['data_fato'])
            # calcula tempo de suspensao em dias

            tempo_suspensao_dias = (dicionario['Dt_inicio_suspensao'] - dicionario['Dt_fim_suspensao']).days

            # desconta o tempo que o processo esteve suspenso
            tempo_efetiva_prescricao_dias = tempo_decorrido_para_prescricao - tempo_suspensao_dias

            # converte o tempo residual para anos
            tempo_decorrido_para_prescricao = converte_dias_para_anos_mais_um(tempo_efetiva_prescricao_dias)

            print(f"Recebimento da denuncia: {dicionario['recebimento_denuncia_bool']}")

            crime_analisado = dicionario['crime']

            if tempo_decorrido_para_prescricao > dic_prescricao[crime_analisado]:
                parecer = f'''                
                       Ref. ao processo: {processo}\n 
                       Investigado(a): {reu}
                       \n\n  
                        
                       MM. Juíza,\n\n            
                       In casu, verifica-se que o(s) delito(s) investigado(s) possui(em) prazo prescricional máximo de {dic_prescricao[crime_analisado]} anos ({crime_analisado}), considerando a idade da parte autora.\n
                       Uma vez que os fatos datam de {corrige_ordem_da_data_str(dicionario['data_fato'])}, forçoso reconhecer a incidência da prescrição.\n            
                       Insta pontuar que se operou causa de suspensão da prescrição da data do fato até a presente data, tendo sido considerado o tempo de {tempo_suspensao_dias} dias no cálculo, a título de decote.\n            
                       Ante o exposto, o MP requer o reconhecimento da extinção da punibilidade, nos termos do art. 107, inciso IV, do CP.\n            
                       Pede deferimento.\n            
                       '''

                resultado['Decurso de prazo prescricional (arredondado em anos)'] = tempo_decorrido_para_prescricao
                resultado['prazo_prescricao'] = dic_prescricao[crime_analisado]
                resultado['tempo_suspensao'] = tempo_suspensao_dias
                resultado['resultado'] = True

                resultado['Data da prescrição'] = calcula_data_prescricao(dicionario['data_fato'],
                                                                          dic_prescricao[crime_analisado],
                                                                          reduz_metade=reducao_da_prescricao_metade,
                                                                          periodo_suspenso=tempo_suspensao_dias)

                return resultado, parecer

            else:
                parecer = f'''
                                  Ref. ao processo: {processo}\n 
                                  Investigado(a): {reu} 
                                  \n\n    
                                    
                                  MM. Juíza,\n\n            
                                  In casu, verifica-se que o(s) delito(s) investigado(s) possui(em) prazo prescricional máximo de {dic_prescricao[crime_analisado]} anos ({crime_analisado}), considerando a idade da parte autora.\n
                                  Uma vez que os fatos datam de {corrige_ordem_da_data_str(dicionario['data_fato'])}, forçoso reconhecer que não houve a incidência da prescrição.\n            
                                  Insta pontuar que foi considerado no cálculo o tempo no qual ocorreu a suspensão da prescrição, o que ensejou o decote do interregno de {abs(tempo_suspensao_dias)} dias.\n
                                  Não houve oferecimento de denúncia e regular recebimento da peça acusatória, apto à interrupção do prazo prescricional.\n             
                                  Ante o exposto, o MP requer o prosseguimento do feito.\n            
                                  Pede deferimento.\n            
                                  '''

                resultado['Decurso de prazo prescricional (arredondado em anos)'] = tempo_decorrido_para_prescricao
                resultado['prazo_prescricao'] = dic_prescricao[crime_analisado]
                resultado['tempo_suspensao'] = tempo_suspensao_dias
                resultado['resultado'] = False

                resultado['Data da prescrição'] = calcula_data_prescricao(dicionario['data_fato'],
                                                                          dic_prescricao[crime_analisado],
                                                                          reduz_metade=reducao_da_prescricao_metade,
                                                                          periodo_suspenso=tempo_suspensao_dias)

                return resultado, parecer


        # analisa tendo havido recebimento da denuncia
        elif dicionario['recebimento_denuncia_bool'] == True:

            print(f"Recebimento da denuncia: {dicionario['recebimento_denuncia_bool']}")

            # seta tempo decorrido, considerando a data do fato
            print('Inicializando análise')
            crime_analisado = dicionario['crime']

            print('Analisando entre data do fato e data recebimento da denuncia:')
            tempo_decorrido_para_prescricao = calcula_diferenca_entre_duas_datas(dicionario['data_fato'],
                                                                                 dicionario[
                                                                                     'Dt_Denuncia'])

            # analisa entre a data do fato e o recebimento da denúncia
            if tempo_decorrido_para_prescricao > dic_prescricao[crime_analisado]:
                parecer = f'''
                       Ref. ao processo: {processo}\n 
                       Investigado(a): {reu}  
                       \n\n  

                       MM. Juíza,\n\n            
                       In casu, verifica-se que o(s) delito(s) investigado(s) possui(em) prazo prescricional máximo de {dic_prescricao[crime_analisado]} anos ({crime_analisado}), considerando a idade da parte autora (CP, Art. 115).\n
                       Uma vez que os fatos datam de {corrige_ordem_da_data_str(dicionario['data_fato'])}, forçoso reconhecer a incidência da prescrição.\n            
                       Insta pontuar que a denúncia foi recebida em {corrige_ordem_da_data_str(dicionario['Dt_Denuncia'])} mas antes desta causa interruptiva, o jus puniendi estatal já se encontrava prescrito, uma vez ter decorrido {tempo_decorrido_para_prescricao} anos após a data do fato.\n            
                       Foi considerado no cálculo o tempo no qual ocorreu a suspensão da prescrição, o que ensejou o decote do interregno de {abs(tempo_suspensao_dias)} dias.\n
                       Ante o exposto, o MP requer o reconhecimento da extinção da punibilidade, nos termos do art. 107, inciso IV, do CP.\n            
                       Pede deferimento.\n            
                       '''

                resultado['Decurso de prazo prescricional (arredondado em anos)'] = tempo_decorrido_para_prescricao
                resultado['prazo_prescricao'] = dic_prescricao[crime_analisado]
                resultado['tempo_suspensao'] = tempo_suspensao_dias
                resultado['resultado'] = True
                resultado['Data da prescrição'] = calcula_data_prescricao(dicionario['data_fato'],
                                                                          dic_prescricao[crime_analisado],
                                                                          reduz_metade=reducao_da_prescricao_metade,
                                                                          periodo_suspenso=tempo_suspensao_dias)

                return resultado, parecer

            # analisa entre o recebimento da denúncia e a presente data

            print('Analisando entre data do recebimento da denuncia e a data atual:')

            tempo_decorrido_para_prescricao = calcula_diferenca_entre_data_ate_atual_em_dias(
                dicionario['Dt_Denuncia'])

            # calcula tempo de suspensao em dias
            tempo_suspensao_dias = (dicionario['Dt_inicio_suspensao'] - dicionario['Dt_fim_suspensao']).days

            # desconta o tempo que o processo esteve suspenso
            tempo_efetiva_prescricao_dias = tempo_decorrido_para_prescricao - tempo_suspensao_dias

            # converte o tempo residual para anos
            tempo_decorrido_para_prescricao = converte_dias_para_anos_mais_um(tempo_efetiva_prescricao_dias)

            # analisa entre a data do recebimento da denúncia e a data atual
            if tempo_decorrido_para_prescricao > dic_prescricao[crime_analisado]:
                parecer = f'''
                                  Ref. ao processo: {processo}\n 
                                  Investigado(a): {reu} 
                                  \n\n  

                                  MM. Juíza,\n\n            
                                  In casu, verifica-se que o(s) delito(s) investigado(s) possui(em) prazo prescricional máximo de {dic_prescricao[crime_analisado]} anos ({crime_analisado}), considerando a idade da parte autora (CP, Art. 115).\n
                                  Uma vez que os fatos datam de {corrige_ordem_da_data_str(dicionario['data_fato'])}, forçoso reconhecer a incidência da prescrição.\n            
                                  Insta pontuar que a denúncia foi recebida em {corrige_ordem_da_data_str(dicionario['Dt_Denuncia'])} tendo, após esta causa interruptiva se operado a prescrição do jus puniendi estatal, uma vez ter decorrido {tempo_decorrido_para_prescricao} anos após tal causa interruptiva.\n            
                                  Foi considerado no cálculo o tempo no qual ocorreu a suspensão da prescrição, o que ensejou o decote do interregno de {abs(tempo_suspensao_dias)} dias.\n
                                  Ante o exposto, o MP requer o reconhecimento da extinção da punibilidade, nos termos do art. 107, inciso IV, do CP.\n            
                                  Pede deferimento.\n            
                                  '''

                resultado['Decurso de prazo prescricional (arredondado em anos)'] = tempo_decorrido_para_prescricao
                resultado['prazo_prescricao'] = dic_prescricao[crime_analisado]
                resultado['tempo_suspensao'] = tempo_suspensao_dias
                resultado['resultado'] = True
                resultado['Data da prescrição'] = calcula_data_prescricao(dicionario['Dt_Denuncia'],
                                                                          dic_prescricao[crime_analisado],
                                                                          reduz_metade=reducao_da_prescricao_metade,
                                                                          periodo_suspenso=tempo_suspensao_dias)

                return resultado, parecer

            else:
                parecer = f"""
                            Ref. ao processo: {processo}\n 
                            Investigado(a): {reu} 
                            \n\n  

                            MM. Juíza,\n\n  
                            Não prescreveu entre a data do fato e a data do recebimento da denuncia. 
                            Não prescreveu entre a data do recebimento da denuncia e a data atual."""

                resultado['Decurso de prazo prescricional (arredondado em anos)'] = tempo_decorrido_para_prescricao
                resultado['prazo_prescricao'] = dic_prescricao[crime_analisado]
                resultado['tempo_suspensao'] = tempo_suspensao_dias
                resultado['resultado'] = False
                resultado['Data da prescrição'] = calcula_data_prescricao(dicionario['Dt_Denuncia'],
                                                                          dic_prescricao[crime_analisado],
                                                                          reduz_metade=reducao_da_prescricao_metade,
                                                                          periodo_suspenso=tempo_suspensao_dias)
                return resultado, parecer


def converte_dic_dataframe_vertical(dicionario_final: dict):
    # convert o dicionario para um DataFrame
    df = pd.DataFrame([dicionario_final])

    # Transponha o DataFrame
    df = df.transpose()

    # Remova o nome da coluna
    df.columns = ['']

    return df


def normaliza_key_dic_dados_informados(dicionario_corrigir: dict) -> dict:
    dicionario_normalizado = {}

    if 'data_fato' in dicionario_corrigir:
        dicionario_normalizado['Data do Fato'] = dicionario_corrigir.pop('data_fato')

    if 'crime' in dicionario_corrigir:
        dicionario_normalizado['Crime'] = dicionario_corrigir.pop('crime')

    if 'recebimento_denuncia_bool' in dicionario_corrigir:
        dicionario_normalizado['Recebimento da Denúncia?'] = dicionario_corrigir.pop('recebimento_denuncia_bool')

    if 'Dt_Denuncia' in dicionario_corrigir:
        dicionario_normalizado['Data de recebimento da Denúncia'] = dicionario_corrigir.pop('Dt_Denuncia')

    if 'suspensao_prescricao_bool' in dicionario_corrigir:
        dicionario_normalizado['Prescrição foi suspensa?'] = dicionario_corrigir.pop('suspensao_prescricao_bool')

    if 'Dt_inicio_suspensao' in dicionario_corrigir:
        dicionario_normalizado['Data do início da suspensão'] = dicionario_corrigir.pop('Dt_inicio_suspensao')

    if 'Dt_fim_suspensao' in dicionario_corrigir:
        dicionario_normalizado['Data do fim da suspensão'] = dicionario_corrigir.pop('Dt_fim_suspensao')

    if 'verificacao_idade' in dicionario_corrigir:
        dicionario_normalizado['Houve verificação da idade do autor do fato?'] = dicionario_corrigir.pop(
            'verificacao_idade')

    if 'idade_autor' in dicionario_corrigir:
        dicionario_normalizado['Data de nascimento do autor do fato'] = dicionario_corrigir.pop('idade_autor')

    if 'Pena in concreto' in dicionario_corrigir:
        pena_in_concreto = dicionario_corrigir['Pena in concreto']
        dicionario_normalizado['Pena in concreto'] = f"{pena_in_concreto[0]} ano(s) e {pena_in_concreto[1]} mês(es)"

    return dicionario_normalizado


def normaliza_value_dic_dados_informados(dicionario_corrigir: dict) -> dict:
    dicionario_normalizado = dict(dicionario_corrigir)

    for key, valores in dicionario_corrigir.items():

        if isinstance(valores, date):
            dicionario_normalizado[key] = valores.strftime('%d/%m/%Y')

        if valores == True:
            dicionario_normalizado[key] = "Sim"

        if valores == False:
            dicionario_normalizado[key] = "Não"

    return dicionario_normalizado


def normaliza_key_dic_dados_calculados(dicionario_corrigir: dict) -> dict:
    dicionario_normalizado = dicionario_corrigir

    if 'prazo_prescricao' in dicionario_corrigir:
        dicionario_normalizado['Prescrição do crime (anos):'] = dicionario_corrigir.pop('prazo_prescricao')

    if 'tempo_suspensao' in dicionario_corrigir:
        dicionario_normalizado['Tempo de suspensão (dias):'] = dicionario_corrigir.pop('tempo_suspensao')

    if 'resultado' in dicionario_corrigir:
        dicionario_normalizado['Crime prescreveu?'] = dicionario_corrigir.pop('resultado')

    if 'Idade atual do autor (anos)' in dicionario_corrigir:
        dicionario_normalizado['Idade atual do autor (anos)'] = dicionario_corrigir['Idade atual do autor (anos)']

    if 'Idade do autor na data do fato (anos)' in dicionario_corrigir:
        dicionario_normalizado['Idade do autor na data do fato (anos)'] = dicionario_corrigir[
            'Idade do autor na data do fato (anos)']

    return dicionario_normalizado


def normaliza_value_dic_dados_calculados(dicionario_corrigir: dict) -> dict:
    dicionario_normalizado = dicionario_corrigir

    for key, valores in dicionario_corrigir.items():

        if isinstance(valores, int):
            dicionario_normalizado[key] = abs(valores)

        if valores is True:
            dicionario_normalizado[key] = "Sim"

        if valores is False:
            dicionario_normalizado[key] = "Não"

    return dicionario_normalizado
