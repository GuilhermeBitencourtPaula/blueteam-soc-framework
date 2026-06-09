import customtkinter as ctk
import tkinter as tk
import hashlib
from cryptography.fernet import Fernet
from tkinter import filedialog
import random

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

janela = ctk.CTk()
janela.geometry("750x700")
janela.title("///  TERMINAL CRIPTOGRÁFICO  ///")
janela.configure(fg_color="#000000")

canvas_matrix = tk.Canvas(janela, bg='black', highlightthickness=0)
canvas_matrix.place(x=0, y=0, relwidth=1, relheight=1)

caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*!"
tamanho_fonte = 16
colunas = 3000 // tamanho_fonte 
num_gotas = 200 # Muito mais gotas simultâneas para dar volume e fluxo!

gotas_x = [random.randint(0, colunas) * tamanho_fonte for _ in range(num_gotas)]
gotas_y = [random.randint(-1500, 800) for _ in range(num_gotas)]
velocidades = [random.randint(15, 30) for _ in range(num_gotas)]

def chover_matrix():
    canvas_matrix.delete("all")
    altura_tela = janela.winfo_height()
    if altura_tela < 100: altura_tela = 1080

    for i in range(num_gotas):
        x = gotas_x[i]
        y = gotas_y[i]
        vel = velocidades[i]

        for r in range(1, 5):
            canvas_matrix.create_text(x, y - (r * tamanho_fonte), text=random.choice(caracteres), fill="#003300", font=("Consolas", tamanho_fonte))

        canvas_matrix.create_text(x, y, text=random.choice(caracteres), fill="#00FF00", font=("Consolas", tamanho_fonte, "bold"))

        gotas_y[i] += vel

        if gotas_y[i] > altura_tela:
            gotas_y[i] = random.randint(-500, 0)
            gotas_x[i] = random.randint(0, colunas) * tamanho_fonte
            velocidades[i] = random.randint(15, 30)

    janela.after(50, chover_matrix)

janela.after(500, chover_matrix)

fonte_hacker = ("Consolas", 14, "bold")
fonte_pequena = ("Consolas", 11)
cor_neon = "#00FF00"

def escrever_no_terminal(mensagem):
    saida_terminal.delete("0.0", "end")
    saida_terminal.insert("0.0", mensagem)

def limpar_entradas():
    entrada_texto.delete(0, "end")
    entrada_chave.delete(0, "end")

def acao_hash():
    texto = entrada_texto.get()
    if texto == "":
        escrever_no_terminal("[!] ERRO: Digite um alvo primeiro!")
        return
    moedor = hashlib.sha256(texto.encode())
    escrever_no_terminal(f"> HASH SHA-256 GERADO:\n{moedor.hexdigest()}")
    limpar_entradas()

def acao_criptografar():
    texto = entrada_texto.get()
    if texto == "":
        escrever_no_terminal("[!] ERRO: Digite um alvo primeiro!")
        return
    chave_mestra = Fernet.generate_key()
    cadeado = Fernet(chave_mestra)
    texto_trancado = cadeado.encrypt(texto.encode())
    escrever_no_terminal(f"> CHAVE MESTRA:\n{chave_mestra.decode()}\n\n> MENSAGEM TRANCADA:\n{texto_trancado.decode()}")
    limpar_entradas()

def acao_descriptografar():
    texto_trancado = entrada_texto.get()
    chave = entrada_chave.get()
    if texto_trancado == "" or chave == "":
        escrever_no_terminal("[!] ERRO: Preencha o texto alvo E cole a Chave Mestra na segunda caixa!")
        return
    try:
        cadeado = Fernet(chave.encode())
        texto_limpo = cadeado.decrypt(texto_trancado.encode())
        escrever_no_terminal(f"> MENSAGEM DESTRANCADA COM SUCESSO:\n{texto_limpo.decode()}")
        limpar_entradas()
    except:
        escrever_no_terminal("[!] ALERTA DE SEGURANÇA: Chave inválida ou mensagem corrompida!")

def criptografar_arquivo():
    caminho_arquivo = filedialog.askopenfilename(title="Selecione um arquivo para criptografar")
    if not caminho_arquivo:
        return
    try:
        with open(caminho_arquivo, "rb") as arquivo:
            dados_originais = arquivo.read()
        chave_mestra = Fernet.generate_key()
        cadeado = Fernet(chave_mestra)
        dados_trancados = cadeado.encrypt(dados_originais)
        caminho_salvar = caminho_arquivo + ".enc"
        with open(caminho_salvar, "wb") as arquivo_trancado:
            arquivo_trancado.write(dados_trancados)
        escrever_no_terminal(f"> SUCESSO!\nO arquivo blindado foi salvo como:\n{caminho_salvar}\n\n> CHAVE MESTRA (GUARDE ISSO!):\n{chave_mestra.decode()}")
    except Exception as e:
        escrever_no_terminal(f"[!] ERRO AO PROCESSAR ARQUIVO: {e}")

