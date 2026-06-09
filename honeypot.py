import socket
import datetime
import notificador_telegram

# Configurações do Honeypot
IP_ISCA = "127.0.0.1"
PORTA_ISCA = 10000

def iniciar_honeypot():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((IP_ISCA, PORTA_ISCA))
    servidor.listen(5)
    
    print("=====================================================")
    print("🛡️  HONEYPOT ATIVADO: A TEIA DE ARANHA ESTÁ ARMADA 🛡️")
    print(f"[*] Escutando silenciosamente na porta {PORTA_ISCA}...")
    print("=====================================================\n")

    try:
        while True:
            cliente, endereco = servidor.accept()
            ip_invasor = endereco[0]
            porta_invasor = endereco[1]
            hora_ataque = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"[!!!] ALARME VERMELHO - INTRUSÃO DETECTADA [!!!]")
            print(f"[*] IP do Invasor: {ip_invasor}")
            print(f"[*] Porta de Origem: {porta_invasor}")
            print(f"[*] Data e Hora da Tentativa: {hora_ataque}")
            
            cliente.settimeout(2.0)
            
            dados_decodificados = "Nenhum dado enviado."
            try:
                dados = cliente.recv(1024)
                if dados:
                    dados_decodificados = dados.decode('utf-8', errors='ignore')
                    print(f"[*] Assinatura da Ferramenta de Ataque (Payload):\n{dados_decodificados}")
            except Exception as e:
                print(f"[-] O invasor não mandou carga útil. ({e})")
            
            import os
            os.makedirs("relatorios", exist_ok=True)
            with open(os.path.join("relatorios", "alertas_intrusao.txt"), "a", encoding="utf-8") as arquivo_log:
                arquivo_log.write(f"[{hora_ataque}] INVASÃO BLOQUEADA | IP: {ip_invasor} | PORTA: {porta_invasor}\n")
                arquivo_log.write(f"PAYLOAD:\n{dados_decodificados}\n")
                arquivo_log.write("-" * 50 + "\n")

                alerta_msg = (
                    f"🚨 INVASÃO DETECTADA!\n\n"
                    f"Alvo: Honeypot\n"
                    f"Atacante IP: {ip_invasor}\n"
                    f"Porta: {porta_invasor}"
                )
            try:
                notificador_telegram.enviar_alerta(alerta_msg)
            except Exception:
                pass

            cliente.close()
            print("[-] A conexão com o invasor foi cortada pela defesa.\n")
            print("-----------------------------------------------------")
            print(f"[*] Escutando silenciosamente na porta {PORTA_ISCA}...\n")
            
    except KeyboardInterrupt:
        print("\n[!] Honeypot desativado pelo administrador.")
        servidor.close()

if __name__ == "__main__":
    iniciar_honeypot()
