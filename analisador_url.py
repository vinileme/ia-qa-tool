# analisador_url.py
# Este script é responsável por "olhar" para uma página web
# e descrever seus elementos interativos de forma que a IA entenda.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def extrair_elementos_da_pagina(url: str) -> str:
    """
    Acessa uma URL, extrai o HTML e retorna uma string simplificada
    com os elementos interativos para alimentar a IA.
    """
    print(f"INFO: Acessando e analisando a URL: {url}...")
    
    options = webdriver.ChromeOptions()
    # Roda o navegador em segundo plano, sem abrir uma janela visual.
    # É mais rápido e limpo para automações.
    options.add_argument('--headless')
    # Diminui a quantidade de mensagens de log do Selenium no terminal.
    options.add_argument('--log-level=3') 

    # Usamos try/finally para garantir que o navegador sempre será fechado,
    # mesmo que ocorra um erro durante a análise.
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        driver.get(url)
        html = driver.page_source
    finally:
        driver.quit()

    soup = BeautifulSoup(html, 'html.parser')
    elementos_interativos = []

    # Procuramos por tags que representam interações do usuário.
    for tag in soup.find_all(['input', 'button', 'a', 'select', 'textarea']):
        info = f"TAG: '{tag.name}'"
        
        # Coletamos atributos importantes que a IA pode usar para criar seletores.
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

# --- Bloco de Teste ---
# A mágica do `if __name__ == '__main__':` é que o código dentro dele
# só roda quando você executa ESTE arquivo diretamente. Se outro arquivo
# importar a função, este bloco não será executado.
if __name__ == '__main__':
    # Usamos um site famoso para praticar automação.
    url_de_teste = 'https://www.saucedemo.com/' 
    
    estrutura_da_pagina = extrair_elementos_da_pagina(url_de_teste)
    
    print("\n--- ESTRUTURA EXTRAÍDA PARA A IA ---")
    print(estrutura_da_pagina)