# main.py (VERSÃO E2E)
# Este ficheiro agora contém a lógica para gerar testes passo a passo
# e depois montar o ficheiro final completo.

import ollama
from analisador_url import extrair_elementos_da_pagina
import os
import datetime
from prompts import PROMPT_GERADOR_DE_PASSO # Importamos o nosso novo prompt

def gerar_passo_de_teste(objetivo_geral: str, passos_anteriores: str, contexto_pagina: str, acao_desejada: str) -> str:
    """
    Gera o código para um único passo do teste E2E.
    """
    prompt_final = PROMPT_GERADOR_DE_PASSO.format(
        objetivo_geral=objetivo_geral,
        passos_anteriores=passos_anteriores,
        contexto_pagina=contexto_pagina,
        acao_desejada=acao_desejada
    )
    
    print("INFO: A enviar prompt de passo para a IA local...")
    
    try:
        response = ollama.chat(model='codellama:7b', messages=[{'role': 'user', 'content': prompt_final}])
        codigo_passo = response['message']['content'].replace("```python", "").replace("```", "").strip()
        return codigo_passo
    except Exception as e:
        print(f"ERRO: Falha ao comunicar com o Ollama: {e}")
        return f"# ERRO: Não foi possível gerar o código para esta ação: {e}"

def montar_script_final(passos_codigo: list) -> str:
    """
    Pega na lista de trechos de código e monta o ficheiro de teste completo.
    """
    # Indenta corretamente cada passo para caber dentro da função de teste
    codigo_passos_indentado = "\n".join([f"    {linha}" for passo in passos_codigo for linha in passo.split('\n')])

    # Usamos um template base para o ficheiro de teste
    template_final = f"""
import pytest
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# O ficheiro conftest.py irá fornecer a lógica para o 'request'
@pytest.fixture
def driver_setup(request):
    driver = webdriver.Chrome()
    yield driver
    # Teardown: executado após o teste
    if request.node.rep_call.failed:
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_name = f"ERRO_{{request.node.name}}_{{timestamp}}.png"
        driver.save_screenshot(screenshot_name)
    else:
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_name = f"SUCESSO_{{request.node.name}}_{{timestamp}}.png"
        driver.save_screenshot(screenshot_name)
    driver.quit()

def test_fluxo_e2e_gerado(driver_setup):
    driver = driver_setup
    wait = WebDriverWait(driver, 10)
    
{codigo_passos_indentado}

    # Se todos os passos foram executados, o teste passa
    assert True
"""
    return template_final.strip()

def salvar_script(codigo_final: str) -> str:
    """Salva o script final e retorna o caminho do ficheiro."""
    pasta_testes = "testes_gerados"
    os.makedirs(pasta_testes, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = os.path.join(pasta_testes, f"test_e2e_{timestamp}.py")
    
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(codigo_final)
    
    print(f"INFO: Script salvo em '{nome_arquivo}'")
    return nome_arquivo