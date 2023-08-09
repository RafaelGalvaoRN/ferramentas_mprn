def calcula_prazo_prescriocional(tempo):
    if tempo < 1:
        return 3
    elif tempo <= 2:
        return 4
    elif tempo <=4:
        return 8
    elif tempo <= 8:
        return 12
    elif tempo <= 12:
        return 16
    elif tempo > 12:
        return 20



codigo_penal = {'Ameaça': 3, 'Infanticídio': 12, "Lesão Corporal - Art 129": 4,
                "Lesão Grave - Art 129, §1": 12, "Lesão Gravíssima - Art 129, §2": 12,
                "Lesão Corporal seguida de morte - Art 129, §3": 16,
                "Lesão Corporal culposa - Art 129, §6": 4,
                "Lesão Corporal privilegiada - Art 129, §4": 3,
                "Lesão Corporal grave privilegiada - Art 129, §4": 12,
                "Lesão Corporal gravíssima privilegiada - Art 129, §4": 12,
                "Lesão Corporal majorada - Art 129, §7": 4,
                "Lesão Corporal grave majorada - Art 129, §7": 12,
                "Lesão Corporal gravíssima majorada - Art 129, §7": 16,
                "Lesão Corporal seguida de morte majorada - Art 129, §7": 20,
                "Lesão Corporal culposa majorada - Art 129, §7": 4,
                "Lesão Corporal em contexto de violência doméstica - Art 129, §9": 8,
                "Lesão Corporal grave em contexto de violência doméstica - Art 129, §10": 12,
                "Lesão Corporal gravíssima em contexto de violência doméstica - Art 129, §10": 16,
                "Lesão Corporal seguida de morte em contexto de violência doméstica - Art 129, §10": 20,
                "Lesão Corporal em contexto de violência doméstica contra pessoa deficiente - Art 129, §11": 8,
                "Lesão Corporal contra a mulher, por razões da condição do sexo feminino - Art 129, §12": 8,
                "Homicídio simples": 20, "Homicídio qualificado": 20, "Feminicídio": 20, "Homicídio culposo": 8,
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

maria_da_penha = {"Descumprimento de decisão judicial que defere MPU": 4}

trafico = {"Art. 28": 2,
           "Art. 33": 20,
           "Art. 33, §2": 8,
           "Art. 33, §3": 3,
           "Art. 34": 16,
           "Art. 35": 16,
           "Art. 36": 20,
           "Art. 37": 12,
           "Art. 38": 4,
           "Art. 39": 8,
           }

estatuto_desarmamento = {""
                         "Posse irregular de arma de fogo de uso permitido - Art. 12": 8,
                         "Omissão de cautela - Art. 13": 4,
                         "Porte ilegal de arma de fogo de uso permitido - Art 14": 8,
                         "Disparo de arma de fogo - Art. 15": 8,
                         "Posse ou porte ilegal de arma de fogo de uso restrito - Art. 16": 12,
                         "Comércio ilegal de arma de fogo - Art. 17": 16,
                         "Tráfico internacional de arma de fogo - Art. 18": 20,
                         "Comércio ilegal de arma de fogo majorado - Art. 17 c/c Art 19": 20,
                         "Tráfico internacional de arma de fogo majorado - Art. 18 c/c Art 19": 20,
                         "Porte ilegal de arma de fogo de uso permitido majorado pela qualidade do agente - Art 14 c/c Art. 20": 12,
                         "Disparo de arma de fogo majorado pela qualidade do agente - Art. 15 c/c Art. 20": 12,
                         "Posse ou porte ilegal de arma de fogo de uso restrito majorado pela qualidade do agente - Art. 16 c/c Art. 20": 16,
                         "Comércio ilegal de arma de fogo majorado pela qualidade do agente - Art. 17 c/c Art. 20": 20,
                         "Tráfico internacional de arma de fogo majorado pela qualidade do agente - Art. 18 c/c Art. 20": 20,
                         }

lcp = {"Vias de fato - Art. 21": 3,
       "Perturbação do trabalho ou do sossego alheios - Art 42": 3,
       "Exercício ilegal de profissão ou atividade - Art. 47": 3,
       "Jogo de azar - Art. 50": 4,
       "Jogo de azar majorado - Art. 50, §1º": 4,
       "Jogo do bixo - Art. 58": 4, }


ctb_penas = {"Art. 302": 4, "Art. 302, §1": 6, "Art. 302, §3": 8,
       "Art 303": 2, "Art. 303, §1º": 3, "Art. 303, §2º": 5, "Art. 304": 1,
       "Art. 305": 1, "Art. 306": 3, "Art. 307": 1, "Art. 308": 3, "Art. 308, §1º": 6,
       "Art. 308, §2": 10, "Art. 309": 1, "Art. 310": 1, "Art. 311": 1, "Art. 312": 1}



ctb  = {key: calcula_prazo_prescriocional(valor) for key, valor in ctb_penas.items()}
