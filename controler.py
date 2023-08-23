import dicionario_legislacao
from datetime import date, timedelta
import datetime


class Acao:

    def __init__(self, data_fato, legislacao, crime):
        self.data_fato = data_fato
        self.legislacao = legislacao
        self.crime = crime
        self.prazo_prescricao = self.get_prescricao()
        self.suspensao_anterior_denuncia = 0
        self.suspensao_posterior_denuncia = 0

        self.data_prescricao_anterior_denuncia = data_fato + timedelta(days=(self.prazo_prescricao * 365)) + timedelta(
            days=self.suspensao_anterior_denuncia)

        # seta temporariamente a data de recebimento da denuncia
        self.data_rec_denuncia = None

        if self.data_rec_denuncia:
            self.data_prescricao_posterior_denuncia = self.data_rec_denuncia + timedelta(
                days=(self.prazo_prescricao * 365)) + timedelta(days=self.suspensao_posterior_denuncia)
        else:
            self.data_prescricao_posterior_denuncia = None

        self.data_pronuncia = None

        self.data_dec_conf_pronuncia = None
        self.data_prescricao_posterior_dec_conf_pronuncia = None

        self.prescreveu = False
        self.reducao_metade_idade = False
        self.idade_autor_data_fato = 0
        self.idade_autor_atual = 0

    def get_prescricao(self):
        if 'Lei 8.137/90' in self.legislacao:
            return dicionario_legislacao.tributario[self.crime]

        # elif self.legislacao == 'Código Penal':
        #
        #     return dicionario_legislacao.codigo_penal[self.crime]

        # elif self.legislacao == 'Lei Maria da Penha':
        #
        #     return dicionario_legislacao.maria_da_penha[self.crime]
        #
        #
        # elif self.legislacao == 'Lei 11.343/06 - Lei de Drogas':
        #
        #     return dicionario_legislacao.lei_drogas[self.crime]

        # elif self.legislacao == 'Lei 10.826/03 - Estatuto do Desarmamento':
        #
        #     return dicionario_legislacao.estatuto_desarmamento[self.crime]
        #
        #
        # elif self.legislacao == "Decreto_Lei nº 3.688 - Lei das Contravenções Penais":
        #
        #     return dicionario_legislacao.lei_contravencoes[self.crime]

        elif self.legislacao == "Lei 9.503/97 - Código de Trânsito Brasileiro":

            return dicionario_legislacao.ctb[self.crime]


        elif self.legislacao == "Lei 9.605/98 - Lei de Crimes Ambientais":

            return dicionario_legislacao.ambiental[self.crime]


        elif self.legislacao == "Código Penal - Júri":

            return dicionario_legislacao.juri[self.crime]

        # Caso contrário, retorna None ou uma mensagem padrão

        return None

    def get_suspensao_anterior_denuncia(self, days):
        self.suspensao_anterior_denuncia = days
        self.data_prescricao_anterior_denuncia = self.data_fato + timedelta(
            days=(self.prazo_prescricao * 365)) + timedelta(days=self.suspensao_anterior_denuncia)

    def get_suspensao_posterior_denuncia(self, days):
        self.suspensao_posterior_denuncia = days
        self.data_prescricao_posterior_denuncia = self.data_rec_denuncia + timedelta(
            days=(self.prazo_prescricao * 365)) + timedelta(days=self.suspensao_posterior_denuncia)

    def get_recebimento_denuncia(self, data: date):
        self.data_rec_denuncia = data
        self.data_prescricao_posterior_denuncia = self.data_rec_denuncia + timedelta(
            days=(self.prazo_prescricao * 365)) + timedelta(days=self.suspensao_posterior_denuncia)

    def get_data_pronuncia(self, data: date):
        self.data_pronuncia = data

        self.data_prescricao_posterior_pronuncia = self.data_pronuncia + timedelta(
            days=(self.prazo_prescricao * 365)) + timedelta(days=self.suspensao_posterior_denuncia)


    def get_data_dec_conf_pronuncia(self, data: date):
        self.data_dec_conf_pronuncia = data

        self.data_prescricao_posterior_dec_conf_pronuncia = self.data_dec_conf_pronuncia + timedelta(
            days=(self.prazo_prescricao * 365))

    def check_prescricao_anterior_denuncia(self):
        self.data_prescricao_anterior_denuncia = self.data_fato + timedelta(
            days=(self.prazo_prescricao * 365)) + timedelta(
            days=self.suspensao_anterior_denuncia)

        if not self.data_rec_denuncia:
            if self.data_prescricao_anterior_denuncia < datetime.date.today():
                print('aqui aqui')
                self.prescreveu = True
                return True
            else:
                self.prescreveu = False
                return False

        elif self.data_rec_denuncia:
            if self.data_prescricao_anterior_denuncia < self.data_rec_denuncia:
                self.prescreveu = True
                return True
            else:
                self.prescreveu = False
                return False

    def check_prescricao_posterior_denuncia(self):
        if not self.data_pronuncia:
            self.data_prescricao_posterior_denuncia = self.data_rec_denuncia + timedelta(
                days=(self.prazo_prescricao * 365)) + timedelta(days=self.suspensao_posterior_denuncia)

            if self.data_prescricao_posterior_denuncia < datetime.date.today():
                self.prescreveu = True
                return True
            else:
                return False

        if self.data_pronuncia:
            self.data_prescricao_posterior_denuncia = self.data_rec_denuncia + timedelta(
                days=(self.prazo_prescricao * 365)) + timedelta(days=self.suspensao_posterior_denuncia)

            if self.data_prescricao_posterior_denuncia < self.data_pronuncia:
                self.prescreveu = True
                return True
            else:
                return False

    def check_prescricao_posterior_pronuncia(self):
        if not self.data_dec_conf_pronuncia:
            if self.data_prescricao_posterior_pronuncia:
                self.data_prescricao_posterior_pronuncia = self.data_prescricao_posterior_denuncia + timedelta(
                    days=(self.prazo_prescricao * 365))

                if self.data_prescricao_posterior_pronuncia < datetime.date.today():
                    self.prescreveu = True
                    return True
                else:
                    return False

        if self.data_dec_conf_pronuncia:
            if self.data_prescricao_posterior_pronuncia:
                self.data_prescricao_posterior_pronuncia = self.data_prescricao_posterior_denuncia + timedelta(
                    days=(self.prazo_prescricao * 365))

                if self.data_prescricao_posterior_pronuncia < self.data_dec_conf_pronuncia:
                    self.prescreveu = True
                    return True
                else:
                    return False


    def check_prescricao_posterior_dec_conf_pronuncia(self):
        if self.data_prescricao_posterior_dec_conf_pronuncia:

            if self.data_prescricao_posterior_dec_conf_pronuncia < datetime.date.today():
                self.prescreveu = True
                return True
            else:
                return False

    def check_reducao_idade_autor(self, data_nascimento):

        idade_na_data_fato = self.data_fato.year - data_nascimento.year - (
                (self.data_fato.month, self.data_fato.day) < (
            data_nascimento.month, data_nascimento.day))

        data_atual = datetime.date.today()

        # calcula a idade na data atual
        idade_na_data_atual = data_atual.year - data_nascimento.year - (
                (data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day))

        # verifica se a pessoa tinha 21 anos na data do fato

        self.idade_autor_data_fato = idade_na_data_fato
        self.idade_autor_atual = idade_na_data_atual

        if idade_na_data_fato < 21 or idade_na_data_atual >= 70:
            self.prazo_prescricao = self.get_prescricao() * 1 / 2

            self.data_prescricao_anterior_denuncia = self.data_fato + timedelta(
                days=(self.prazo_prescricao * 365)) + timedelta(
                days=self.suspensao_anterior_denuncia)

            self.data_prescricao_posterior_denuncia = self.data_rec_denuncia + timedelta(
                days=(self.prazo_prescricao * 365)) + timedelta(days=self.suspensao_posterior_denuncia)

            self.reducao_metade_idade = True
            self.check_prescricao_anterior_denuncia()
            self.check_prescricao_posterior_denuncia()

    def return_data(self):
        data = {'Data do fato': self.data_fato,
                'Incidência Penal': self.crime,
                'Prazo prescricional legal': self.prazo_prescricao,
                'Suspensão anterior a denúncia (dias)': self.suspensao_anterior_denuncia,
                'Suspensão posterior a denúncia (dias)': self.suspensao_posterior_denuncia,
                'Data de Prescrição a partir da data do fato': self.data_prescricao_anterior_denuncia,
                'Data de recebimento da Denúncia': self.data_rec_denuncia,
                'Data de Prescrição a partir do recebimento da denúncia': self.data_prescricao_posterior_denuncia,
                'Data da Pronúncia': self.data_pronuncia,
                'Data da decisão confirmatória da pronúncia': self.data_dec_conf_pronuncia,
                'Data de prescrição após a decisão confirmatória da pronúncia': self.data_prescricao_posterior_dec_conf_pronuncia,
                'Houve redução do prazo prescricional pela idade do agente': self.reducao_metade_idade,
                'Idade do autor na data do fato': self.idade_autor_data_fato,
                'Idade do autor na data atual': self.idade_autor_atual,
                'Crime prescreveu?': self.prescreveu
                }

        for key, valor in data.items():
            # Check if it's a date
            if isinstance(valor, date):
                data[key] = valor.strftime('%d/%m/%Y')
            # Check if it's a boolean True or False
            elif valor is True:
                data[key] = "Sim"
            elif valor is False:
                data[key] = "Não"
            # Else, just assign the original value
            else:
                data[key] = valor

        return data