def limpar_tela():
    saida_terminal.delete("0.0", "end")
    saida_terminal.insert("0.0", "> TERMINAL LIMPO. AGUARDANDO COMANDOS...\n")
    limpar_entradas()

titulo = ctk.CTkLabel(janela, text="SYS.ENCRYPT // ROOT_ACCESS", font=("Consolas", 22, "bold"), text_color=cor_neon)
titulo.pack(pady=(20, 0))
subtitulo = ctk.CTkLabel(janela, text="Desenvolvido por Guilherme Bitencourt - Blue Team Security Tool", font=fonte_pequena, text_color="gray")
subtitulo.pack(pady=(0, 20))

frame_texto = ctk.CTkFrame(janela, fg_color="#111111", border_color=cor_neon, border_width=1)
frame_texto.pack(pady=10, padx=20, fill="x")

label_alvo = ctk.CTkLabel(frame_texto, text="Texto Original ou Mensagem Trancada:", font=fonte_pequena, text_color=cor_neon)
label_alvo.pack(pady=(10, 0), padx=20, anchor="w")
entrada_texto = ctk.CTkEntry(frame_texto, font=fonte_hacker, text_color=cor_neon, fg_color="black", border_color=cor_neon)
entrada_texto.pack(pady=(0, 10), padx=20, fill="x")

label_chave = ctk.CTkLabel(frame_texto, text="Sua Chave Mestra (Apenas para Descriptografia):", font=fonte_pequena, text_color=cor_neon)
label_chave.pack(pady=(10, 0), padx=20, anchor="w")
entrada_chave = ctk.CTkEntry(frame_texto, font=fonte_hacker, text_color=cor_neon, fg_color="black", border_color=cor_neon)
entrada_chave.pack(pady=(0, 15), padx=20, fill="x")

frame_botoes = ctk.CTkFrame(frame_texto, fg_color="transparent")
frame_botoes.pack(pady=(0, 15))

botao_hash = ctk.CTkButton(frame_botoes, text="GERAR HASH", command=acao_hash, font=fonte_hacker, text_color="black", fg_color=cor_neon, hover_color="#00CC00", width=200)
botao_hash.pack(side="left", padx=10)

botao_cripto = ctk.CTkButton(frame_botoes, text="CRIPTOGRAFAR TEXTO", command=acao_criptografar, font=fonte_hacker, text_color="black", fg_color=cor_neon, hover_color="#00CC00", width=200)
botao_cripto.pack(side="left", padx=10)

botao_descripto = ctk.CTkButton(frame_botoes, text="DESCRIPTOGRAFAR TEXTO", command=acao_descriptografar, font=fonte_hacker, text_color="black", fg_color=cor_neon, hover_color="#00CC00", width=200)
botao_descripto.pack(side="left", padx=10)

frame_arquivo = ctk.CTkFrame(janela, fg_color="#111111", border_color="#FF0000", border_width=1)
frame_arquivo.pack(pady=10, padx=20, fill="x")

label_arq = ctk.CTkLabel(frame_arquivo, text="Módulo Avançado: Criptografia de Arquivos Locais (Anti-Ransomware)", font=fonte_pequena, text_color="#FF0000")
label_arq.pack(pady=(10, 5))

botao_arquivo = ctk.CTkButton(frame_arquivo, text=" SELECIONAR E CRIPTOGRAFAR ARQUIVO ", command=criptografar_arquivo, font=fonte_hacker, text_color="black", fg_color="#FF0000", hover_color="#CC0000")
botao_arquivo.pack(pady=(5, 15))

frame_terminal = ctk.CTkFrame(janela, fg_color="transparent")
frame_terminal.pack(pady=10, padx=20, fill="both", expand=True)

saida_terminal = ctk.CTkTextbox(frame_terminal, font=("Consolas", 12), text_color=cor_neon, fg_color="black", border_color=cor_neon, border_width=1)
saida_terminal.pack(fill="both", expand=True, side="left")
saida_terminal.insert("0.0", "> SISTEMA INICIADO.\n> AGUARDANDO COMANDOS...\n")

botao_limpar = ctk.CTkButton(frame_terminal, text=" LIMPAR TERMINAL ", command=limpar_tela, font=fonte_hacker, text_color="black", fg_color="#FFD700", hover_color="#FFEA00", width=120)
botao_limpar.pack(side="right", padx=(10, 0), anchor="s")

janela.mainloop()