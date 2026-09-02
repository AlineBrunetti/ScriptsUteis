import argparse
import os
from datetime import datetime

# Pega dinamicamente a pasta Downloads do usuário logado atualmente
pasta_downloads = os.path.join(os.path.expanduser("~"), "Downloads")

# Configuração para receber o destino e a origem via linha de comando
parser = argparse.ArgumentParser(
    description="Gera a árvore de diretórios e salva em arquivo de texto."
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

# Pega o nome da pasta (se for '.', pega o nome da pasta aberta no momento da execução)
caminho_absoluto = os.path.abspath(args.origem)
nome_pasta = os.path.basename(caminho_absoluto)

# Tratativa caso seja a raiz do disco (ex: C:\) para evitar nome vazio
if not nome_pasta:
  nome_pasta = caminho_absoluto.replace(":", "").replace("\\", "_")

# Gera a data e o nome do arquivo .txt no formato desejado
data_hoje = datetime.now().strftime("%d_%m_%Y")
nome_arquivo = f"EC_{nome_pasta}_{data_hoje}.txt"
caminho_completo = os.path.join(args.caminho, nome_arquivo)

# Executa o comando tree do Windows enviando a saída para o arquivo
comando = f'tree "{args.origem}" /F /A > "{caminho_completo}"'
os.system(comando)

print(f"Estrutura salva com sucesso em: {caminho_completo}")