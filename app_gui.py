# app_gui.py (VERSÃO 3.1 - Melhorias de Layout)

from flask import Flask, render_template_string, request, session, redirect, url_for
import main
import executor
from analisador_url import extrair_elementos_da_pagina

app = Flask(__name__)
app.secret_key = 'uma-chave-secreta-muito-segura-para-e2e-v3'

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IA QA Tool - Construtor E2E com Pré-visualização</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background-color: #282c34; color: #abb2bf; margin: 0; padding: 20px; display: flex; gap: 20px; height: 95vh; }
        .column { display: flex; flex-direction: column; }
        .column.left { flex: 1; }
        .column.middle { flex: 2; }
        .column.right { flex: 1; background-color: #21252b; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
        h1, h2 { color: #61afef; border-bottom: 2px solid #3e4451; padding-bottom: 10px; margin-top: 0; }
        h3 { color: #e5c07b; margin-top: 20px; }
        label { font-weight: bold; color: #98c379; }
        input[type=text], textarea { width: 95%; max-width: 95%; padding: 10px; margin-top: 5px; margin-bottom: 20px; border-radius: 4px; border: 1px solid #3e4451; background-color: #282c34; color: #abb2bf; font-size: 14px; }
        button { background-color: #61afef; color: #21252b; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; font-weight: bold; width: 100%; margin-top: 10px; }
        button.secondary { background-color: #e06c75; }
        pre { background-color: #21252b; border: 1px solid #3e4451; padding: 10px; border-radius: 4px; white-space: pre-wrap; word-wrap: break-word; color: #c8ccd4; flex-grow: 1; overflow-y: auto; font-size: 13px; }
        hr { border-color: #3e4451; }
        .step-card { background-color: #2c313a; border-left: 4px solid #61afef; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
        .step-card h3 { margin-top: 0; color: #98c379; font-size: 1em; }
        .step-card pre { background-color: #282c34; margin-top: 10px; font-size: 0.8em; }
        .scroll-container { flex-grow: 1; overflow-y: auto; padding-right: 10px; display: flex; flex-direction: column; }
        iframe { width: 100%; height: 100%; border: 1px solid #3e4451; border-radius: 8px; }
        
        /* --- AQUI ESTÁ A CORREÇÃO --- */
        .sidebar-section pre {
            min-height: 100px; /* Garante uma altura mínima para as caixas de texto */
            max-height: 250px; /* Limita a altura máxima para não ocupar o ecrã todo */
            overflow-y: auto;  /* Adiciona uma barra de scroll se o conteúdo for grande */
            flex-grow: 0;      /* Impede que cresça para preencher o espaço */
        }
    </style>
</head>
<body>
    <!-- Coluna Esquerda: Fluxo do Teste -->
    <div class="column left">
        <h1>Fluxo do Teste</h1>
        <div class="scroll-container">
            {% for passo in session.get('passos_executados', []) %}
                <div class="step-card">
                    <h3>Passo {{ loop.index }}: {{ passo.action }}</h3>
                    <pre>{{ passo.code }}</pre>
                </div>
            {% endfor %}
            {% if not session.get('passos_executados') %}
                <p>Comece um novo teste no painel de controlo.</p>
            {% endif %}
        </div>
    </div>

    <!-- Coluna Central: Pré-visualização ao Vivo -->
    <div class="column middle">
        <h2>Pré-visualização Ao Vivo</h2>
        {% if session.get('url_atual') %}
            <iframe src="{{ session.get('url_atual') }}"></iframe>
        {% else %}
            <p>A pré-visualização aparecerá aqui quando iniciar um teste.</p>
        {% endif %}
    </div>

    <!-- Coluna Direita: Painel de Controlo -->
    <div class="column right scroll-container">
        {% if not session.get('objetivo_geral') %}
        <h2>Começar Novo Teste</h2>
        <form action="/iniciar" method="post">
            <!-- formulário inicial -->
            <label for="url_inicial">URL Inicial:</label><br>
            <input type="text" id="url_inicial" name="url_inicial" value="https://www.saucedemo.com/" required><br>
            <label for="objetivo_geral">Objetivo Geral:</label><br>
            <textarea id="objetivo_geral" name="objetivo_geral" rows="3" required>Fazer login, adicionar um item ao carrinho e validar o checkout.</textarea><br>
            <button type="submit">1. Iniciar</button>
        </form>
        {% else %}
        <h2>Painel de Controlo</h2>
        <p><strong>URL para Análise:</strong><br>{{ session.get('url_atual', 'Nenhuma') }}</p>
        <hr>
        <h3>Análise da Página</h3>
        <!-- Adicionamos a classe 'sidebar-section' ao <pre> -->
        <pre class="sidebar-section">{{ contexto_pagina }}</pre>
        <hr>
        <h3>Próximo Passo</h3>
        <form action="/adicionar_passo" method="post">
            <label for="acao_desejada">Descreva a próxima ação:</label><br>
            <textarea id="acao_desejada" name="acao_desejada" rows="3" required></textarea><br>
            <label for="proxima_url">URL Esperada Após a Ação (Opcional):</label><br>
            <input type="text" id="proxima_url" name="proxima_url"><br>
            <button type="submit">2. Adicionar Passo</button>
        </form>
        <hr>
        <h3>Finalizar</h3>
        <form action="/finalizar" method="post">
            <button type="submit">3. Salvar e Executar</button>
        </form>
        <form action="/" method="get">
            <button type="submit" class="secondary">Recomeçar</button>
        </form>
        
        {% if session.get('ultimo_resultado') %}
        <hr>
        <h3>Resultado da Execução</h3>
        <!-- Adicionamos a classe 'sidebar-section' ao <pre> -->
        <pre class="sidebar-section">{{ session.get('ultimo_resultado') }}</pre>
        {% endif %}
        {% endif %}
    </div>
</body>
</html>
'''

# O backend em Python permanece o mesmo da versão anterior, pois a lógica não muda, apenas a apresentação.
@app.route('/')
def index():
    session.clear()
    return render_template_string(HTML_TEMPLATE)

@app.route('/iniciar', methods=['POST'])
def iniciar_teste():
    session['url_inicial'] = request.form['url_inicial']
    session['url_atual'] = request.form['url_inicial']
    session['objetivo_geral'] = request.form['objetivo_geral']
    session['passos_executados'] = [{
        'action': 'Navegar para a URL inicial',
        'code': f'driver.get("{session["url_inicial"]}")'
    }]
    session['ultimo_resultado'] = None
    return redirect(url_for('construir'))

@app.route('/construir')
def construir():
    contexto_pagina = "Analisando..."
    if session.get('url_atual'):
        contexto_pagina = extrair_elementos_da_pagina(session['url_atual'])
    return render_template_string(HTML_TEMPLATE, contexto_pagina=contexto_pagina)

@app.route('/adicionar_passo', methods=['POST'])
def adicionar_passo():
    contexto_pagina = extrair_elementos_da_pagina(session['url_atual'])
    passos_anteriores = "\n".join([passo['code'] for passo in session.get('passos_executados', [])])
    acao_desejada = request.form.get('acao_desejada', '')

    novo_passo_codigo = main.gerar_passo_de_teste(
        session.get('objetivo_geral', ''),
        passos_anteriores,
        contexto_pagina,
        acao_desejada
    )
    
    passos_atuais = session.get('passos_executados', [])
    passos_atuais.append({
        'action': acao_desejada,
        'code': novo_passo_codigo
    })
    session['passos_executados'] = passos_atuais
    
    proxima_url = request.form.get('proxima_url')
    if proxima_url:
        session['url_atual'] = proxima_url
        
    return redirect(url_for('construir'))

@app.route('/finalizar', methods=['POST'])
def finalizar_teste():
    passos_codigo = [passo['code'] for passo in session.get('passos_executados', [])]
    
    codigo_final = main.montar_script_final(passos_codigo)
    caminho_ficheiro = main.salvar_script(codigo_final)
    resultado = executor.executar_pytest(caminho_ficheiro)
    session['ultimo_resultado'] = resultado
    return redirect(url_for('construir'))


if __name__ == '__main__':
    print("Iniciando o servidor web local...")
    print("Abra o seu navegador e aceda a: http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)