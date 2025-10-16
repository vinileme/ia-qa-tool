# analisador_url.py (VERSÃO 2.0 - Robusta)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
# Novas importações para a espera inteligente
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extrair_elementos_da_pagina(url: str) -> str:
    """
    Acessa uma URL, extrai o HTML e retorna uma string simplificada
    com os elementos interativos para alimentar a IA.
    """
    print(f"INFO: A aceder e analisar a URL: {url}...")
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--log-level=3') 

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        driver.get(url)
        # ADIÇÃO: Espera até 5 segundos para que a tag <body> da página esteja presente.
        # Isto garante que a página começou a ser renderizada antes de lermos o HTML.
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        html = driver.page_source
    except Exception as e:
        print(f"ERRO: Não foi possível carregar ou analisar a URL {url}. Detalhe: {e}")
        return f"ERRO: Não foi possível carregar a página. Verifique a URL e a sua conexão."
    finally:
        driver.quit()

    soup = BeautifulSoup(html, 'html.parser')
    elementos_interativos = []

    for tag in soup.find_all(['input', 'button', 'a', 'select', 'textarea']):
        info = f"TAG: '{tag.name}'"
        
        tag_id = tag.get('id')
        if tag_id:
            info += f", ID: '{tag_id}'"
        
        tag_name = tag.get('name')
        if tag_name:
            info += f", NAME: '{tag_name}'"
            
        tag_type = tag.get('type')
        if tag_type:
            info += f", TYPE: '{tag_type}'"

        tag_text = tag.text.strip()
        if tag_text:
            info += f", TEXTO: '{tag_text}'"
        
        elementos_interativos.append(info)
    
    print("INFO: Análise da página concluída.")
    return "\n".join(elementos_interativos)
