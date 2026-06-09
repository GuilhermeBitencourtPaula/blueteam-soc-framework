import socket
import sys
import concurrent.futures

# Mapeamento de portas conhecidas
portas_conhecidas = {
    20: "FTP (Dados)",
    21: "FTP (Controle) - Risco de Vazamento de Arquivos",
    22: "SSH - Acesso Remoto",
    23: "Telnet - Acesso Remoto INSEGURO",
    25: "SMTP - E-mail",
    53: "DNS",
    80: "HTTP - Servidor Web Desprotegido",
    135: "RPC - Serviço Interno do Windows",
    443: "HTTPS - Servidor Web Seguro",
    445: "SMB - Compartilhamento de Arquivos Windows (Alvo de Ransomwares!)"
}

def scan_porta(ip, porta):
    telefone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    telefone.settimeout(0.5) 
    
    resposta = telefone.connect_ex((ip, porta))
    
    if resposta == 0:
        servico = portas_conhecidas.get(porta, "Serviço Desconhecido")
        print(f"[!] ALERTA: Porta {porta} ABERTA | Serviço: {servico}")
        
    telefone.close()

print("/// INICIANDO VARREDURA DE PORTAS (MODO TURBO) ///")

if len(sys.argv) > 1:
    alvo = sys.argv[1]
else:
    alvo = "127.0.0.1"
    
print(f"Alvo: {alvo}")
print("Escaneando portas de 20 a 1024 simultaneamente...")

# Motor de varredura multithread
try:
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        for porta in range(20, 1025):
            executor.submit(scan_porta, meu_ip, porta)
            
except KeyboardInterrupt:
    print("\n[!] Varredura cancelada pelo usuário.")
    sys.exit()

print("\n/// VARREDURA CONCLUÍDA ///")