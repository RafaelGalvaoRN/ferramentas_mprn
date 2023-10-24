





codigo_penal = {'Homicídio simples - Art. 121': 20,
                'Homicídio simples privilegiado - Art. 121, §1º': 16.8,
                "Homicídio qualificado - Art 121, §2º": 30,
                "Homicídio culposo - 121, §3º ": 3,
                "Induzimento, instigação ou auxílio a suicídio ou a automutilação - Art. 122": 2,
                "Induzimento, instigação ou auxílio a suicídio ou a automutilação qualificada - Art. 122, §1º": 3,
                "Induzimento, instigação ou auxílio a suicídio ou a automutilação com morte - Art. 122, º 2": 6,
                "Infanticídio - Art. 123": 6,
                "Aborto provocado pela gestante ou com seu consentimento - Art. 124": 3,
                "Aborto provocado por terceiro, sem conhecimento da gestante - Art. 125": 10,
                "Aborto provocado por terceiro, com o conhecimento da gestante - Art. 126": 4,

                "Lesão Corporal - Art 129": 1,
                "Lesão Corporal grave - Art 129, §1": 5,
                "Lesão Corporal gravíssima - Art 129, §2": 8,
                "Lesão Corporal seguida de morte - Art 129, §3": 12,
                "Lesão Corporal culposa - Art 129, §6": 1,


                "Lesão Corporal em contexto de violência doméstica - Art 129, §9": 3,



                "Abandono de incapaz - Art. 133": 3,
                "Abandono de incapaz com resultado de lesão grave - Art. 133, §1º": 5,
                "Abandono de incapaz com resultado morte - Art. 133, §1º": 12,
                "Exposição ou abandono de recém-nascido - Art. 134": 2,
                "Exposição ou abandono de recém-nascido com lesão grave - Art. 134, §1º": 3,
                "Exposição ou abandono de recém-nascido com morte - Art. 134, §2º": 6,
                "Omissão de socorro - Art. 135": 0.5,

                # parei aqui 


                "Calunia": 4,
                "Difamação": 3, "Injúria": 3,


                "Condicionamento de atendimento médico-hospitalar emergencial": 1, "Maus tratos": 1,
                "Maus tratos com lesão grave": 4,
                "Maus tratos com morte": 12, "Rixa": 0.2, "Rixa com morte ou lesão grave": 2,
                "Injúria Racial": 8,
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
                "Emprego irregular de verbas públicas": 3, "Concussão": 20, "Corrupção passiva": 20,
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
                "Patrocínio infiel": 8, "Exploração de prestígio": 12}






#ok
maria_da_penha = {"Descumprimento de decisão judicial que defere MPU": 2}

#ok
trafico = {
           "Art. 33": 15,
           "Art. 33, §2": 3,
           "Art. 33, §3": 1,
           "Art. 34": 10,
           "Art. 35": 10,
           "Art. 36": 20,
           "Art. 37": 6,
           "Art. 38": 2,
           "Art. 39": 3,
           }

#ok
estatuto_desarmamento = {""
                         "Posse irregular de arma de fogo de uso permitido - Art. 12": 3,
                         "Omissão de cautela - Art. 13": 2,
                         "Porte ilegal de arma de fogo de uso permitido - Art 14": 4,
                         "Disparo de arma de fogo - Art. 15": 4,
                         "Posse ou porte ilegal de arma de fogo de uso restrito - Art. 16": 6,
                         "Comércio ilegal de arma de fogo - Art. 17": 12,
                         "Tráfico internacional de arma de fogo - Art. 18": 16,
                         "Comércio ilegal de arma de fogo majorado - Art. 17 c/c Art 19": 18,
                         "Tráfico internacional de arma de fogo majorado - Art. 18 c/c Art 19": 24,
                         "Porte ilegal de arma de fogo de uso permitido majorado pela qualidade do agente - Art 14 c/c Art. 20": 6,
                         "Disparo de arma de fogo majorado pela qualidade do agente - Art. 15 c/c Art. 20": 6,
                         "Posse ou porte ilegal de arma de fogo de uso restrito majorado pela qualidade do agente - Art. 16 c/c Art. 20": 9,
                         "Comércio ilegal de arma de fogo majorado pela qualidade do agente - Art. 17 c/c Art. 20": 18,
                         "Tráfico internacional de arma de fogo majorado pela qualidade do agente - Art. 18 c/c Art. 20": 24,
                         }
#ok
lcp = {"Vias de fato - Art. 21": 0.25,
       "Perturbação do trabalho ou do sossego alheios - Art 42": 0.25,
       "Exercício ilegal de profissão ou atividade - Art. 47": 0.25,
       "Jogo de azar - Art. 50": 1,
       "Jogo de azar majorado - Art. 50, §1º": 1.4,
       "Jogo do bixo - Art. 58": 1, }


#ok
ctb = {"Art. 302": 4, "Art. 302, §1": 6, "Art. 302, §3": 8,
             "Art 303": 2, "Art. 303, §1º": 3, "Art. 303, §2º": 5, "Art. 304": 1,
             "Art. 305": 1, "Art. 306": 3, "Art. 307": 1, "Art. 308": 3, "Art. 308, §1º": 6,
             "Art. 308, §2": 10, "Art. 309": 1, "Art. 310": 1, "Art. 311": 1, "Art. 312": 1}

