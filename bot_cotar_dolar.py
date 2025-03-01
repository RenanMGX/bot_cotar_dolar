import os
import subprocess
import sys
import psutil
from selenium import webdriver
#from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
from time import sleep
import win32com.client
from Entities.dependencies.credenciais import Credential
from Entities.dependencies.config import Config
from Entities.dependencies.logs import Logs, traceback
from Entities.dependencies.sap import SAPManipulation

if not os.path.exists("bot_cotar_dolar"):
    os.makedirs("bot_cotar_dolar")

crd:dict = Credential(Config()['credential']['crd']).load()

#tratamento de datas
hoje_bruto = datetime.datetime.now()
ontem_bruto = hoje_bruto - datetime.timedelta(days=1)
hoje = hoje_bruto.strftime("%d%m%Y")
ontem = ontem_bruto.strftime("%d%m%Y")
ontem_verificar = ontem_bruto.strftime("%d/%m/%Y")

# Nome do processo que você deseja fechar (substitua pelo nome do processo correto)
def fechar_programa(process_name, insta=False):
    if insta == False:
        sleep(30)
    # Procurar pelo processo pelo nome
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if process.info['name'] == process_name:
            pid = process.info['pid']
            # Encerrar o processo
            psutil.Process(pid).terminate()
            print(f"Processo {process_name} encerrado com sucesso.")
            break
    else:
        print(f"Processo {process_name} não encontrado.")


class Bot_sap(SAPManipulation):
    def __init__(self):
        '''
        metodo para construir o objeto
        quando o metodo é criado ele faz o login no sap
        '''
        
        super().__init__(user=crd['user'], password=crd['password'], ambiente=crd['ambiente'], new_conection=True)
        
        self.finalizou = False

    
    @SAPManipulation.start_SAP
    def sap_auto(self, cotacao):
        '''
        metodo para iniciar os procedimentos de uso no SAP previamente gravados usando a ferramenta de graçavação do proprio sap
        e gerando o arquivo .vbs,
        copie só as linhas com o session.finById() e adicione o self.,
        em algumas linhas no final é preciso adicionar o "()".
        '''
        data = ontem_bruto.strftime("%d.%m.%Y")
        try:
            self.session.findById("wnd[0]").maximize()
            self.session.findById("wnd[0]/tbar[0]/okcd").text = "/nob08"
            self.session.findById("wnd[0]").sendVKey(0)
            self.session.findById("wnd[0]/tbar[1]/btn[5]").press()
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-KURST[0,0]").text = "M"
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-KURST[0,1]").text = "M"
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-KURST[0,2]").text = "M"
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-KURST[0,3]").text = "M"
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-KURST[0,4]").text = "M"
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-KURST[0,5]").text = "M"
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-KURST[0,6]").text = "M"
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-KURST[0,7]").text = "M"
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-GDATU[1,0]").text = data
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-GDATU[1,1]").text = data
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-GDATU[1,2]").text = data
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-GDATU[1,3]").text = data
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-GDATU[1,4]").text = data
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-GDATU[1,5]").text = data
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-GDATU[1,6]").text = data
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-GDATU[1,7]").text = data
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/txtRFCU9-KURSM[2,0]").text = cotacao["dolar"]
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/txtRFCU9-KURSM[2,1]").text = cotacao["euro"]
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/txtRFCU9-KURSM[2,2]").text = 1
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/txtRFCU9-KURSM[2,3]").text = 1
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-FCURR[5,0]").text = "BRL"
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-FCURR[5,1]").text = "BRL"
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-FCURR[5,2]").text = "BRL"
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-FCURR[5,3]").text = "BRL"
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-FCURR[5,4]").text = "USD"
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-FCURR[5,5]").text = "EUR"
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-FCURR[5,6]").text = "MPN"
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-FCURR[5,7]").text = "IGPM"
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/txtRFCU9-KURSP[7,4]").text = cotacao["dolar"]
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/txtRFCU9-KURSP[7,5]").text = cotacao["euro"]
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/txtRFCU9-KURSP[7,6]").text = 1
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/txtRFCU9-KURSP[7,7]").text = 1
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-TCURR[10,0]").text = "USD"
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-TCURR[10,1]").text = "EUR"
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-TCURR[10,2]").text = "MPN"
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-TCURR[10,3]").text = "IGPM"
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-TCURR[10,4]").text = "BRL"
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-TCURR[10,5]").text = "BRL"
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-TCURR[10,6]").text = "BRL"
            self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-TCURR[10,7]").text = "BRL"
            self.session.findById("wnd[0]").sendVKey(0)
            self.session.findById("wnd[0]/tbar[0]/btn[0]").press()
            self.session.findById("wnd[0]/tbar[0]/btn[11]").press()

            self.finalizou = True
            
        except Exception as error:
            registro(str(error))
        finally:
            self.fechar_sap()
            

