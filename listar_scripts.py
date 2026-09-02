import os
import re


def listar_comandos():
  pasta_atual = os.path.dirname(os.path.abspath(__file__))
  print("==================================================")
  print("         SEUS SCRIPTS E COMANDOS DISPONÍVEIS      ")
  print("==================================================\n")

  encontrou = False
  for arquivo in os.listdir(pasta_atual):
    if arquivo.endswith(".py") and arquivo not in [
        "listar_scripts.py",
        "instalar.py",
    ]:
      encontrou = True
      nome_comando = arquivo[:-3]  # Nome do comando baseado no arquivo .py
      caminho_py = os.path.join(pasta_atual, arquivo)

      # Tenta extrair a descrição do argparse de dentro do script Python
      descricao = "Sem descrição informada."
      try:
        with open(caminho_py, "r", encoding="utf-8") as f:
          conteudo = f.read()
          match = re.search(r'description\s*=\s*["\']([^"\']+)["\']', conteudo)
          if match:
            descricao = match.group(1)
      except Exception:
        pass

      print(f"🚀 Comando: {nome_comando}")
      print(f"   Função : {descricao}")
      print(f"   Atalho : digite '{nome_comando}' no terminal")
      print("-" * 50)

  if not encontrou:
    print("Nenhum script encontrado na pasta.")
  print()


if __name__ == "__main__":
  listar_comandos()