#ok
crimesambientais = {
    'Art. 29': 1,
    'Art. 29, §1º': 1,
    'Art. 29, §4°': 1.5,
    'Art. 29, §5º': 3,
    'Art. 30': 3,
    'Art. 31': 1,
    'Art. 32': 1,
    'Art. 32, §1º': 1,
    'Art. 32, §1-A': 5,
    'Art. 32, §2º': 4,
    'Art. 33': 3,
    'Art. 33, § único': 3,
    'Art. 34': 3,
    'Art. 34, § único': 3,
    'Art. 35': 5,
    'Art. 38': 3,
    'Art. 38 c/c Art. 53': 4,
    'Art. 38, § único': 1.5,
    'Art. 38, § único c/c art. 53': 1.8,
    'Art. 38-A': 3,
    'Art. 38-A c/c art. 53': 4,
    'Art. 38-A, § único': 1.5,
    'Art. 38-A, § único c/c art. 53': 1.8,
    'Art. 39': 3,
    'Art. 39 c/c art. 53': 4,
    'Art. 40': 5,
    'Art. 40 c/c art. 53': 6.8,
    'Art. 40, § 3º': 2.5,
    'Art. 40, § 3º c/c art. 53': 3.2,
    'Art. 41': 4,
    'Art. 41 c/c art. 53': 5.4,
    'Art. 41, § único': 1,
    'Art. 41, § único c/c art. 53': 1.4,
    'Art. 42': 3,
    'Art. 42 c/c art. 53': 4,
    'Art. 44': 1,
    'Art. 44 c/c art. 53': 1.4,
    'Art. 45': 2,
    'Art. 45 c/c art. 53': 1.8,
    'Art. 46': 1,
    'Art. 46 c/c art. 53': 1.4,
    'Art. 46, § único': 1,
    'Art. 48': 1,
    'Art. 48 c/c art. 53': 1.4,
    'Art. 49': 1,
    'Art. 49 c/c art. 53': 1.4,
    'Art. 50': 1,
    'Art. 50 c/c art. 53': 1.4,
    'Art. 50-A': 4,
    'Art. 50-A c/c 53': 5.4,
    'Art. 51': 1,
    'Art. 51 c/c art. 53': 1.4,
    'Art. 52': 1,
    'Art. 52 c/c art. 53': 1.4,
    'Art. 54': 4,
    'Art. 54 c/c art. 58, I': 5.4,
    'Art. 54 c/c art. 58, II': 6,
    'Art. 54 c/c art. 58, III': 8,
    'Art. 54, § 1º': 1,
    'Art. 54, § 2º': 5,
    'Art. 54, § 2º c/c art. 58, I': 6.8,
    'Art. 54, § 2º c/c art. 58, II': 7.5,
    'Art. 54, § 2º c/c art. 58,III': 10,
    'Art. 54, § 3º': 5,
    'Art. 54, § 3º c/c art. 58,I': 6.8,
    'Art. 54, § 3º c/c art. 58, II': 7.5,
    'Art. 54, §3º c/c art. 58, III': 10,
    'Art. 55': 1,
    'Art. 55 c/c art. 58, I': 1.4,
    'Art. 55 c/c art. 58, II': 1.6,
    'Art. 55 c/c art. 58, III': 2,
    'Art. 55, § único': 1,
    'Art. 55, § único c/c art. 58, I': 1.4,
    'Art. 55, § único c/c art. 58, II': 1.6,
    'Art. 55, § único c/c art. 58, III': 2,
    'Art. 56': 4,
    'Art. 56, c/c art. 58, I': 5.4,
    'Art. 56 c/c art. 58, II': 6,
    'Art. 56 c/c art. 58, III': 8,
    'Art. 56, § 1º': 4,
    'Art. 56, §1º c/c art. 58, I': 5.4,
    'Art. 56, §1º c/c art. 58, II': 6,
    'Art. 56, §1º c/c art. 58, III': 8,
    'Art. 56, § 2º': 5.4,
    'Art. 56, § 3º': 1,
    'Art. 60': 6,
    'Art. 60 c/c art. 58, I': 8,
    'Art. 60 c/c art. 58, II': 9,
    'Art. 60 c/c art. 58, III': 12,
    'Art. 61': 4,
    'Art. 61 c/c art. 58, I': 5.4,
    'Art. 61 c/c art. 58, II': 6,
    'Art. 61 c/c art. 58, III': 8,
    'Art. 62': 3,
    'Art. 62, § único': 1,
    'Art. 63': 3,
    'Art. 64': 1,
    'Art. 65': 1,
    'Art. 65, § 1°': 1,
    'Art. 66': 3,
    'Art. 67': 3,
    'Art. 67, § único': 1,
    'Art. 68': 3,
    'Art. 68, § único': 1,
    'Art. 69': 3,
    'Art. 69-A': 6,
    'Art. 69-A, § 1°': 3,
    'Art. 69-A, § 2º': 10
}


#ok
crimes_juri = {"Homicídio simples - Art. 121": 20,
        "Homicídio privilegiado - Art. 121 §1º": 13.3,
        "Homicídio qualificado - Art. 121 §2º": 30}

#ok
crimes_tributarios = {"Art 1º": 5, "Art. 2º": 2, "Art. 3º": 4}



ctb = {key: calcula_prazo_prescriocional(valor) for key, valor in ctb_penas.items()}

ambiental = {key: calcula_prazo_prescriocional(valor) for key, valor in crimesambientais.items()}

tributario = {key: calcula_prazo_prescriocional(valor) for key, valor in crimes_tributarios.items()}

juri = {key: calcula_prazo_prescriocional(valor) for key, valor in crimes_juri.items()}
