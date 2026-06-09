import sqlite3

def inicializar_banco():
    conexao = sqlite3.connect("sistema_secreto.db")
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            saldo REAL
        )
    """)

    cursor.execute("DELETE FROM usuarios")
    cursor.execute("INSERT INTO usuarios (username, password, saldo) VALUES ('admin', 'SenhaSuperMestraInvasavel_2026', 1500000.00)")

    conexao.commit()
    return conexao

def login_vulneravel(conexao, usuario, senha):
    cursor = conexao.cursor()

    query = "SELECT * FROM usuarios WHERE username = ? AND password = ?"

    print(f"\n[DEBUG DO SISTEMA] O banco de dados recebeu o comando:\n-> {query}\n")

    try:
        cursor.execute(query, (usuario, senha))
        resultado = cursor.fetchone()

        if resultado:
            print("="*45)
            print(f"[!] ACESSO CONCEDIDO: Bem-vindo, {resultado[1]}!")
            print(f"[!] Saldo em Conta: R$ {resultado[3]:.2f}")
            print("="*45 + "\n")
        else:
            print("[-] ACESSO NEGADO: Usuário ou senha incorretos.\n")

    except Exception as e:
        print(f"[-] Erro fatal no Banco de Dados: {e}\n")

print("/// BANCO CENTRAL INICIADO ///\n")
db = inicializar_banco()

print("Por favor, faça o login para acessar a área restrita.")
usr = input("Usuário: ")
pwd = input("Senha: ")

login_vulneravel(db, usr, pwd)
db.close()
