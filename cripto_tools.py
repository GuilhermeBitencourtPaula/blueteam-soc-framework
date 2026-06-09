from cryptography.fernet import Fernet
import hashlib

print("=== BEM-VINDO À FERRAMENTA BLUE TEAM ===")
print("[1] Gerar um Hash de Senha")
print("[2] Criptografar uma Mensagem")
opcao = input("Escolha a sua opção (1 ou 2): ")

texto= input("Digite a senha ou mensagem: ")

if opcao == "1":
    print("\n--- GERANDO HASH ---")
    texto_bytes = texto.encode('')
    moedor = hashlib.sha256(texto_bytes)
    print(f"O Hash protegido é: {moedor.hexdigest()}")
elif opcao == "2":
    print("\n--- CRIPTOGRAFANDO ---")
    chave_mestra = Fernet.generate_key()
    cadeado = Fernet(chave_mestra)
    texto_bytes = texto.encode()
    texto_trancado = cadeado.encrypt(texto_bytes)

    print(f"Guarde sua Chave Mestra: {chave_mestra.decode()}") 
    print(f"Mensagem Trancada: {texto_trancado.decode()}")

else:
    print("Opção inválida. Tente novamente.")
