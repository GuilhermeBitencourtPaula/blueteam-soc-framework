import sqlite3

def inicializar_banco():
    # Conecta a um banco de dados local chamado "sistema_secreto.db"
    conexao = sqlite3.connect("sistema_secreto.db")
    cursor = conexao.cursor()
    
    # Cria a tabela de usuários (como em qualquer sistema real)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            saldo REAL
        )
    """)
    
    # Limpa a tabela para o teste e insere nosso alvo (o Administrador)
    cursor.execute("DELETE FROM usuarios")
    cursor.execute("INSERT INTO usuarios (username, password, saldo) VALUES ('admin', 'SenhaSuperMestraInvasavel_2026', 1500000.00)")
    
    conexao.commit()
    return conexao

def login_vulneravel(conexao, usuario, senha):
    cursor = conexao.cursor()
    
    # A VULNERABILIDADE CLÁSSICA: Concatenar variáveis diretamente na String do SQL!
    query = "SELECT * FROM usuarios WHERE username = ? AND password = ?"
    
    
    # Imprimimos a Query na tela para entendermos o que o Banco está processando de verdade
    print(f"\n[DEBUG DO SISTEMA] O banco de dados recebeu o comando:\n-> {query}\n")
    
    try:
        # Tenta executar o comando
        cursor.execute(query, (usuario, senha))
        resultado = cursor.fetchone()
        
        # Se ele encontrou alguma linha que seja verdadeira, o login é aprovado
        if resultado:
            print("="*45)
            print(f"[!] ACESSO CONCEDIDO: Bem-vindo, {resultado[1]}!")
            print(f"[!] Saldo em Conta: R$ {resultado[3]:.2f}")
            print("="*45 + "\n")
        else:
            print("[-] ACESSO NEGADO: Usuário ou senha incorretos.\n")
            
    except Exception as e:
        print(f"[-] Erro fatal no Banco de Dados: {e}\n")

# ------- MOTOR PRINCIPAL -------
print("/// BANCO CENTRAL INICIADO ///\n")
db = inicializar_banco()

print("Por favor, faça o login para acessar a área restrita.")
usr = input("Usuário: ")
pwd = input("Senha: ")

login_vulneravel(db, usr, pwd)
db.close()
