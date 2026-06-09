import requests
import sys
import os
import urllib3

# Oculta o aviso vermelho do "InsecureRequestWarning" na tela
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("/// SABUJO WEB (OSINT DE INFRAESTRUTURA) INICIADO ///\n")

# Alvo oficial do nosso Bug Bounty Educacional
# A Tesla é conhecida por ter um programa de Bug Bounty aberto e muitos subdomínios públicos
# Agora ele aceita o domínio diretamente do Painel SOC, senão usa o padrão
if len(sys.argv) > 1:
    alvo_dominio = sys.argv[1]
else:
    alvo_dominio = "ticketgd.com.br"
    
alvo_url = f"https://{alvo_dominio}"

print(f"[*] Alvo Primário: {alvo_dominio}\n")

# ---------------------------------------------------------
# FASE 1: INSPEÇÃO DE CABEÇALHOS (HEADERS)
# ---------------------------------------------------------
print("[+] Fase 1: Inspecionando Cabeçalhos do Servidor...")
try:
    # Usamos timeout e ignoramos erros de certificado (verify=False)
    # porque as vezes servidores antigos da empresa tem certificados vencidos
    resposta = requests.get(alvo_url, timeout=5, verify=False)
    cabecalhos = resposta.headers
    
    # Procurando vazamento de tecnologia
    servidor = cabecalhos.get("Server", "Oculto/Não Informado")
    tecnologia = cabecalhos.get("X-Powered-By", "Oculto/Não Informado")
    
    print(f"    -> Servidor detectado: {servidor}")
    print(f"    -> Tecnologia por trás (X-Powered-By): {tecnologia}")
    
    # Verificando segurança
    if "Strict-Transport-Security" not in cabecalhos:
        print("    [!] AVISO: O site pode não estar forçando HTTPS (Falta HSTS).")
    if "X-Frame-Options" not in cabecalhos:
        print("    [!] AVISO: O site está vulnerável a Clickjacking (Falta X-Frame-Options).")

except requests.exceptions.RequestException as e:
    print(f"[-] Erro ao conectar no alvo principal: {e}")

print("\n")

# ---------------------------------------------------------
# FASE 2 e 3: ENUMERAÇÃO DE SUBDOMÍNIOS (Plano B: HackerTarget)
# ---------------------------------------------------------
print("[+] Fase 2: Consultando API de Inteligência (HackerTarget)...")
print("    Como o crt.sh estava instável, acionamos nosso Plano B de busca...")

# O HackerTarget é uma API lendária no OSINT que retorna texto/CSV com o Subdomínio e o IP
url_api = f"https://api.hackertarget.com/hostsearch/?q={alvo_dominio}"

try:
    resposta_api = requests.get(url_api, timeout=15)
    
    if resposta_api.status_code == 200:
        # Lemos o texto recebido e separamos linha por linha
        linhas = resposta_api.text.split("\n")
        
        subdominios_encontrados = set()
        
        for linha in linhas:
            if "," in linha:
                # O formato é "subdominio.com,192.168.0.1". Vamos dividir na vírgula e pegar a parte 0 (o domínio)
                subdominio = linha.split(",")[0]
                if "*" not in subdominio:
                    subdominios_encontrados.add(subdominio.lower())
                    
        print(f"[!] ALERTA CRÍTICO: Foram descobertos {len(subdominios_encontrados)} subdomínios públicos vinculados a {alvo_dominio}!\n")
        
        # ---------------------------------------------------------
        # FASE 4: RELATÓRIO TÁTICO
        # ---------------------------------------------------------
        if len(subdominios_encontrados) > 0:
            os.makedirs("relatorios", exist_ok=True)
            nome_arquivo = os.path.join("relatorios", f"relatorio_infra_{alvo_dominio}.txt")
            with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
                arquivo.write(f"RELATORIO DE INFRAESTRUTURA - {alvo_dominio.upper()}\n")
                arquivo.write("="*50 + "\n\n")
                arquivo.write(">>> SUBDOMÍNIOS ENCONTRADOS <<<\n")
                
                # Mostramos apenas os primeiros 15 na tela para não travar o terminal
                contador = 0
                for sub in sorted(subdominios_encontrados):
                    if contador < 15:
                        print(f"    -> {sub}")
                    contador += 1
                    
                    # Mas salvamos todos no arquivo!
                    arquivo.write(f"{sub}\n")
                    
                if len(subdominios_encontrados) > 15:
                    print(f"    ... e mais {len(subdominios_encontrados) - 15} portas dos fundos ocultas!")
                    
            print(f"\n[+] Relatório de Inteligência salvo com sucesso em: {nome_arquivo}")
        else:
            print("\n[-] Nenhum subdomínio foi encontrado. Geração de relatório ignorada.")

    else:
        print(f"[-] O crt.sh negou a conexão. Código: {resposta_api.status_code}")

except Exception as e:
    print(f"[-] Erro ao consultar a API do crt.sh: {e}")

print("\n/// SABUJO FINALIZADO ///")