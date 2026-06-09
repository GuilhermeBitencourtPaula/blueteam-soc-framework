# 🛡️ BlueTeam SOC Framework

Bem-vindo ao **BlueTeam SOC (Security Operations Center) Framework**. 
Este projeto é uma suíte de segurança defensiva e ofensiva desenvolvida inteiramente em Python. Ele possui uma Interface Gráfica (GUI) moderna que orquestra diversas ferramentas de Cibersegurança em tempo real.

[Interface do Painel SOC](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
[Tkinter GUI](https://img.shields.io/badge/Tkinter-Modern_UI-green?style=for-the-badge)

*Arquitetura do Sistema*

O framework foi construído com a mentalidade de "Separação de Preocupações" (Separation of Concerns). O arquivo central (`painel_soc.py`) atua como um maestro, abrindo instâncias independentes no terminal para cada módulo de inteligência e varredura.

Os logs e relatórios são salvos em um "cofre" (a pasta `relatorios/`) e processados pela interface para fácil leitura, contendo um sistema nativo de filtros e exclusão forense.

 Módulos de Operação

1.  Analisador Forense (Logs)
Ferramenta defensiva projetada para investigar arquivos de log de servidores web (ex: Nginx/Apache). Ele utiliza Expressões Regulares (RegEx) para identificar assinaturas de ataques SQL Injection e mapear os endereços IP dos atacantes geograficamente via API. O resultado final é compilado em um relatório tático (CSV).

 2.  Cofre Criptográfico (AES-256)
Módulo de Data Security. Utiliza a biblioteca `cryptography` para implementar criptografia assimétrica/simétrica de grau militar (Padrão AES-256). Protege textos sensíveis ou simula sistemas de proteção contra vazamentos.

 3.  Scanner de Vulnerabilidade (Rede)
Ferramenta ofensiva/defensiva construída com a biblioteca `socket`. Realiza varreduras de portas abertas (Port Scanning) utilizando múltiplas Threads (processamento paralelo) para máxima velocidade, identificando serviços expostos na rede alvo.

 4.  Sabujo de Inteligência (OSINT)
Módulo de *Threat Intelligence*. Baseado em técnicas de Reconhecimento passivo. Ele varre diretórios expostos, mapeia subdomínios via Certificados SSL (crt.sh) e identifica portas abertas silenciosamente. O dossiê completo é salvo no banco de relatórios.

 5.  Honeypot (Armadilha TCP)
Um simulador de alvo fácil. O Honeypot escuta silenciosamente uma porta arbitrária (ex: 10000) fingindo ser um servidor vulnerável. Quando um atacante tenta a invasão, o script corta a conexão, extrai o *Payload* utilizado, registra o IP, e **envia um Alerta em Tempo Real via Telegram Bot** para o celular do administrador do SOC.

 6. Simulador de Injeção SQL
Laboratório interativo baseado em `sqlite3` construído com código vulnerável intencional (ausência de queries parametrizadas). É utilizado estritamente para propósitos educacionais, demonstrando como falhas de autenticação (`' OR 1=1 --`) ocorrem no mundo real.

  Como Executar

 Pré-requisitos
- Python 3.x
- Instale as dependências executando:
  ```bash
  pip install requests cryptography
  ```

 Inicialização
Para iniciar o Painel Central de Operações, execute no seu terminal:
```bash
python painel_soc.py
```

---
*Este projeto foi desenvolvido com foco educacional em Arquitetura de Software e Cibersegurança.*
