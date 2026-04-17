# 🖨️ Monitor Universal de Impressoras (SNMP)

Ferramenta desenvolvida para automação de inventário e monitoramento de suprimentos em redes corporativas.

## 🚀 Funcionalidades
- **Monitoramento em Lote:** Uso de Multithreading para alta performance.
- **Varredura de Tabela (Walk):** Identifica todos os componentes de suprimento automaticamente.
- **Relatórios:** Exportação para CSV (Histórico) e TXT (Status em Tempo Real).

## 🛠️ Tecnologias
- **Python 3.x**
- **PySNMP** (Protocolo de Gerenciamento de Rede)
- **Concurrent Futures** (Paralelismo)

## 📋 Como usar
1. Instale as dependências: `pip install -r requirements.txt`
2. Configure os IPs no arquivo `ips_config.txt`
3. Execute o script ou o binário gerado.
📦 Gerando o Executável (.exe)
Para distribuir esta ferramenta para outros técnicos que não possuem Python instalado, siga os passos abaixo:

Passo 1: Instale o PyInstaller
bash
pip install pyinstaller

Passo 2: Gere o executável
bash

py -m PyInstaller --onefile --clean --name monitor_impressoras monitor_universal.py

Passo 3: Localize o executável
O arquivo monitor_impressoras.exe estará disponível na pasta dist/ após a conclusão.

Passo 4: Distribuição
Você pode copiar apenas o arquivo .exe para qualquer computador Windows. Ele não precisa do Python instalado. Basta colocar 
o executável na mesma pasta que o arquivo ips_config.txt.
