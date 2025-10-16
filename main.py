# main.py (VERSÃO FINAL - Baseado em Template)

import ollama
from analisador_url import extrair_elementos_da_pagina
import os
import datetime

PROMPT_FINAL = '''
Sua tarefa é identificar os seletores ID para os elementos de uma página de login.
Baseado na estrutura de elementos fornecida, retorne APENAS os valores dos atributos ID para os seguintes campos:
1.  Campo de input do nome de utilizador.
2.  Campo de input da palavra-passe.
3.  Botão de submissão do login.

Responda no seguinte formato exato, sem texto adicional:
USER_ID: valor_do_id_aqui
PASSWORD_ID: valor_do_id_aqui
BUTTON_ID: valor_do_id_aqui
'''

def gerar_script_final(url: str):
    """
    Função principal que orquestra todo o processo.
    """
    print("INFO: A analisar a página para extrair a estrutura...")
    estrutura_pagina = extrair_elementos_da_pagina(url)
    
    prompt_para_ia = (
        f"Estrutura da Página:\n---\n{estrutura_pagina}\n---\n{PROMPT_FINAL}"
    )
    
    print("INFO: A enviar a estrutura para a IA para identificar os seletores...")
    try:
        response = ollama.chat(model='codellama:7b', messages=[{'role': 'user', 'content': prompt_para_ia}])
        resposta_ia = response['message']['content']
        
        print(f"INFO: Resposta da IA recebida:\n{resposta_ia}")
        
        # Extrair os IDs da resposta da IA
        ids = {}
        for linha in resposta_ia.split('\n'):
            if ':' in linha:
                chave, valor = linha.split(':', 1)
                ids[chave.strip()] = valor.strip()

        # Ler o nosso template de teste robusto
        with open("template_teste.py", "r", encoding="utf-8") as f:
            conteudo_template = f.read()
            
        # Substituir os placeholders pelos valores reais
        script_final = conteudo_template.replace("{URL_LOGIN}", url)
        script_final = script_final.replace("{USER_INPUT_ID}", ids.get("USER_ID", "user-name"))
        script_final = script_final.replace("{PASSWORD_INPUT_ID}", ids.get("PASSWORD_ID", "password"))
        script_final = script_final.replace("{LOGIN_BUTTON_ID}", ids.get("BUTTON_ID", "login-button"))
        script_final = script_final.replace("{SUCCESS_URL_CONTAINS}", "inventory.html")
        
        return script_final

    except Exception as e:
        print(f"ERRO: Falha ao gerar o script: {e}")
        return None

if __name__ == '__main__':
    url_alvo = 'https://www.saucedemo.com/'
    script_final_gerado = gerar_script_final(url_alvo)
    
    if script_final_gerado:
        pasta_testes = "testes_gerados"
        os.makedirs(pasta_testes, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = os.path.join(pasta_testes, f"test_login_{timestamp}.py")
        
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(script_final_gerado)
        
        print("\n" + "="*50)
        print(f"✅ SUCESSO! Script de automação baseado em template salvo em '{nome_arquivo}'")
        print("="*50)
        print("\nPara executar o novo teste, use o comando:")
        print(f"pytest {nome_arquivo}")
    else:
        print("\n❌ FALHA: Não foi possível gerar o script de teste.")

