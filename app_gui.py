# app_gui.py (VERSÃO FINAL com Execução)

from flask import Flask, render_template_string, request, session
import main
import executor  # Importamos o nosso novo módulo executor

app = Flask(__name__)
# Chave secreta necessária para 'session' funcionar
app.secret_key = 'uma-chave-secreta-muito-segura'

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IA QA Tool</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background-color: #282c34; color: #abb2bf; margin: 40px; }
        .container { max-width: 800px; margin: auto; background-color: #21252b; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
        h1 { color: #61afef; border-bottom: 2px solid #3e4451; padding-bottom: 10px; }
        h2 { color: #e5c07b; }
        label { font-weight: bold; color: #98c379; }
        input[type=text] { width: 95%; padding: 10px; margin-top: 5px; margin-bottom: 20px; border-radius: 4px; border: 1px solid #3e4451; background-color: #282c34; color: #abb2bf; font-size: 14px; }
        input[type=submit], button { background-color: #61afef; color: #21252b; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; font-weight: bold; }
        input[type=submit]:hover, button:hover { background-color: #528baf; }
        button { background-color: #98c379; } /* Botão de executar em verde */
        button:hover { background-color: #80a96f; }
        pre { background-color: #21252b; border: 1px solid #3e4451; padding: 10px; border-radius: 4px; white-space: pre-wrap; word-wrap: break-word; color: #c8ccd4; }
        .results { margin-top: 30px; }
        .form-container { display: flex; align-items: center; gap: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Ferramenta de Geração de Testes com IA</h1>
        <div class="form-container">
            <form action="/generate" method="post" style="flex-grow: 1;">
                <label for="url">Cole a URL da página de login:</label><br>
                <input type="text" id="url" name="url" value="https://www.saucedemo.com/" required>
                <input type="submit" value="1. Gerar Automação">
            </form>
        </div>
        
        {% if log %}
        <div class="results">
            <h2>Progresso da Geração:</h2>
            <pre>{{ log }}</pre>
        </div>
        {% endif %}

        {% if filename %}
        <div class="results">
            <form action="/execute" method="post">
                <input type="hidden" name="filename" value="{{ filename }}">
                <button type="submit">2. Executar Teste ({{ filename.split('/')[-1] }})</button>
            </form>
        </div>
        {% endif %}
        
        {% if test_result %}
        <div class="results">
            <h2>Resultado da Execução do Teste:</h2>
            <pre>{{ test_result }}</pre>
        </div>
        {% endif %}
        
        {% if script %}
        <div class="results">
            <h2>Script Gerado:</h2>
            <pre>{{ script }}</pre>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    # Limpa a sessão ao carregar a página inicial
    session.clear()
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate():
    url = request.form.get('url')
    script, filename, log = main.gerar_script_final(url)
    # Guardamos os resultados na sessão para uso posterior
    session['script'] = script
    session['filename'] = filename
    session['log'] = log
    return render_template_string(HTML_TEMPLATE, script=script, filename=filename, log=log)

@app.route('/execute', methods=['POST'])
def execute():
    filename = request.form.get('filename')
    
    # Executamos o teste e obtemos o resultado
    test_result = executor.executar_pytest(filename)
    
    # Recuperamos os dados da sessão para re-exibir a página completa
    script = session.get('script')
    log = session.get('log')
    
    return render_template_string(HTML_TEMPLATE, script=script, filename=filename, log=log, test_result=test_result)


if __name__ == '__main__':
    print("Iniciando o servidor web local...")
    print("Abra o seu navegador e aceda a: http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=False)

