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
