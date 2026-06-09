import requests

TOKEN = "8426333707:AAH_j3PZmPGs4UWqG8DkHGQGwjxt--UF96M"
CHAT_ID = "1616171877"

def enviar_alerta(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    pacote = {
        "chat_id": CHAT_ID,
        "text": mensagem
    }

    try:
        resposta = requests.post(url, data=pacote)

        if resposta.status_code == 200:
            print("Alerta enviado com sucesso!")
        else:
            print(f"[-] Erro ao enviar para o Telegram: {resposta.text}")
    except Exception as e:
        print(f"[-] Falha na conexão com a internet: {e}")

if __name__ == "__main__":
    enviar_alerta("🚨 ALERTA: Teste do Sistema SOC iniciado!")
