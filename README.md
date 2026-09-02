# Guia de Configuração e Manutenção da Pasta de Scripts

## 1. Instalação Inicial (Primeiro Uso em um Novo PC)

Ao baixar ou sincronizar a pasta de scripts pela primeira vez em um computador novo (via Google Drive ou arquivo `.zip`), siga estes passos:

1. Posicione a pasta em um local definitivo no computador (ex: `C:\ScriptsUteis`).
2. Entre na pasta e execute o arquivo **`instalar.bat`** (clique duplo).
3. Aguarde a mensagem de conclusão e **feche/reabra** o seu terminal (CMD ou PowerShell).

A partir desse momento, todos os scripts da pasta estarão disponíveis globalmente em qualquer diretório do sistema.

---

## 2. Como Consultar os Comandos Disponíveis

Para verificar rapidamente quais scripts estão instalados na sua pasta e o que cada um faz diretamente pelo terminal, execute de qualquer diretório:

```cmd
listar_scripts

```

O utilitário lê de forma dinâmica as descrições embutidas no código de cada automação.

---

## 3. Como Adicionar Novos Scripts

Para expandir sua caixa de ferramentas mantendo a compatibilidade com o sistema, adicione sempre um par de arquivos para cada nova automação:

1. **Crie o script Python (`.py`):** Salve o código diretamente na pasta principal (ex: `limpar_cache.py`), certificando-se de preencher a `description` no `argparse` para que o comando `listar_scripts` capture sua função.
2. **Crie o atalho de lote (`.bat`):** Crie um arquivo com o **mesmo nome** do script (ex: `limpar_cache.bat`) contendo a seguinte estrutura:

```cmd
@echo off
python "%~dp0limpar_cache.py" %*

```

---

## 4. Mantendo a Saúde do Ambiente (Atualização de Atalhos)

Como o CMD reconhece automaticamente qualquer `.bat` adicionado à pasta através do `PATH`, novos scripts funcionam nele de imediato. Para registrar novos comandos no **PowerShell**:

* Execute o arquivo **`instalar.bat`** novamente sempre que criar novos scripts.
* **Funcionamento seguro:** O instalador faz uma varredura limpa, apagando entradas antigas e reescrevendo apenas o bloco de atalhos no seu perfil do PowerShell. Isso evita duplicatas ou acúmulo de lixo.
* Feche e abra o PowerShell novamente para utilizar a nova ferramenta.

---

## 5. Regras de Ouro para Portabilidade

* **Evite mover a pasta após instalar:** Se precisar trocar a pasta de lugar no disco, rode o `instalar.bat` de novo para atualizar os ponteiros do sistema.
* **Padronize os destinos:** Utilize sempre caminhos dinâmicos nos seus scripts Python (como a pasta `Downloads` do usuário atual) para que funcionem independentemente de quem esteja logado na máquina.
