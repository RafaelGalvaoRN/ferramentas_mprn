from datetime import datetime, date
import pandas as pd


dic_prescricao ={'Ameaça': 3, 'Infanticídio': 12, "Lesão Corporal": 4,
                  "Lesão Grave": 12, "Lesão Gravíssima": 12, "Homicídio simples": 20,
                  "Homicídio qualificado": 20, "Feminicídio": 20, "Homicídio culposo": 8,
                  "Induzimento, instigação ou auxílio a suicídio ou a automutilação": 4, "Calunia": 4,
                  "Difamação": 3, "Injúria": 3, "Abandono de incapaz": 8,
                  "Abandono de incapaz com resultado de lesão grave": 12,
                  "Abandono de incapaz  com resultado de lesão grave": 20, "Exposição ou abandono de recém-nascido": 4,
                  "Exposição ou abandono de recém-nascido com lesão grave": 8,
                  "Exposição ou abandono de recém-nascido com morte": 12,
                  "Omissão de socorro": 3, "Omissão de socorro com lesão grave": 3, "Omissão de socorro com morte": 4,
                  "Condicionamento de atendimento médico-hospitalar emergencial": 3, "Maus tratos": 4,
                  "Maus tratos com lesão grave": 8,
                  "Maus tratos com morte": 16, "Rixa": 3, "Rixa com morte ou lesão grave": 4, "Injúria Racial": 8,
                  "Constrangimento ilegal": 3,
                  "Perseguição": 4, "Perseguição majorada": 8, "Violência psicológica contra a mulher": 4,
                  "Sequestro e cárcere privado": 8, "Sequestro e cárcere privado majorado": 12,
                  "Sequestro e cárcere privado com grave sofrimento físico ou moral": 12,
                  "Redução a condição análoga à de escravo": 12, "Redução a condição análoga à de escravo majorado": 16,
                  "Tráfico de Pessoas": 12, "Tráfico de pessoas majorado": 16, "Violação de domicílio": 3,
                  "Violação de domicílio majorado": 4, "Violação de correspondência": 3,
                  "Sonegação ou destruição de correspondência": 3, "Divulgação de segredo": 3,
                  "Divulgação de informações sigilosas da Administração Pública": 8,
                  "Violação do segredo profissional": 3, "Invasão de dispostitivo informático": 8, "Furto": 8,
                  "Furto durante repouso noturno": 12, "Furto qualificado": 12, "Furto com emprego de explosivo": 16,
                  "Furto mediante fraude e por meio de dispositivo eletrônico ou informático": 12,
                  "Furto de veículo automotor com transporte interestadual": 12,
                  "Furto de semovente": 12, "Furto de substância explosiva": 16, "Furto de coisa comum": 4,
                  "Roubo": 16, "Roubo majorado": 16, "Latrocínio": 20, "Extorsão": 16,
                  "Extorsão mediante sequestro": 20,
                  "Extorsão indireta": 8, "Dano": 3, "Dano qualificado": 8, "Apropriação Indébita": 8,
                  "Apropriação Indébita Previdenciária": 12,
                  "Estelionato": 8, "Estelionato Eletrônico": 12, "Abuso de Incapazes": 12, "Receptação": 8,
                  "Receptação qualificada": 12,
                  "Receptação de animal": 12, "Estupro": 16, "Violação sexual mediante fraude": 12,
                  "Importunação sexual": 12,
                  "Assédio Sexual": 4, "Registro não autorizado da intimidade sexual": 3, "Estupro de vulnerável": 20,
                  "Corrupção de menores": 12,
                  "Satisfação de lascívia mediante presença de criança ou adolescente": 8,
                  "Favorecimento da prostituição ou de outra forma de exploração sexual de criança ou adolescente ou de vulnerável": 16,
                  "Divulgação de cena de estupro": 12, "Divulgação de cena de estupro majorada": 12,
                  "Mediação para servir a lascívia de outrem": 8,
                  "Mediação para servir a lascívia de outrem contra vítima menor": 12,
                  "Mediação para servir a lascívia de outrem com violência": 12,
                  "Favorecimento da prostituição": 12, "Casa de prostituição": 12, "Rufianismo": 8,
                  "Rufianismo contra vítima menor": 12,
                  "Rufianismo com violência": 12, "Ato obsceno": 3, "Escrito obseceno": 4, "Bigamia": 12,
                  "Registro de nascimento inexistente": 12,
                  "Parto suposto": 12, "Sonegação de estado de filiação": 12, "Abandono material": 8,
                  "Entrega de filho menor a pessoa inidônea": 4,
                  "Abandono intelectual": 3, "Induzimento a fuga, entrega arbitrária ou sonegação de incapazes": 3,
                  "Subtração de incapazes": 4,
                  "Incêndio": 12, "Explosão": 12, "Incitação ao crime": 3, "Apologia de crime": 3,
                  "Associação criminosa": 8, "Constituição de milicia privada": 12,
                  "Falsificação de documento público": 12, "Falsificação de documento particular": 12,
                  "Falsidade ideológica": 12, "Falsidade de atestado médico": 3,
                  "Fraudes em certames de interesse público": 8,
                  "Fraudes em certames de interesse público com dano à administração": 12, "Peculato": 20,
                  "Peculato culposo": 3,
                  "Peculato mediante erro de outrem": 8, "Inserção de dados falsos em sistema de informações": 20,
                  "Modificação ou alteração não autorizada de sistema de informações": 4,
                  "Extravio, sonegaçãoo ou inutilização de livro ou documento": 8,
                  "emprego irregular de verbas públicas": 3, "Concussão": 20, "Corrupção passiva": 20,
                  "Facilitação de contrabando ou descaminho": 12, "Prevaricação": 3, "Condescendência criminosa": 3,
                  "Advocacia administrativa": 3, "Violência arbitrária": 8, "Abandono de Função": 3,
                  "Exercício funcional ilegalmente antecipado ou prolongado": 3, "Violação de sigilo funcional": 4,
                  "Usurpação de função pública": 4, "Usurpação de função pública com vantagem": 12, "Resistência": 4,
                  "Resistência qualificada": 4, "Desobediência": 3,
                  "Desacato": 4, "Tráfico de influência": 8, "Corrupção ativa": 20, "Contrabando": 12,
                  "Contratação direta ilegal": 12, "Frustração do caráter competititvo da licitação": 12,
                  "Patrocínio de contratação indevida": 8,
                  "Modificação ou pagamento irregular em contrato administrativo": 12,
                  "Perturbação de processo licitatório": 8,
                  "Violação de siligilo de licitação": 8, "Afastamento de licitante": 12,
                  "Fraude em licitação ou contrato": 12, "Contratação inidônea": 8, "Contratação inidônea majorada": 12,
                  "Impedimento indevido": 4,
                  "Omissão grave de dado ou de informação por projetista": 8, "Denunciação caluniosa": 12,
                  "Comunicação falsa de crime ou de contravenção": 3, "Auto-acusação falsa": 4,
                  "Falso testemunho ou falsa perícia": 8, "Coação no curso do processo": 8,
                  "Exercício arbitrário das próprias razões": 3, "Fraude processual": 4, "Favorecimento pessoal": 3,
                  "Favorecimento real": 3, "Ingressar aparelho telefônico em estabelecimento prisional": 3,
                  "Fuga de pessoa presa ou submetida a medida de segurança": 4,
                  "Evasão nediante violência contra a pessoa": 3, "Arrebatamento de preso": 8, "Motim de presos": 4,
                  "Patrocínio infiel": 8, "Exploração de prestígio": 12,

                 ## Lei maria da penha

                 "Descumprimento de decisão judicial que defere MPU": 4,

                 ## lei de drogas

                 "Art. 33": 20, "Art. 33, §2": 8, "Art. 33, §3": 3, "Art. 34": 16,
                 "Art. 35": 16, "Art. 36": 20, "Art. 37": 12, "Art. 38":4, "Art. 39":8,

                 }

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

