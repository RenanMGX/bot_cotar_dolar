"""
WARNING:

Please make sure you install the bot dependencies with `pip install --upgrade -r requirements.txt`
in order to get all the dependencies on your Python environment.

Also, if you are using PyCharm or another IDE, make sure that you use the SAME Python interpreter
as your IDE.

If you get an error like:
```
ModuleNotFoundError: No module named 'botcity'
```

This means that you are likely using a different Python interpreter than the one used to install the dependencies.
To fix this, you can either:
- Use the same interpreter as your IDE and install your bot with `pip install --upgrade -r requirements.txt`
- Use the same interpreter as the one used to install the bot (`pip install --upgrade -r requirements.txt`)

Please refer to the documentation for more information at
https://documentation.botcity.dev/tutorials/custom-automations/python-custom/
"""

# Import for integration with BotCity Maestro SDK
from botcity.maestro import * #type: ignore
import traceback
from patrimar_dependencies.gemini_ia import ErrorIA
from patrimar_dependencies.screenshot import screenshot
from Entities.web import Web, datetime, relativedelta
from Entities.sap import SAP
from Entities.utils import *
from Entities.exceptions import *
from time import sleep

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False #type: ignore


class Execute:
    @staticmethod
    def start():
        date_param = execution.parameters.get("date")
        if date_param:
            date = datetime.strptime(str(date_param), "%d/%m/%Y")
        else:
            date = datetime.now() - relativedelta(days=1)  # Data de exemplo, pode ser alterada conforme necessário
        
        crd_param = execution.parameters.get("crd")
        if not isinstance(crd_param, str):
            raise ValueError("Parâmetro 'crd_param' deve ser uma string representando o label da credencial.")
        
        
        web = Web(maestro=maestro, headless=True)
        moedas = {}
        moedas |= web.get_moeda('DOLAR DOS EUA', date=date)
        moedas |= web.get_moeda('EURO', date=date)

        if not verificar_cotaçoes(
            cotacoes_verificar=["DOLAR DOS EUA", "EURO"],
            cotacoes_disponiveis=moedas,
        ):
            raise CotacoesNotFoundException(f"Cotação não encontrada para DOLAR DOS EUA ou EURO na data especificada. - {moedas}")
        
        try:
            sap = SAP(
                maestro=maestro,
                user=maestro.get_credential(label=crd_param, key="user"),
                password=maestro.get_credential(label=crd_param, key="password"),
                ambiente=maestro.get_credential(label=crd_param, key="ambiente")
            )
            
            if not sap.registrar(cotacao=moedas, date=date):
                raise SAPCotacoesNotSavedException(f"Não foi possível registrar as cotações no SAP para a data {date.strftime('%d/%m/%Y')}. - {moedas}")
            
            maestro.new_log_entry(
                activity_label="Cotacao_no_SAP",
                values={
                    "infor": f"Cotação do Dolar: {moedas.get('DOLAR DOS EUA', 'N/A')}, Cotação do Euro: {moedas.get('EURO', 'N/A')}, Data: {date.strftime('%d/%m/%Y')}"
                }
            )            
        finally:
            sap.fechar_sap() #type: ignore
            
        


if __name__ == '__main__':
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()
    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")
    
    for _ in range(3):
        try:
            Execute.start()
            
            maestro.finish_task(
                        task_id=execution.task_id,
                        status=AutomationTaskFinishStatus.SUCCESS,
                        message="Tarefa Cotação no SAP foi finalizada com sucesso",
                        total_items=1, # Número total de itens processados
                        processed_items=1, # Número de itens processados com sucesso
                        failed_items=0 # Número de itens processados com falha
            )
            break
            
        except CotacoesNotFoundException as error:
            maestro.finish_task(
                        task_id=execution.task_id,
                        status=AutomationTaskFinishStatus.SUCCESS,
                        message="Tarefa Cotação no SAP foi finalizada mas não encontrou as cotações",
                        total_items=1, # Número total de itens processados
                        processed_items=0, # Número de itens processados com sucesso
                        failed_items=1 # Número de itens processados com falha
            )
            
            
        except SAPCotacoesNotSavedException as error:
            maestro.finish_task(
                        task_id=execution.task_id,
                        status=AutomationTaskFinishStatus.FAILED,
                        message="Tarefa Cotação no SAP falhou ao salvar as cotações",
                        total_items=1, # Número total de itens processados
                        processed_items=0, # Número de itens processados com sucesso
                        failed_items=1 # Número de itens processados com falha
            )
            
            
        except Exception as error:
            ia_response = "Sem Resposta da IA"
            try:
                token = maestro.get_credential(label="GeminiIA-Token-Default", key="token")
                if isinstance(token, str):
                    ia_result = ErrorIA.error_message(
                        token=token,
                        message=traceback.format_exc()
                    )
                    ia_response = ia_result.replace("\n", " ")
            except Exception as e:
                maestro.error(task_id=int(execution.task_id), exception=e)
                
            maestro.error(task_id=int(execution.task_id), exception=error, screenshot=screenshot(), tags={"IA Analise": ia_response})
        
        sleep(5 * 60)
