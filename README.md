# Bot para Cotação de Moedas e Atualização no SAP

Este script Python automatiza o processo de consulta das cotações de moedas (Dólar e Euro) e atualiza esses valores no sistema SAP. Utiliza a biblioteca Selenium para navegar na internet, coletar informações de cotação de moedas do Banco Central e, em seguida, atualiza essas cotações no SAP utilizando scripts VBS gerados pela ferramenta de gravação do próprio SAP.

## Funcionalidades

- **Criação de Diretório**: Verifica e cria um diretório para armazenar configurações e logs (`bot_cotar_dolar`).
- **Cifragem e Decifragem**: Possui funções para cifrar e decifrar textos, aplicando uma chave numérica simples.
- **Carregamento de Configurações**: Carrega dados de login e configurações do SAP de um arquivo JSON. Se o arquivo não existir, cria um com valores padrão.
- **Consulta de Cotação de Moedas**: Abre o navegador (Google Chrome) e acessa o site do Banco Central para consultar as cotações do Dólar e do Euro referentes ao dia anterior. Os valores são extraídos e armazenados.
- **Atualização no SAP**: Inicia o SAP GUI, realiza login e executa uma série de passos automatizados para atualizar as cotações de moedas no sistema.
- **Registro de Logs**: Mantém um registro de logs de operações, incluindo erros, para facilitar o diagnóstico de problemas.

## Pré-requisitos

- Python 3.x instalado.
- Bibliotecas Python: `os`, `subprocess`, `sys`, `psutil`, `selenium`, `datetime`, `json`, `win32com.client`.
- Navegador Google Chrome instalado.
- Driver do Chrome (ChromeDriver) compatível com a versão do navegador instalado e no PATH do sistema.
- SAP GUI instalado e configurado no sistema.

## Configuração Inicial

1. **Configuração do JSON**: Verifique o arquivo `bot_cotar_dolar/config.json` para garantir que os dados de login e a descrição da entrada SAP estejam corretos.
2. **ChromeDriver**: Certifique-se de que o ChromeDriver esteja instalado e configurado corretamente.

## Uso

Para executar o script, simplesmente rode o arquivo Python através do terminal ou IDE de sua preferência:

```bash
python nome_do_script.py
