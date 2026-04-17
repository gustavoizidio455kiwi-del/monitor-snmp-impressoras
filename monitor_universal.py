import os
import csv
import ipaddress
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from pysnmp.hlapi import *

# --- CONFIGURACOES ---
ARQUIVO_IPS = "ips_config.txt"
ARQUIVO_LOG = "erros.log"
ARQUIVO_STATUS = "status_atual.txt" # O novo arquivo que voce sugeriu
MAX_WORKERS = 10 

OIDS = {
    'nome': '1.3.6.1.2.1.43.11.1.1.6.1',
    'max': '1.3.6.1.2.1.43.11.1.1.8.1',
    'nivel': '1.3.6.1.2.1.43.11.1.1.9.1'
}

def registrar_log(mensagem):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {mensagem}\n")
    except: pass

def carregar_config():
    if not os.path.exists(ARQUIVO_IPS):
        with open(ARQUIVO_IPS, "w", encoding="utf-8") as f:
            f.write("# IP, Community, Timeout\n192.168.1.100, public, 2\n")
        return []
    
    alvos = []
    with open(ARQUIVO_IPS, "r", encoding="utf-8") as f:
        for linha in f:
            if linha.startswith("#") or not linha.strip(): continue
            try:
                partes = linha.strip().split(",")
                ip_str = partes[0].strip()
                ipaddress.ip_address(ip_str)
                comm = partes[1].strip() if len(partes) > 1 else "public"
                tmout = int(partes[2].strip()) if len(partes) > 2 else 2
                alvos.append({"ip": ip_str, "comm": comm, "timeout": tmout})
            except: continue
    return alvos

def snmp_walk(ip, community, oid, timeout):
    resultados = {}
    try:
        for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(
            SnmpEngine(),
            CommunityData(community, mpModel=1),
            UdpTransportTarget((ip, 161), timeout=timeout, retries=1),
            ContextData(),
            ObjectType(ObjectIdentity(oid)),
            lexicographicMode=False
        ):
            if errorIndication or errorStatus: break
            for varBind in varBinds:
                idx = str(varBind[0]).split('.')[-1]
                resultados[idx] = varBind[1]
    except: pass
    return resultados

def monitorar_host(alvo):
    ip = alvo['ip']
    nomes = snmp_walk(ip, alvo['comm'], OIDS['nome'], alvo['timeout'])
    if not nomes: return ip, None, "Inacessivel"

    maximos = snmp_walk(ip, alvo['comm'], OIDS['max'], alvo['timeout'])
    niveis = snmp_walk(ip, alvo['comm'], OIDS['nivel'], alvo['timeout'])
    
    suprimentos = []
    for idx in nomes:
        try:
            v_max, v_niv = int(maximos.get(idx, 0)), int(niveis.get(idx, 0))
            if v_niv == -3: status = "OK"
            elif v_max > 0:
                p = int((v_niv / v_max) * 100)
                status = f"CRITICO: {p}%" if p < 10 else f"{p}%"
            else: status = "N/A"
            suprimentos.append({"item": str(nomes[idx]), "status": status})
        except: continue
    return ip, suprimentos, "OK"

def iniciar():
    alvos = carregar_config()
    if not alvos: return

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        resultados = list(executor.map(monitorar_host, alvos))

    data_agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    
    # Criando o conteudo do arquivo de texto (Status Atual)
    linhas_texto = [f"RELATORIO DE IMPRESSORAS - {data_agora}\n", "-"*40 + "\n"]
    
    for ip, dados, msg in resultados:
        if dados:
            linhas_texto.append(f"HOST: {ip}\n")
            for d in dados:
                linhas_texto.append(f"  > {d['item']}: {d['status']}\n")
        else:
            linhas_texto.append(f"HOST: {ip} | STATUS: {msg}\n")
        linhas_texto.append("\n")

    # Salva o novo arquivo TXT (Sempre sobrescreve com o status mais recente)
    with open(ARQUIVO_STATUS, "w", encoding="utf-8") as f:
        f.writelines(linhas_texto)
    
    print("-" * 60)
    print(f"Monitoramento concluido.")
    print(f"Resumo salvo em: {ARQUIVO_STATUS}")
    print(f"Historico salvo em: historico_monitoramento.csv")

if __name__ == "__main__":
    try:
        iniciar()
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        print("-" * 60)
        input("Pressione ENTER para sair...")