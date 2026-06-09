import tkinter as tk
from tkinter import ttk, scrolledtext
import os

BG_DARK = "#1E1E1E"       # Fundo principal
BG_PANEL = "#252526"      # Fundo dos painéis
BG_HOVER = "#2D2D30"      # Fundo ao passar o mouse
ACCENT = "#00A67D"        # Verde-azulado premium (Cyberpunk)
TEXT_MAIN = "#FFFFFF"     # Texto principal
TEXT_MUTED = "#CCCCCC"    # Texto secundário
FONT_UI = ("Segoe UI", 11)
FONT_TITLE = ("Segoe UI", 24, "bold")
FONT_CODE = ("Consolas", 11)

def lançar_ferramenta(nome_script, argumentos=""):
    comando = f'start cmd /k "title SOC - {nome_script} & color 0a & python {nome_script} {argumentos}"'
    os.system(comando)

def pedir_alvo_e_lancar(script, titulo, mensagem, valor_padrao=""):
    dialog = tk.Toplevel(janela)
    dialog.title(titulo)

    largura = 400
    altura = 200
    pos_x = (dialog.winfo_screenwidth() // 2) - (largura // 2)
    pos_y = (dialog.winfo_screenheight() // 2) - (altura // 2)
    dialog.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    dialog.configure(bg=BG_PANEL)
    dialog.transient(janela) # Fica por cima
    dialog.grab_set() # Bloqueia a janela principal

    tk.Label(dialog, text=mensagem, font=("Segoe UI", 11, "bold"), fg=TEXT_MAIN, bg=BG_PANEL).pack(pady=(30, 10))
    entrada = tk.Entry(dialog, font=("Segoe UI", 12), bg=BG_DARK, fg=ACCENT, insertbackground=TEXT_MAIN, relief="flat", width=30)
    entrada.pack(pady=10)
    entrada.insert(0, valor_padrao)

    def confirmar():
        alvo = entrada.get().strip()
        dialog.destroy()
        if alvo:
            lançar_ferramenta(script, alvo)
        else:
            lançar_ferramenta(script)

    btn = tk.Button(dialog, text="INICIAR MISSÃO", command=confirmar, font=("Segoe UI", 10, "bold"), fg=BG_DARK, bg=ACCENT, relief="flat", cursor="hand2", width=20)
    btn.pack(pady=10)

def carregar_lista_relatorios():
    lista_arquivos.delete(0, tk.END)
    arquivos_na_pasta = os.listdir('.')

    for arquivo in arquivos_na_pasta:
        if arquivo.endswith('.txt') or arquivo.endswith('.csv'):
            if arquivo in ["requirements.txt", "server_logs.txt"]:
                continue

            tag = "[DOC]"
            if "alertas_intrusao" in arquivo:
                tag = "[HONEYPOT]"
            elif "relatorio_ataques" in arquivo:
                tag = "[FORENSE ]"
            elif "relatorio_infra" in arquivo:
                tag = "[ OSINT  ]"

            lista_arquivos.insert(tk.END, f"  {tag}  {arquivo}")

def ler_arquivo_selecionado(event):
    selecao = lista_arquivos.curselection()
    if not selecao:
        return

    item_texto = lista_arquivos.get(selecao[0]).strip()
    nome_real = item_texto.split("]  ")[1]

    tela_leitura.config(state='normal')
    tela_leitura.delete(1.0, tk.END)

    try:
        caminho_completo = os.path.join("relatorios", nome_real)
        with open(caminho_completo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
            tela_leitura.insert(tk.END, conteudo)
    except Exception as e:
        tela_leitura.insert(tk.END, f"Erro ao ler o arquivo: {e}")

    tela_leitura.config(state='disabled')

def on_enter(e):
    e.widget['background'] = ACCENT
    e.widget['foreground'] = BG_DARK

def on_leave(e):
    e.widget['background'] = BG_PANEL
    e.widget['foreground'] = ACCENT

janela = tk.Tk()
janela.title("SOC - Security Operations Center")
janela.geometry("1000x650")
janela.configure(bg=BG_DARK)

estilo = ttk.Style()
estilo.theme_use('clam') 
estilo.configure("TNotebook", background=BG_DARK, borderwidth=0)
estilo.configure("TNotebook.Tab", background=BG_PANEL, foreground=TEXT_MAIN, padding=[25, 10], font=("Segoe UI", 10, "bold"), borderwidth=0, focuscolor=BG_PANEL)
estilo.map("TNotebook.Tab", background=[("selected", ACCENT)], foreground=[("selected", BG_DARK)], focuscolor=[("selected", ACCENT)])

abas = ttk.Notebook(janela)
abas.pack(expand=True, fill='both', padx=10, pady=10)

aba_arsenal = tk.Frame(abas, bg=BG_DARK)
abas.add(aba_arsenal, text="🛡️ MÓDULOS DE OPERAÇÃO")

header_frame = tk.Frame(aba_arsenal, bg=BG_DARK)
header_frame.pack(pady=(40, 20))
tk.Label(header_frame, text="CENTRAL DE COMANDO TÁTICO", font=FONT_TITLE, fg=TEXT_MAIN, bg=BG_DARK).pack()
tk.Label(header_frame, text="Selecione um módulo para iniciar um terminal de segurança blindado independente.", font=FONT_UI, fg=TEXT_MUTED, bg=BG_DARK).pack(pady=5)

grade_botoes = tk.Frame(aba_arsenal, bg=BG_DARK)
grade_botoes.pack(pady=20)

def criar_botao(parent, texto, comando, row, col):
    btn = tk.Button(parent, text=texto, command=comando, font=("Segoe UI", 11, "bold"), 
                    fg=ACCENT, bg=BG_PANEL, activebackground=ACCENT, activeforeground=BG_DARK, 
                    width=38, height=3, relief="flat", bd=0, cursor="hand2", takefocus=0)
    btn.grid(row=row, column=col, padx=15, pady=15)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

criar_botao(grade_botoes, "🕵️ Analisador Forense (Logs)", lambda: pedir_alvo_e_lancar("analisador.py", "Alvo Forense", "Digite o nome do arquivo de log:", "server_logs.txt"), 0, 0)
criar_botao(grade_botoes, "🔐 Cofre Criptográfico (AES-256)", lambda: lançar_ferramenta("cripto_gui.py"), 0, 1)
criar_botao(grade_botoes, "📡 Scanner de Vulnerabilidade (Rede)", lambda: pedir_alvo_e_lancar("scanner.py", "Alvo do Scanner", "Digite o IP do servidor alvo:", ""), 1, 0)
criar_botao(grade_botoes, "🌐 Sabujo de Inteligência (OSINT)", lambda: pedir_alvo_e_lancar("sabujo.py", "Alvo de Espionagem", "Digite o domínio da empresa alvo:", ""), 1, 1)
criar_botao(grade_botoes, "🕸️ Honeypot (Armadilha TCP)", lambda: lançar_ferramenta("honeypot.py"), 2, 0)
criar_botao(grade_botoes, "💥 Simulador de Injeção SQL", lambda: lançar_ferramenta("banco_vulneravel.py"), 2, 1)

aba_relatorios = tk.Frame(abas, bg=BG_DARK)
abas.add(aba_relatorios, text="📊 INTELIGÊNCIA E RELATÓRIOS")

frame_lista = tk.Frame(aba_relatorios, bg=BG_PANEL, width=320)
frame_lista.pack(side="left", fill="y", padx=(20, 10), pady=20)
frame_lista.pack_propagate(False)

tk.Label(frame_lista, text="BASES DE DADOS", font=("Segoe UI", 12, "bold"), fg=TEXT_MAIN, bg=BG_PANEL).pack(pady=(15, 5))

frame_filtros = tk.Frame(frame_lista, bg=BG_PANEL)
frame_filtros.pack(fill="x", padx=10, pady=5)

def filtrar(tag_filtro):
    os.makedirs("relatorios", exist_ok=True)

    try:
        botoes = {"TODOS": btn_todos, "OSINT": btn_osint, "HONEYPOT": btn_honey, "FORENSE": btn_forense}
        for tag, btn in botoes.items():
            if tag == tag_filtro:
                btn.config(bg=ACCENT, fg=BG_DARK) # Aba Ativa (Verde)
            else:
                btn.config(bg="#333333", fg=ACCENT) # Aba Inativa (Cinza)
    except NameError:
        pass # Se a função for chamada antes de desenhar a tela

    lista_arquivos.delete(0, tk.END)
    arquivos_na_pasta = os.listdir('relatorios')

    for arquivo in arquivos_na_pasta:
        if arquivo.endswith('.txt') or arquivo.endswith('.csv'):
            if arquivo in ["requirements.txt", "server_logs.txt"]:
                continue

            tag = "[DOC]"
            if "alertas_intrusao" in arquivo:
                tag = "[HONEYPOT]"
            elif "relatorio_ataques" in arquivo:
                tag = "[FORENSE]"
            elif "relatorio_infra" in arquivo:
                tag = "[OSINT]"

            if tag_filtro == "TODOS" or tag_filtro in tag:
                lista_arquivos.insert(tk.END, f"  {tag}  {arquivo}")

    tela_leitura.config(state='normal')
    tela_leitura.delete(1.0, tk.END)
    tela_leitura.config(state='disabled')

estilo_filtro = {"font": ("Segoe UI", 9, "bold"), "fg": ACCENT, "bg": "#333333", "activebackground": ACCENT, "activeforeground": BG_DARK, "relief": "flat", "cursor": "hand2", "pady": 4, "takefocus": 0}
btn_todos = tk.Button(frame_filtros, text="TODOS", command=lambda: filtrar("TODOS"), **estilo_filtro)
btn_todos.pack(side="left", expand=True, fill="x", padx=1)
btn_osint = tk.Button(frame_filtros, text="OSINT", command=lambda: filtrar("OSINT"), **estilo_filtro)
btn_osint.pack(side="left", expand=True, fill="x", padx=1)
btn_honey = tk.Button(frame_filtros, text="HONEYPOT", command=lambda: filtrar("HONEYPOT"), **estilo_filtro)
btn_honey.pack(side="left", expand=True, fill="x", padx=1)
btn_forense = tk.Button(frame_filtros, text="FORENSE", command=lambda: filtrar("FORENSE"), **estilo_filtro)
btn_forense.pack(side="left", expand=True, fill="x", padx=1)

lista_arquivos = tk.Listbox(frame_lista, font=("Consolas", 10), bg=BG_PANEL, fg=TEXT_MUTED, 
                            selectbackground=ACCENT, selectforeground=BG_DARK, borderwidth=0, highlightthickness=0, activestyle="none")
lista_arquivos.pack(expand=True, fill="both", padx=10, pady=5)
lista_arquivos.bind('<<ListboxSelect>>', ler_arquivo_selecionado)

def excluir_relatorio():
    selecao = lista_arquivos.curselection()
    if not selecao:
        return
    item_texto = lista_arquivos.get(selecao[0]).strip()
    nome_real = item_texto.split("]  ")[1]

    try:
        caminho_completo = os.path.join("relatorios", nome_real)
        os.remove(caminho_completo)
        tela_leitura.config(state='normal')
        tela_leitura.delete(1.0, tk.END)
        tela_leitura.insert(tk.END, f"[!] Arquivo '{nome_real}' foi excluído e destruído do servidor com sucesso.")
        tela_leitura.config(state='disabled')
        filtrar("TODOS")
    except Exception as e:
        pass

frame_botoes_lista = tk.Frame(frame_lista, bg=BG_PANEL)
frame_botoes_lista.pack(fill="x", padx=10, pady=10)

btn_atualizar = tk.Button(frame_botoes_lista, text="↻ Atualizar", command=lambda: filtrar("TODOS"), 
                          font=("Segoe UI", 9, "bold"), fg=BG_DARK, bg=ACCENT, relief="flat", cursor="hand2", pady=8, takefocus=0)
btn_atualizar.pack(side="left", expand=True, fill="x", padx=(0, 2))

btn_excluir = tk.Button(frame_botoes_lista, text="🗑️ Excluir", command=excluir_relatorio, 
                          font=("Segoe UI", 9, "bold"), fg="#FFFFFF", bg="#8B0000", relief="flat", cursor="hand2", pady=8, takefocus=0)
btn_excluir.pack(side="right", expand=True, fill="x", padx=(2, 0))

frame_visor = tk.Frame(aba_relatorios, bg=BG_PANEL)
frame_visor.pack(side="right", expand=True, fill="both", padx=(10, 20), pady=20)

tk.Label(frame_visor, text="VISUALIZADOR FORENSE", font=("Segoe UI", 12, "bold"), fg=TEXT_MAIN, bg=BG_PANEL).pack(pady=(15, 5))

tela_leitura = scrolledtext.ScrolledText(frame_visor, font=FONT_CODE, bg="#181818", fg="#4EC9B0", 
                                         insertbackground=TEXT_MAIN, borderwidth=0, highlightthickness=0, state='disabled', padx=15, pady=15)
tela_leitura.pack(expand=True, fill="both", padx=10, pady=(0, 10))

rodape = tk.Frame(janela, bg=ACCENT, height=25)
rodape.pack(side="bottom", fill="x")
tk.Label(rodape, text="Blue Team SOC Framework v2.0 - Sistema Autenticado", font=("Segoe UI", 9, "bold"), fg=BG_DARK, bg=ACCENT).pack(pady=2)

filtrar("TODOS")
janela.mainloop()
