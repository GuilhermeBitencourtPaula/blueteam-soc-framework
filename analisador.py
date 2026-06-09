
import sys
import re
import csv
import requests
import os

nome_do_arquivo = sys.argv[1]   
meu_arquivo = open(nome_do_arquivo, "r")
linhas = meu_arquivo.readlines()

contagem_ips = {}

for linha in linhas:
    if "Failed" in linha:
        padrao_ip = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        resultados = re.findall(padrao_ip, linha)
        if len(resultados) > 0:
            ip = resultados[0]
            if ip in contagem_ips:
                contagem_ips[ip] = contagem_ips[ip] + 1
            else:
                contagem_ips[ip] = 1

top_ip = ''
max_tentativas = 0
for ip, tentativas in contagem_ips.items():
    if tentativas > max_tentativas:
        max_tentativas = tentativas
        top_ip = ip

url_da_api = f"https://ip-api.com/json/{top_ip}"
resposta = requests.get(url_da_api)
dados_do_hacker = resposta.json()
if dados_do_hacker["status"] == "success":
    pais = dados_do_hacker["country"]
    cidade = dados_do_hacker["city"]
else:
    pais = "País Desconhecido (IP de Teste/Privado)"
    cidade = "Desconhecida"


print("--- RELATÓRIO DE SEGURANÇA (SOC) ---")
print(f"ALERTA: O IP {top_ip} é a maior ameaça com {max_tentativas} tentativas de invasão.")
print(f"INTELIGÊNCIA: O atacante está operando a partir de: {cidade}, {pais}")
meu_arquivo.close()
if len(contagem_ips) > 0:
    os.makedirs("relatorios", exist_ok=True)
    with open(os.path.join("relatorios", "relatorio_ataques.csv"), "w", newline="", encoding="utf-8") as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        escritor.writerow(["Endereço IP", " Tentativas de Invasão"])
        for ip, tentativas in contagem_ips.items():
            escritor.writerow([ip, tentativas])
    print("O relatório 'relatorio_ataques.csv' foi gerado com sucesso.")
else:
    print("Nenhum ataque detectado. Arquivo CSV ignorado para poupar espaço.")
