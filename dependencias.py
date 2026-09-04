import argparse
import json
import os
import subprocess
from datetime import datetime
import graphviz

pasta_downloads = os.path.join(os.path.expanduser("~"), "Downloads")

parser = argparse.ArgumentParser(
    description=(
        "Gera SVG limpo focado no alvo: Esquerda (importados), Centro (alvo),"
        " Direita (importadores)."
    )
)
parser.add_argument(
    "--caminho",
    "-c",
    default=pasta_downloads,
    help="Diretório de destino para salvar o SVG",
)
parser.add_argument(
    "--origem",
    "-o",
    default="src",
    help="Diretório raiz do código fonte",
)
parser.add_argument(
    "--alvo",
    "-a",
    required=True,
    help="Caminho do arquivo alvo obrigatório para este modo de foco",
)

args = parser.parse_args()
os.makedirs(args.caminho, exist_ok=True)

nome_base = os.path.splitext(os.path.basename(args.alvo))[0]
data_hoje = datetime.now().strftime("%d_%m_%Y")
nome_arquivo = f"DP_Foco_{nome_base}_{data_hoje}"
caminho_completo_saida = os.path.join(args.caminho, nome_arquivo)

print(f"Analisando dependências do projeto para encontrar: {args.alvo}...")

# Monta o comando como string para o Windows processar o npx corretamente
cmd = f"npx madge --json --extensions ts,tsx,js,jsx {args.origem}"
if os.path.exists("tsconfig.json"):
  cmd += " --ts-config tsconfig.json"
elif os.path.exists("jsconfig.json"):
  cmd += " --ts-config jsconfig.json"

# Executa o comando capturando a saída
resultado = subprocess.run(cmd, capture_output=True, text=True, shell=True)

if resultado.returncode != 0:
  print("Erro ao rodar a análise do Madge:")
  print(resultado.stderr)
  exit(1)

try:
  grafo_json = json.loads(resultado.stdout)
except Exception as e:
  print(f"Erro ao interpretar o retorno JSON do Madge: {e}")
  print(f"Saída recebida: {resultado.stdout[:200]}")
  exit(1)

# Busca flexível ignorando extensão e maiúsculas/minúsculas
chave_alvo = None
nome_alvo_sem_ext = os.path.splitext(os.path.basename(args.alvo))[0].lower()

for key in grafo_json.keys():
  key_nome = os.path.splitext(os.path.basename(key))[0].lower()
  if key_nome == nome_alvo_sem_ext:
    chave_alvo = key
    break

if not chave_alvo:
  print(f"Erro: O arquivo '{args.alvo}' não foi encontrado no mapeamento do Madge.")
  exit(1)
else:
  print(f"Chave mapeada com sucesso no Madge: {chave_alvo}")

# Coleta o que ele importa (Esquerda) e quem o importa (Direita)
importados = set()
if chave_alvo in grafo_json:
  importados = set(grafo_json[chave_alvo])

importadores = set()
for arquivo, dependencias in grafo_json.items():
  if chave_alvo in dependencias:
    importadores.add(arquivo)

print(f"-> Encontrados {len(importados)} imports e {len(importadores)} importadores.")

# Constrói o Grafo Direcional em Colunas Limpas
dot = graphviz.Digraph(comment="Dependencias Focadas", format="svg")
dot.attr(rankdir="LR", bgcolor="#1e1e1e", compound="true")

dot.attr(
    "node",
    shape="box",
    style="rounded,filled",
    fillcolor="#2d2d2d",
    fontcolor="#ffffff",
    fontname="Arial",
    margin="0.2",
)

dot.attr("edge", color="#666666", penwidth="1.5")

# Coluna da Esquerda: O que o arquivo alvo consome
with dot.subgraph(name="cluster_esquerda") as c:
  c.attr(rank="same")
  if not importados:
    c.node("vazio_esq", label="(Nenhum import)", style="invis")
  for imp in sorted(importados):
    c.node(imp, label=os.path.basename(imp), tooltip=imp)
    c.edge(imp, chave_alvo, color="#4da6ff")

# Coluna do Centro: O arquivo alvo em destaque laranja
with dot.subgraph(name="cluster_centro") as c:
  c.attr(rank="same")
  c.node(
      chave_alvo,
      label=f"★ {os.path.basename(chave_alvo)}",
      fillcolor="#ff8800",
      fontcolor="#000000",
      penwidth="2",
      tooltip=chave_alvo,
  )

# Coluna da Direita: Quem consome o arquivo alvo
with dot.subgraph(name="cluster_direita") as c:
  c.attr(rank="same")
  if not importadores:
    c.node("vazio_dir", label="(Ninguém importa)", style="invis")
  for imp_por in sorted(importadores):
    c.node(imp_por, label=os.path.basename(imp_por), tooltip=imp_por)
    c.edge(chave_alvo, imp_por, color="#00cc66")

# Renderiza o SVG final
caminho_final_gerado = dot.render(caminho_completo_saida, cleanup=True)
print(f"Gráfico focado gerado com sucesso em: {caminho_final_gerado}")