Ferramenta de Geração de Testes com IA Local

Este projeto é uma Prova de Conceito (POC) de uma ferramenta que utiliza um Modelo de Linguagem de Larga Escala (LLM) rodando localmente com Ollama para gerar scripts de automação de testes em Python, Selenium e Pytest.

Funcionalidades (Fase 1)

Analisa a estrutura de uma página web a partir de uma URL.

Envia a estrutura para um LLM local (codellama:7b).

A IA identifica os seletores (IDs) dos elementos de login.

O sistema preenche um template de teste robusto com os seletores identificados.

Gera um ficheiro .py pronto para ser executado com Pytest.

Tira screenshots automaticamente em caso de sucesso ou falha.

Como Configurar e Executar

Pré-requisitos:

Python 3.10+

Ollama instalado e a correr com o modelo codellama:7b.

Instalação:

# Clone o repositório
git clone https://github.com/vinileme/ia-qa-tool/

# Entre na pasta do projeto
cd ia_qa_tool

# Crie e ative um ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt


Execução:

# Para gerar um novo script de teste
python main.py

# Para executar o teste gerado
pytest testes_gerados/NOME_DO_FICHEIRO_GERADO.py