def analisa_prescricao(dicionario: dict):
    # verifica se o crime está cadastrado e, não estando - manda msg e encerra


    resultado = {}
    reducao_da_prescricao_metade = 1



    if dicionario['crime'] not in dic_prescricao:
        print(f" Crime {dicionario['crime']} não cadastrado na base de dados")
        return 0



    if dicionario['verificacao_idade'] == True:

        if calcula_se_e_menor_21_tempo_crime(dicionario['idade_autor'],
                                             dicionario['data_fato']) or calcula_se_e_maior_de_setenta_anos(
                dicionario['idade_autor']):

            reducao_da_prescricao_metade = 1/2



    if dicionario['suspensao_prescricao_bool'] == False:


        # analisa sem ter havido recebimento da denuncia
        if dicionario['recebimento_denuncia_bool'] == False:

            # seta tempo decorrido, considerando a data do fato
            tempo_decorrido_para_prescricao = calcula_diferenca_entre_data_ate_atual(dicionario['data_fato']) * reducao_da_prescricao_metade

            crime_analisado = dicionario['crime']

            if tempo_decorrido_para_prescricao > dic_prescricao[crime_analisado]:
                parecer = f'''
                MM. Juíza,\n\n            
                In casu, verifica-se que o(s) delito(s) investigado(s) possui(em) prazo prescricional máximo de {dic_prescricao[crime_analisado]} anos ({crime_analisado}).\n
                Uma vez que os fatos datam de {corrige_ordem_da_data_str(dicionario['data_fato'])}, forçoso reconhecer a incidência da prescrição.\n            
                Insta pontuar que não se operou nenhuma causa de suspensão da prescrição da data do fato até a presente data.\n            
                Ante o exposto, o MP requer o reconhecimento da extinção da punibilidade, nos termos do art. 107, inciso IV, do CP.\n            
                Pede deferimento.\n            
                '''

                resultado['tempo_decorrido_para_prescricao'] = tempo_decorrido_para_prescricao
                resultado['prazo_prescricao'] = dic_prescricao[crime_analisado]
                resultado['resultado'] = True
                return resultado, parecer


            else:
                parecer = f'''
                           MM. Juíza,\n\n            
                           In casu, verifica-se que o(s) delito(s) investigado(s) possui(em) prazo prescricional máximo de {dic_prescricao[crime_analisado]} anos ({crime_analisado}).\n
                           Uma vez que os fatos datam de {corrige_ordem_da_data_str(dicionario['data_fato'])}, forçoso reconhecer que não houve a incidência da prescrição.\n            
                           Insta pontuar que não se operou nenhuma causa de suspensão ou interrupção da prescrição da data do fato até a presente data.\n
                           Não houve oferecimento de denúncia e regular recebimento da peça acusatória, apto à interrupção do prazo prescricional.\n             
                           Ante o exposto, o MP requer o prosseguimento do feito.\n            
                           Pede deferimento.\n            
                           '''

                resultado['tempo_decorrido_para_prescricao'] = tempo_decorrido_para_prescricao
                resultado['prazo_prescricao'] = dic_prescricao[crime_analisado]
                resultado['resultado'] = False
                return resultado, parecer

        # analisa tendo havido recebimento da denuncia
        elif dicionario['recebimento_denuncia_bool'] == True:

            # seta tempo decorrido, considerando a data do fato
            print('Inicializando análise')
            crime_analisado = dicionario['crime']

            print('Analisando entre data do fato e data recebimento da denuncia:')
            tempo_decorrido_para_prescricao = calcula_diferenca_entre_duas_datas(dicionario['data_fato'],
                                                                                 dicionario['Dt_Denuncia']) * reducao_da_prescricao_metade

            print(tempo_decorrido_para_prescricao)

            # analisa entre a data do fato e o recebimento da denúncia
            if tempo_decorrido_para_prescricao > dic_prescricao[crime_analisado]:
                parecer = f'''

                MM. Juíza,\n\n            
                In casu, verifica-se que o(s) delito(s) investigado(s) possui(em) prazo prescricional máximo de {dic_prescricao[crime_analisado]} anos ({crime_analisado}).\n
                Uma vez que os fatos datam de {corrige_ordem_da_data_str(dicionario['data_fato'])}, forçoso reconhecer a incidência da prescrição.\n            
                Insta pontuar que a denúncia foi recebida em {corrige_ordem_da_data_str(dicionario['Dt_Denuncia'])} mas antes desta causa interruptiva, o jus puniendi estatal já se encontrava prescrito, uma vez ter decorrido {tempo_decorrido_para_prescricao} anos após a data do fato.\n            
                Ante o exposto, o MP requer o reconhecimento da extinção da punibilidade, nos termos do art. 107, inciso IV, do CP.\n            
                Pede deferimento.\n           
                
                '''

                resultado['tempo_decorrido_para_prescricao'] = tempo_decorrido_para_prescricao
                resultado['prazo_prescricao'] = dic_prescricao[crime_analisado]
                resultado['resultado'] = True
                return resultado, parecer


            print('Analisando entre data do recebimento da denuncia e a data atual:')
            tempo_decorrido_para_prescricao = calcula_diferenca_entre_data_ate_atual(dicionario['Dt_Denuncia']) * reducao_da_prescricao_metade

            # analisa entre a data do recebimento da denúncia e a data atual
            if tempo_decorrido_para_prescricao > dic_prescricao[crime_analisado]:
                parecer = f'''

                           MM. Juíza,\n\n            
                           In casu, verifica-se que o(s) delito(s) investigado(s) possui(em) prazo prescricional máximo de {dic_prescricao[crime_analisado]} anos ({crime_analisado}).\n
                           Uma vez que os fatos datam de {corrige_ordem_da_data_str(dicionario['data_fato'])}, forçoso reconhecer a incidência da prescrição.\n            
                           Insta pontuar que a denúncia foi recebida em {dicionario['Dt_Denuncia']} tendo, após esta causa interruptiva se operado a prescrição do jus puniendi estatal, uma vez ter decorrido {tempo_decorrido_para_prescricao} anos após tal causa interruptiva.\n            
                           Ante o exposto, o MP requer o reconhecimento da extinção da punibilidade, nos termos do art. 107, inciso IV, do CP.\n            
                           Pede deferimento.\n            
                           '''

                resultado['tempo_decorrido_para_prescricao'] = tempo_decorrido_para_prescricao
                resultado['prazo_prescricao'] = dic_prescricao[crime_analisado]
                resultado['resultado'] = True
                return resultado, parecer


            else:
                parecer = 'Não prescreveu entre a data do fato e a data de recebimento da denuncia. ' \
                          'Não prescreveu entre a data de recebimento da denúncia e a data atual.'
                resultado['tempo_decorrido_para_prescricao'] = tempo_decorrido_para_prescricao
                resultado['prazo_prescricao'] = dic_prescricao[crime_analisado]
                resultado['resultado'] = False
                return resultado, parecer


    elif dicionario['suspensao_prescricao_bool'] == True:
        tempo_suspensao_dias = dicionario['Dt_inicio_suspensao'] - dicionario['Dt_fim_suspensao']
        tempo_suspensao_dias = tempo_suspensao_dias.days

        print(f'Tempo de suspensao calculado em dias: {tempo_suspensao_dias}')

        # analisa sem ter havido recebimento da denuncia
        if dicionario['recebimento_denuncia_bool'] == False:
            # seta tempo decorrido, considerando a data do fato
            tempo_decorrido_para_prescricao = calcula_diferenca_entre_data_ate_atual_em_dias(dicionario['data_fato']) * reducao_da_prescricao_metade
            # calcula tempo de suspensao em dias
            print('')
            tempo_suspensao_dias = (dicionario['Dt_inicio_suspensao'] - dicionario['Dt_fim_suspensao']).days

            # desconta o tempo que o processo esteve suspenso
            tempo_efetiva_prescricao_dias = tempo_decorrido_para_prescricao - tempo_suspensao_dias

            # converte o tempo residual para anos
            tempo_decorrido_para_prescricao = converte_dias_para_anos_mais_um(tempo_efetiva_prescricao_dias)

            print(f"Recebimento da denuncia: {dicionario['recebimento_denuncia_bool']}")

            crime_analisado = dicionario['crime']

            if tempo_decorrido_para_prescricao > dic_prescricao[crime_analisado]:
                parecer = f'''
                       MM. Juíza,\n\n            
                       In casu, verifica-se que o(s) delito(s) investigado(s) possui(em) prazo prescricional máximo de {dic_prescricao[crime_analisado]} anos ({crime_analisado}).\n
                       Uma vez que os fatos datam de {corrige_ordem_da_data_str(dicionario['data_fato'])}, forçoso reconhecer a incidência da prescrição.\n            
                       Insta pontuar que se operou causa de suspensão da prescrição da data do fato até a presente data, tendo sido considerado o tempo de {tempo_suspensao_dias} dias no cálculo, a título de decote.\n            
                       Ante o exposto, o MP requer o reconhecimento da extinção da punibilidade, nos termos do art. 107, inciso IV, do CP.\n            
                       Pede deferimento.\n            
                       '''

                resultado['tempo_decorrido_para_prescricao'] = tempo_decorrido_para_prescricao
                resultado['prazo_prescricao'] = dic_prescricao[crime_analisado]
                resultado['tempo_suspensao'] = tempo_suspensao_dias
                resultado['resultado'] = True
                return resultado, parecer

            else:
                parecer = f'''
                                  MM. Juíza,\n\n            
                                  In casu, verifica-se que o(s) delito(s) investigado(s) possui(em) prazo prescricional máximo de {dic_prescricao[crime_analisado]} anos ({crime_analisado}).\n
                                  Uma vez que os fatos datam de {corrige_ordem_da_data_str(dicionario['data_fato'])}, forçoso reconhecer que não houve a incidência da prescrição.\n            
                                  Insta pontuar que foi considerado no cálculo o tempo no qual ocorreu a suspensão da prescrição da data do fato até a presente data, o que ensejou o decote do interregno de {tempo_suspensao_dias} anos.\n
                                  Não houve oferecimento de denúncia e regular recebimento da peça acusatória, apto à interrupção do prazo prescricional.\n             
                                  Ante o exposto, o MP requer o prosseguimento do feito.\n            
                                  Pede deferimento.\n            
                                  '''

                resultado['tempo_decorrido_para_prescricao'] = tempo_decorrido_para_prescricao
                resultado['prazo_prescricao'] = dic_prescricao[crime_analisado]
                resultado['tempo_suspensao'] = tempo_suspensao_dias
                resultado['resultado'] = True
                return resultado, parecer


        # analisa tendo havido recebimento da denuncia
        elif dicionario['recebimento_denuncia_bool'] == True:

            print(f"Recebimento da denuncia: {dicionario['recebimento_denuncia_bool']}")

            # seta tempo decorrido, considerando a data do fato
            print('Inicializando análise')
            crime_analisado = dicionario['crime']

            print('Analisando entre data do fato e data recebimento da denuncia:')
            tempo_decorrido_para_prescricao = calcula_diferenca_entre_duas_datas(dicionario['data_fato'],
                                                                                 dicionario['Dt_Denuncia']) * reducao_da_prescricao_metade

            # analisa entre a data do fato e o recebimento da denúncia
            if tempo_decorrido_para_prescricao > dic_prescricao[crime_analisado]:
                parecer = f'''

                       MM. Juíza,\n\n            
                       In casu, verifica-se que o(s) delito(s) investigado(s) possui(em) prazo prescricional máximo de {dic_prescricao[crime_analisado]} anos ({crime_analisado}).\n
                       Uma vez que os fatos datam de {corrige_ordem_da_data_str(dicionario['data_fato'])}, forçoso reconhecer a incidência da prescrição.\n            
                       Insta pontuar que a denúncia foi recebida em {corrige_ordem_da_data_str(dicionario['Dt_Denuncia'])} mas antes desta causa interruptiva, o jus puniendi estatal já se encontrava prescrito, uma vez ter decorrido {tempo_decorrido_para_prescricao} anos após a data do fato.\n            
                       Foi considerado no cálculo o tempo no qual ocorreu a suspensão da prescrição da data do fato até a presente data, o que ensejou o decote do interregno de {tempo_suspensao_dias} anos.\n
                       Ante o exposto, o MP requer o reconhecimento da extinção da punibilidade, nos termos do art. 107, inciso IV, do CP.\n            
                       Pede deferimento.\n            
                       '''

                resultado['tempo_decorrido_para_prescricao'] = tempo_decorrido_para_prescricao
                resultado['prazo_prescricao'] = dic_prescricao[crime_analisado]
                resultado['tempo_suspensao'] = tempo_suspensao_dias
                resultado['resultado'] = True
                return resultado, parecer


            # analisa entre o recebimento da denúncia e a presente data

            print('Analisando entre data do recebimento da denuncia e a data atual:')

            tempo_decorrido_para_prescricao = calcula_diferenca_entre_data_ate_atual_em_dias(dicionario['Dt_Denuncia']) * reducao_da_prescricao_metade
            # calcula tempo de suspensao em dias
            tempo_suspensao_dias = (dicionario['Dt_inicio_suspensao'] - dicionario['Dt_fim_suspensao']).days

            # desconta o tempo que o processo esteve suspenso
            tempo_efetiva_prescricao_dias = tempo_decorrido_para_prescricao - tempo_suspensao_dias

            # converte o tempo residual para anos
            tempo_decorrido_para_prescricao = converte_dias_para_anos_mais_um(tempo_efetiva_prescricao_dias)

            # analisa entre a data do recebimento da denúncia e a data atual
            if tempo_decorrido_para_prescricao > dic_prescricao[crime_analisado]:
                parecer = f'''

                                  MM. Juíza,\n\n            
                                  In casu, verifica-se que o(s) delito(s) investigado(s) possui(em) prazo prescricional máximo de {dic_prescricao[crime_analisado]} anos ({crime_analisado}).\n
                                  Uma vez que os fatos datam de {corrige_ordem_da_data_str(dicionario['data_fato'])}, forçoso reconhecer a incidência da prescrição.\n            
                                  Insta pontuar que a denúncia foi recebida em {corrige_ordem_da_data_str(dicionario['Dt_Denuncia'])} tendo, após esta causa interruptiva se operado a prescrição do jus puniendi estatal, uma vez ter decorrido {tempo_decorrido_para_prescricao} anos após tal causa interruptiva.\n            
                                  Foi considerado no cálculo o tempo no qual ocorreu a suspensão da prescrição da data do fato até a presente data, o que ensejou o decote do interregno de {tempo_suspensao_dias} anos.\n
                                  Ante o exposto, o MP requer o reconhecimento da extinção da punibilidade, nos termos do art. 107, inciso IV, do CP.\n            
                                  Pede deferimento.\n            
                                  '''

                resultado['tempo_decorrido_para_prescricao'] = tempo_decorrido_para_prescricao
                resultado['prazo_prescricao'] = dic_prescricao[crime_analisado]
                resultado['tempo_suspensao'] = tempo_suspensao_dias
                resultado['resultado'] = True
                return resultado, parecer

            else:
                parecer = 'Não prescreveu entre a data do fato e a data do recebimento da denuncia. ' \
                          'Não prescreveu entre a data do recebimento da denuncia e a data atual'
                resultado['tempo_decorrido_para_prescricao'] = tempo_decorrido_para_prescricao
                resultado['prazo_prescricao'] = dic_prescricao[crime_analisado]
                resultado['tempo_suspensao'] = tempo_suspensao_dias
                resultado['resultado'] = False
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
    dicionario_normalizado ={}


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
        dicionario_normalizado['Houve verificação da idade do autor do fato?'] = dicionario_corrigir.pop('verificacao_idade')

    if 'idade_autor' in dicionario_corrigir:
        dicionario_normalizado['Data de nascimento do autor do fato'] = dicionario_corrigir.pop('idade_autor')

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

    print('aqyu')
    print(dicionario_corrigir)

    dicionario_normalizado = {}

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

    dicionario_normalizado = {}


    for key, valores in dicionario_corrigir.items():

        if isinstance(valores, int):
            dicionario_normalizado[key] = abs(valores)

        if valores == True:
            dicionario_normalizado[key] = "Sim"

        if valores == False:
            dicionario_normalizado[key] = "Não"

    return dicionario_normalizado