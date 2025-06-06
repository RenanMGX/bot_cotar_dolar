from patrimar_dependencies.navegador_chrome import NavegadorChrome, By, Select
from datetime import datetime
from dateutil.relativedelta import relativedelta
from patrimar_dependencies.functions import P
from typing import Literal
from botcity.maestro import *  # type: ignore


class Web(NavegadorChrome):
    def __init__(self, *, maestro:BotMaestroSDK, headless:bool=True):
        self.maestro:BotMaestroSDK = maestro
        super().__init__(headless=headless)
        
    def get_moeda(self, moeda:Literal["DOLAR DOS EUA", "EURO"]|str, *, date:datetime):
        yesterday = date - relativedelta(days=1)
        self.get("https://ptax.bcb.gov.br/ptax_internet/consultaBoletim.do?method=exibeFormularioConsultaBoletim")
        
        initial_date = self.find_element(By.ID, 'DATAINI')
        initial_date.clear()
        initial_date.send_keys(yesterday.strftime("%d%m%Y"))
        
        last_date = self.find_element(By.ID, 'DATAFIM')
        last_date.clear()
        last_date.send_keys(date.strftime("%d%m%Y"))
        
        select_element = self.find_element(By.XPATH, '/html/body/div/form/table[2]/tbody/tr[4]/td[2]/select')
        select = Select(select_element)
        
        try:
            select.select_by_visible_text(moeda)
        except:
            return {}
        
        self.find_element(By.XPATH, '/html/body/div/form/div/input').click()
        
        try:
            error = self.find_element(By.XPATH, '/html/body/div[1]', timeout=1).text
            if '• Não existe informação para a pesquisa efetuada! •' == error:
                print(P(error))
                
                self.maestro.alert(
                    task_id=self.maestro.get_execution().task_id,
                    title="Cotação não encontrada!",
                    message=f"• Não existe informação para a pesquisa efetuada! • para a cotação da moeda '{moeda}' da data {date.strftime("%d/%m/%Y")}",
                    alert_type=AlertType.INFO
                )                
                
                return {}
        except:
            pass
        
        result = {}
        tbody = self.find_element(By.TAG_NAME, 'tbody')
        tr = tbody.find_elements(By.TAG_NAME, 'tr')
        for linhas in tr:
            if date.strftime("%d/%m/%Y") in linhas.text:
                result[moeda] = linhas.text.split()[2]
                
        return result
        
if __name__ == "__main__":
    pass
        