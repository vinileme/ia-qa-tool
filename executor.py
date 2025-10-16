# executor.py
# Módulo responsável por executar os testes Pytest a partir do nosso código.

import subprocess
import sys
import os

def executar_pytest(caminho_arquivo: str) -> str:
    """
    Executa um ficheiro de teste específico usando Pytest e captura a sua saída.

    Retorna uma string com o resultado da execução (stdout e stderr).
    """
    if not os.path.exists(caminho_arquivo):
        return f"ERRO: O ficheiro de teste '{caminho_arquivo}' não foi encontrado."

    # Usamos sys.executable para garantir que estamos a usar o mesmo interpretador Python
    # que está a executar a nossa aplicação Flask.
    comando = [sys.executable, "-m", "pytest", caminho_arquivo]
    
    print(f"INFO: A executar o comando: {' '.join(comando)}")
    
    try:
        # Executa o comando no terminal
        resultado = subprocess.run(
            comando,
            capture_output=True, # Captura a saída
            text=True,           # Converte a saída para texto (string)
            check=False          # Não levanta uma exceção se o Pytest falhar (exit code != 0)
        )
        
        # Combinamos a saída padrão e a saída de erro para um log completo
        saida_completa = resultado.stdout + resultado.stderr
        print("INFO: Execução do Pytest concluída.")
        return saida_completa
        
    except FileNotFoundError:
        return "ERRO: O comando 'pytest' não foi encontrado. Verifique se o Pytest está instalado no ambiente virtual."
    except Exception as e:
        return f"ERRO: Ocorreu uma falha inesperada durante a execução do teste: {e}"
