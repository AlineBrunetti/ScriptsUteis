import argparse
import os
import subprocess
from datetime import datetime

pasta_downloads = os.path.join(os.path.expanduser("~"), "Downloads")

parser = argparse.ArgumentParser(
    description=(
        "Gera arquivo SVG de dependências usando o Madge com suporte a"
        " aliases."
    )
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
    help="Arquivo específico para focar (caminho absoluto ou relativo)",
)
parser.add_argument(
    "--extensoes",
    "-e",
    default="ts,tsx,js,jsx",
    help="Extensões suportadas separadas por vírgula",
)

args = parser.parse_args()

os.makedirs(args.caminho, exist_ok=True)

alvo_processado = args.alvo
if args.alvo:
  if os.path.isabs(args.alvo):
    alvo_processado = os.path.relpath(args.alvo, start=os.getcwd())
  nome_base = os.path.splitext(os.path.basename(args.alvo))[0]
else:
  caminho_absoluto = os.path.abspath(args.origem)
  nome_base = os.path.basename(caminho_absoluto) or "projeto"

data_hoje = datetime.now().strftime("%d_%m_%Y")
nome_arquivo = f"DP_{nome_base}_{data_hoje}.svg"
caminho_completo = os.path.join(args.caminho, nome_arquivo)

cmd = ["npx", "madge", f"--extensions={args.extensoes}"]

# Correção aplicada: parâmetro correto do CLI do Madge é --ts-config
if os.path.exists("tsconfig.json"):
  cmd.extend(["--ts-config", "tsconfig.json"])
elif os.path.exists("jsconfig.json"):
  cmd.extend(["--ts-config", "jsconfig.json"])

if alvo_processado:
  cmd.append(alvo_processado)

cmd.extend([args.origem, "--image", caminho_completo])

print(f"Gerando relatório para: {alvo_processado or args.origem}...")

resultado = subprocess.run(cmd, shell=True)

if resultado.returncode == 0:
  print(f"Salvo com sucesso em: {caminho_completo}")
else:
  print("Erro ao gerar o gráfico de dependências.")