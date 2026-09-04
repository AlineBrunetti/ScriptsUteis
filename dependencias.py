import argparse
import os
import subprocess
from datetime import datetime

# Pega dinamicamente a pasta Downloads do usuário logado atualmente
pasta_downloads = os.path.join(os.path.expanduser("~"), "Downloads")

parser = argparse.ArgumentParser(
    description="Gera arquivo SVG de dependências usando o Madge."
)
parser.add_argument(
    "--caminho",
    "-c",
    default=pasta_downloads,
    help="Diretório de destino para salvar o SVG (padrão: Downloads)",
)
parser.add_argument(
    "--origem",
    "-o",
    default="src",
    help="Diretório raiz do código fonte (padrão: src)",
)
parser.add_argument(
    "--alvo",
    "-a",
    default=None,
    help="Arquivo específico ou componente para focar as relações (opcional)",
)
parser.add_argument(
    "--extensoes",
    "-e",
    default="ts,tsx,js,jsx",
    help="Extensões suportadas separadas por vírgula (padrão: ts,tsx,js,jsx)",
)

args = parser.parse_args()

# Garante que a pasta de destino existe
os.makedirs(args.caminho, exist_ok=True)

# Define o nome base para o arquivo com base no alvo ou na pasta de origem
if args.alvo:
    nome_base = os.path.splitext(os.path.basename(args.alvo))[0]
else:
    caminho_absoluto = os.path.abspath(args.origem)
    nome_base = os.path.basename(caminho_absoluto) or "projeto"

# Formato do nome: DP_coisa_analisada_dia_mes_ano.svg
data_hoje = datetime.now().strftime("%d_%m_%Y")
nome_arquivo = f"DP_{nome_base}_{data_hoje}.svg"
caminho_completo = os.path.join(args.caminho, nome_arquivo)

# Monta o comando base do Madge
cmd = ["npx", "madge", f"--extensions={args.extensoes}"]

# Se um arquivo/alvo específico foi passado, o Madge foca nele e nos seus dependentes/dependências
if args.alvo:
    cmd.append(args.alvo)

# Adiciona a pasta de origem e o arquivo de saída gerado
cmd.extend([args.origem, "--image", caminho_completo])

print(f"Gerando relatório de dependências para: {args.alvo or args.origem}...")

# Executa o comando via subprocess
resultado = subprocess.run(cmd, shell=True)

if resultado.returncode == 0:
    print(f"Dependências salvas com sucesso em: {caminho_completo}")
else:
    print("Erro ao gerar o gráfico de dependências.")