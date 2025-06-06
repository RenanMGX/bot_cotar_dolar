import os
from patrimar_dependencies.sap import SAPManipulation
from datetime import datetime
from botcity.maestro import * # type: ignore

class SAP(SAPManipulation):
    def __init__(self, *, maestro:BotMaestroSDK, user:str, password:str, ambiente:str) -> None:
        self.maestro:BotMaestroSDK = maestro
        super().__init__(user=user, password=password, ambiente=ambiente)
        
        
    @SAPManipulation.start_SAP
    def registrar(self, *, cotacao:dict, date:datetime) -> bool:
        '''
        metodo para iniciar os procedimentos de uso no SAP previamente gravados usando a ferramenta de graçavação do proprio sap
        e gerando o arquivo .vbs,
        copie só as linhas com o session.finById() e adicione o self.,
        em algumas linhas no final é preciso adicionar o "()".
        '''

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
        self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-GDATU[1,0]").text = date.strftime("%d.%m.%Y")
        self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-GDATU[1,1]").text = date.strftime("%d.%m.%Y")
        self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-GDATU[1,2]").text = date.strftime("%d.%m.%Y")
        self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-GDATU[1,3]").text = date.strftime("%d.%m.%Y")
        self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-GDATU[1,4]").text = date.strftime("%d.%m.%Y")
        self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-GDATU[1,5]").text = date.strftime("%d.%m.%Y")
        self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-GDATU[1,6]").text = date.strftime("%d.%m.%Y")
        self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/ctxtV_TCURR-GDATU[1,7]").text = date.strftime("%d.%m.%Y")
        self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/txtRFCU9-KURSM[2,0]").text = cotacao['DOLAR DOS EUA']
        self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/txtRFCU9-KURSM[2,1]").text = cotacao["EURO"]
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
        self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/txtRFCU9-KURSP[7,4]").text = cotacao['DOLAR DOS EUA']
        self.session.findById("wnd[0]/usr/tblSAPL0SAPTCTRL_V_TCURR/txtRFCU9-KURSP[7,5]").text = cotacao["EURO"]
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
            
        result = self.session.findById("wnd[0]/sbar").text
        
        if result == 'Dados gravados':
            return True
        else:
            self.maestro.alert(
                task_id=self.maestro.get_execution().task_id,
                title="Alerta do SAP caso dados não sejam salvos",
                message=f"Não foi possível registrar as cotações no SAP para a data {date.strftime('%d/%m/%Y')}. - {cotacao} motivo: {result}",
                alert_type=AlertType.ERROR
            )                
            
            return False
        
if __name__ == "__main__":
    pass
        