class bot_navegador():
    def __init__(self):
        '''
        metodo construtor responsavel por abrir o navegador do google chrome na pagina solicitada
        '''
        self.navegador = webdriver.Chrome()
        self.navegador.get("https://ptax.bcb.gov.br/ptax_internet/consultaBoletim.do?method=exibeFormularioConsultaBoletim")
        self.cotacao = {}

    def clicar(self, target=None):
        '''
        metodo utilizado para clicar em lugares da pagina aceia apenas XPATH que será recebido pelo 'target'
        '''
        try:
            button = self.navegador.find_element(By.XPATH, target)
            button.click()
        except Exception as error:
            return

    def escrever(self, target=None, texto=None):
        '''
        metodo utilizado para escrever em algum campo do site os dados recebidos pelo 'texto' o metodo aceita apenas XPATH que é recebido pelo 'target'.
        '''
        try:
            button = self.navegador.find_element(By.XPATH, target)
            button.clear()
            button.send_keys(str(texto))
        except Exception as error:
            return

    def salvar(self, target=None, key=None):
        '''
        metodo utilizado para copiar dados de um campo no site
        este metodo especificamente coleta os dados de uma tabela no site do banco do brasil e separa por linhas o dado
        depois ele verifica linha por linha se tem a data solicitada que por padrão será a data do dia anterior
        caso ache a linha com a data especificada ele da um 'split' na linha dividindo pelo espaço vazio ' ' e seleciona o valor que estiver no endereço 2 que estará o valor da moeda solicitada
        ele salva em uma instancia global 'self.cotacao' e define a chave pelo valor recebido por 'key' esté metodo só aceita XPATH que é recebido pelo 'target'
        '''
        try:
            button = self.navegador.find_element(By.XPATH, target)
            valor = button.text
            valor = valor.split("\n")
            for data in valor:
                if ontem_verificar in data:
                    valor_moeda = data.split(" ")
                    # até o desenvolvimento desse script o endereço [2] da variavel 'valor_moeda' será o valor monetario
                    self.cotacao[key] = valor_moeda[2]

        except Exception as error:
            return

    def esperar(self, target=None):
        '''
        metodo responsavel por esperar o elemento XPATH aparecer na pagina para depois dar continuidade ao script
        isso ajuda caso a pagina demore a carregar e o script não avançe o roteiro sem necessidade
        o metodo aceita apenas XPATH recebido pelo 'target'.
        '''
        contador = 0
        while True:
            if contador >= 5*60:
                return
            else:
                contador += 1

            try:
                self.navegador.find_element(By.XPATH, target)
                break
            except Exception as error:
                sleep(1)


    def testes(self, target=None):
        '''
        metodo reservado apenas para testes no desenvolvimento do bot.
        '''
        try:
            buttom = self.navegador.find_element(By.XPATH, target)
            #buttom.clear()
            #buttom.send_keys(str(target))
            print(buttom.text)

        except Exception as error:
            registro("Não Achou")

    def checar(self, target=None):
        try:
            button = self.navegador.find_element(By.XPATH, target)
            if button.text == "• Não existe informação para a pesquisa efetuada! •":
                registro("finalizador de emergencia do Navegador acionado: não existe cotação para esta data")
                sys.exit()
        except Exception as error:
            return

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
            elif param == "checar":
                self.checar(target=action[1])


def registro(error="OK"):
    '''
    está função salva um registro na mesma pasta do da execução do script,
    funciona para ser um tipo de log para saber se o script deu error ou foi executado corretamente,
    ele faz o registro em um arquivo .csv separados por ';' com as seguintes categorias de dados:
    -data: dia/mes/ano da ocorrencia
    -hora: hora:minuto:segundo da ocorrencia
    -error: registro da ocorrencia tanto positiva quanto negativa, no caso de negativa geramente é o error retornado pelo Exeption.
    '''
    print(error)
    error = str(error)
    error = error.replace("\n"," ")
    data_atual = datetime.datetime.now().strftime("%d/%m/%Y")
    hora = datetime.datetime.now().strftime("%H:%M:%S")
    with open("bot_cotar_dolar\\logs_error.csv", "a") as arqui:
        arqui.write(f"{data_atual};{hora};{error}\n")

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
    ["checar", "/html/body/div[1]"],
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
        finalizador_emergencia = 0
        while True:
            try:
                bot:bot_navegador = bot_navegador()
                bot.executando(roteiro)
                if not bot.cotacao:
                    continue
                else:
                    break
            except Exception as error:
                bot.navegador.close() #type: ignore
                sleep(1)
                finalizador_emergencia += 1
                if finalizador_emergencia >= 15*60:
                    registro(str(error))
                    registro("finalizador de emergencia do Navegador acionado!")
                    sys.exit()
        bot.navegador.quit()
        #input()
        registro(str(bot.cotacao))
        finalizador_emergencia = 0
        while True:
            #fechar_programa("saplogon.exe", insta=True)
            finalizador_emergencia += 1
            if finalizador_emergencia >= 15:
                registro("finalizador de emergencia do SAP acionado!")
                sys.exit()
            #print(finalizador_emergencia)
            try:
                sap = Bot_sap()
                sap.sap_auto(bot.cotacao)
                if sap.finalizou == True:
                    registro("SAP - OK")
                    sap.fechar_sap()
                    #fechar_programa("saplogon.exe")
                    break
            except Exception as error:
                registro(str(error))
                #fechar_programa("saplogon.exe")
                sleep(5*60)
        
        Logs().register(status='Concluido', description=f"Cotação Registrada: {bot.cotacao}")
        sys.exit()
    except Exception as err:
        Logs().register(status='Error', description=str(err), exception=traceback.format_exc())
