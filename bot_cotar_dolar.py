import subprocess
import sys
subprocess.check_output("pip install --upgrade selenium", shell=True)
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchWindowException
import datetime
from time import sleep

hoje_bruto = datetime.datetime.now()
ontem_bruto = hoje_bruto - datetime.timedelta(days=1)
hoje = hoje_bruto.strftime("%d%m%Y")
ontem = ontem_bruto.strftime("%d%m%Y")
ontem_verificar = ontem_bruto.strftime("%d/%m/%Y")


class bot_navegador():
    def __init__(self):
        self.navegador = webdriver.Chrome()
        self.navegador.get("https://ptax.bcb.gov.br/ptax_internet/consultaBoletim.do?method=exibeFormularioConsultaBoletim")
        self.cotacao = {}
    
    def clicar(self, target=None):
        try:
            button = self.navegador.find_element(By.XPATH, target)
            button.click()
        except Exception as error:
            print(error)
    
    def escrever(self, target=None, texto=None):
        try:
            button = self.navegador.find_element(By.XPATH, target)
            button.clear()
            button.send_keys(texto)
        except Exception as error:
            print(error)

    def salvar(self, target=None, key=None):
        try:
            button = self.navegador.find_element(By.XPATH, target)
            valor = button.text
            valor = valor.split("\n")
            for data in valor:
                if ontem_verificar in data:
                    valor_moeda = data.split(" ")
                    self.cotacao[key] = valor_moeda[2]

        except Exception as error:
            print(error)

    def esperar(self, target=None):
        while True:
            try:
                self.navegador.find_element(By.XPATH, target)
                break
            except Exception as error:
                print(error)
    
    
    def testes(self, target=None):
        try:
            buttom = self.navegador.find_element(By.XPATH, target)
            #buttom.clear()
            #buttom.send_keys(str(target))
            print(buttom.text)

        except Exception as error:
            print("Não Achou")
    
    def executando(self, roteiro):
        '''
        action[0] - será os parametros para definir a ação
        action[1] - será o endereço XPATH
        action[2] -  multiplas ações:
                se vier do 'escrever' - é o conteudo a ser escrito no site
                se vier do 'salvar' - irá salvar o conteudo em uma dict o valor que vier do roteiro será a key do dict
        '''

        for action in roteiro:
            param = action[0]
            if param == "click":
                self.clicar(target=action[1])
            elif param == "escrever":
                self.escrever(target=action[1], texto=action[2])
            elif param == "salvar":
                self.salvar(target=action[1], key=action[2])
            elif param == "carregar_pagina":
                self.navegador.get(action[1])
            elif param == "esperar":
                self.esperar(target=action[1])
        print("fim")


def registro(error="OK"):
    print(error)
    data_atual = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
    with open("logs_error.csv", "a") as arqui:
        arqui.write(f"{data_atual};{error}\n")

#parametros do roteiro
# 'click' - para clicar -- 2 valores
# 'escrever' - para digitar em algum campo -- 3 valores
# 'salvar' irá salvar em uma dict o valor monetario do dola ou euro -- 3 valores
# 'esperar' - vai esperar a pagina carregar para avançar -- 2 valores
# 'carregar_pagina' - vai carregar a pagina solicitada -- 2 valores
roteiro = [
    ["esperar",'//*[@id="DATAINI"]'], #espera pagina carregar
    ["escrever",'//*[@id="DATAINI"]', ontem], #data inicial
    ["escrever",'//*[@id="DATAFIM"]', hoje], #data final
    ["click","/html/body/div/form/table[2]/tbody/tr[4]/td[2]/select/option[58]"], #Dolar
    ["click","/html/body/div/form/div/input"], #pesquisar
    ["salvar","/html/body/div/table/tbody", "dolar"], #salvar na dict o valor do Dolar
    ["carregar_pagina","https://ptax.bcb.gov.br/ptax_internet/consultaBoletim.do?method=exibeFormularioConsultaBoletim"], #voltar para pagina inicial
    ["escrever",'//*[@id="DATAINI"]', ontem], #data inicial
    ["escrever",'//*[@id="DATAFIM"]', hoje], #data final
    ["click","/html/body/div/form/table[2]/tbody/tr[4]/td[2]/select/option[87]"], #Euro
    ["click","/html/body/div/form/div/input"], #pesquisar
    ["salvar","/html/body/div/table/tbody", "euro"], #salva na dict o valor do Euro
]
        
if __name__== "__main__":
    try:

        #### teste
        # bot = bot_navegador()
        # while True:
        #     entrada = input()
        #     bot.testes(entrada)

        #######

        bot = bot_navegador()
        bot.executando(roteiro)

        #input()
        registro(bot.cotacao)     
        sys .exit()  
    except Exception as error:
        registro(error)