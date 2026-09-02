import argparse
import os
from datetime import datetime

# Pega dinamicamente a pasta Downloads do usuário logado atualmente
pasta_downloads = os.path.join(os.path.expanduser("~"), "Downloads")

# Configuração para receber o destino e a origem via linha de comando
parser = argparse.ArgumentParser(
    description="Gera a árvore de diretórios (apenas pastas) com os tipos de arquivos e salva em arquivo de texto."
)
parser.add_argument(
    "--caminho",
    "-c",
    default=pasta_downloads,
    help="Caminho do diretório de destino (padrão: Downloads do usuário)",
)
parser.add_argument(
    "--origem",
    "-o",
    default=".",
    help="Diretório que você deseja mapear (padrão: pasta atual)",
)
args = parser.parse_args()

# Garante que a pasta de destino existe
os.makedirs(args.caminho, exist_ok=True)

# Pega o nome da pasta
caminho_absoluto = os.path.abspath(args.origem)
nome_pasta = os.path.basename(caminho_absoluto)

# Tratativa caso seja a raiz do disco (ex: C:\) para evitar nome vazio
if not nome_pasta:
    nome_pasta = caminho_absoluto.replace(":", "").replace("\\", "_")

# Gera a data e o nome do arquivo .txt no formato desejado
data_hoje = datetime.now().strftime("%d_%m_%Y")
nome_arquivo = f"EPA_Pastas_{nome_pasta}_{data_hoje}.txt"
caminho_completo = os.path.join(args.caminho, nome_arquivo)

def gerar_arvore_pastas(dir_atual, prefixo=""):
    linhas = []
    try:
        entradas = sorted(os.listdir(dir_atual))
    except PermissionError:
        return []

    # Filtra apenas subdiretórios
    pastas = [e for e in entradas if os.path.isdir(os.path.join(dir_atual, e))]
    
    for i, pasta in enumerate(pastas):
        caminho_pasta = os.path.join(dir_atual, pasta)
        
        # Coleta as extensões dos arquivos existentes diretamente dentro desta pasta
        try:
            arquivos = [f for f in os.listdir(caminho_pasta) if os.path.isfile(os.path.join(caminho_pasta, f))]
            extensoes = sorted(set(os.path.splitext(f)[1].lower() for f in arquivos if os.path.splitext(f)[1]))
        except PermissionError:
            extensoes = []

        ext_str = f" [{', '.join(extensoes)}]" if extensoes else ""
        
        eh_ultimo = (i == len(pastas) - 1)
        conector = "└── " if eh_ultimo else "├── "
        
        linhas.append(f"{prefixo}{conector}{pasta}{ext_str}")
        
        # Recursão para subpastas
        novo_prefixo = prefixo + ("    " if eh_ultimo else "│   ")
        linhas.extend(gerar_arvore_pastas(caminho_pasta, novo_prefixo))
        
    return linhas

# Coleta extensões da pasta raiz (origem) também
try:
    arquivos_raiz = [f for f in os.listdir(caminho_absoluto) if os.path.isfile(os.path.join(caminho_absoluto, f))]
    ext_raiz = sorted(set(os.path.splitext(f)[1].lower() for f in arquivos_raiz if os.path.splitext(f)[1]))
except PermissionError:
    ext_raiz = []

ext_raiz_str = f" [{', '.join(ext_raiz)}]" if ext_raiz else ""
linhas_totais = [f"{nome_pasta}{ext_raiz_str}"]
linhas_totais.extend(gerar_arvore_pastas(caminho_absoluto, ""))

# Salva o resultado no arquivo de texto
with open(caminho_completo, "w", encoding="utf-8") as f:
    f.write("\n".join(linhas_totais))

print(f"Estrutura de pastas salva com sucesso em: {caminho_completo}")