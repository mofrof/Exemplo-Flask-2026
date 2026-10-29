import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session

import config
from utils.decorators import login_required
from models import usuario_model, jogo_model

app = Flask(__name__)

# Configurações carregadas diretamente sem classes e sem variáveis de ambiente
app.secret_key = config.SECRET_KEY
app.config['SESSION_TYPE'] = config.SESSION_TYPE
app.config['SESSION_PERMANENT'] = config.SESSION_PERMANENT
app.config['SESSION_USE_SIGNER'] = config.SESSION_USE_SIGNER
app.config['SESSION_FILE_DIR'] = config.SESSION_FILE_DIR
app.config['SESSION_COOKIE_HTTPONLY'] = config.SESSION_COOKIE_HTTPONLY
app.config['SESSION_COOKIE_SAMESITE'] = config.SESSION_COOKIE_SAMESITE
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = config.ALLOWED_EXTENSIONS
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

# Garantir criação de diretórios
os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Inicializar Flask-Session
Session(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# ==========================================
# ROTAS DE AUTENTICAÇÃO E NAVEGAÇÃO GERAL
# ==========================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'usuario_logado' in session and session['usuario_logado']:
        return redirect(url_for('index_jogos'))

    if request.method == 'POST':
        login_user = request.form.get('login', '').strip()
        senha = request.form.get('senha', '')

        if not login_user or not senha:
            flash('Por favor, informe seu login e senha.', 'danger')
            return render_template('login.html', login=login_user)

        usuario = usuario_model.buscar_usuario_por_login(login_user)

        if usuario and usuario_model.verificar_senha(usuario, senha):
            session.clear()
            session['usuario_logado'] = {
                'uuid': usuario['uuid'],
                'login': usuario['login'],
                'nome': usuario['nome']
            }
            flash(f'Bem-vindo(a) de volta, {usuario["nome"]}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index_jogos'))
        else:
            flash('Usuário ou senha incorretos. Tente novamente.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu do sistema com segurança.', 'info')
    return redirect(url_for('login'))

@app.route('/privacidade')
def privacidade():
    return render_template('privacidade.html')


# ==========================================
# ROTAS DE GERENCIAMENTO DE JOGOS (CRUD)
# ==========================================

@app.route('/')
@app.route('/jogos')
@login_required
def index_jogos():
    filtro_nome = request.args.get('nome', '').strip()
    filtro_ano = request.args.get('ano', '').strip()
    ordem_campo = request.args.get('ordem_campo', 'nome')
    ordem_direcao = request.args.get('ordem_direcao', 'ASC')
    pagina = request.args.get('pagina', 1, type=int)

    resultado = jogo_model.listar_jogos(
        filtro_nome=filtro_nome,
        filtro_ano=filtro_ano,
        ordem_campo=ordem_campo,
        ordem_direcao=ordem_direcao,
        pagina=pagina,
        itens_por_pagina=6
    )

    return render_template(
        'jogos/index.html',
        jogos=resultado['jogos'],
        total_itens=resultado['total_itens'],
        total_paginas=resultado['total_paginas'],
        pagina_atual=resultado['pagina_atual'],
        filtro_nome=filtro_nome,
        filtro_ano=filtro_ano,
        ordem_campo=ordem_campo,
        ordem_direcao=ordem_direcao
    )

@app.route('/jogos/detalhes/<jogo_uuid>')
@login_required
def detalhar_jogo(jogo_uuid):
    jogo = jogo_model.buscar_jogo_por_uuid(jogo_uuid)
    if not jogo:
        flash('Jogo não foi localizado no sistema.', 'danger')
        return redirect(url_for('index_jogos'))
    return render_template('jogos/detalhe.html', jogo=jogo)

@app.route('/jogos/novo', methods=['GET', 'POST'])
@login_required
def cadastrar_jogo():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        plataforma = request.form.get('plataforma', '').strip()
        ano_lancamento = request.form.get('anoLancamento', '').strip()
        file = request.files.get('imagem')

        if not nome or not plataforma or not ano_lancamento:
            flash('Preencha todos os campos obrigatórios!', 'warning')
            return render_template('jogos/novo.html', nome=nome, plataforma=plataforma, anoLancamento=ano_lancamento)

        if jogo_model.buscar_jogo_por_nome(nome):
            flash('Já existe um jogo cadastrado com este nome.', 'danger')
            return render_template('jogos/novo.html', nome=nome, plataforma=plataforma, anoLancamento=ano_lancamento)

        local_imagem = None
        if file and file.filename != '':
            if allowed_file(file.filename):
                filename = secure_filename(f"{nome.replace(' ', '_')}_{file.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                local_imagem = f"uploads/{filename}"
            else:
                flash('Formato de imagem inválido. Utilize JPG, PNG ou WEBP.', 'danger')
                return render_template('jogos/novo.html', nome=nome, plataforma=plataforma, anoLancamento=ano_lancamento)

        try:
            jogo_model.criar_jogo(nome, plataforma, ano_lancamento, local_imagem)
            flash(f'Jogo "{nome}" foi cadastrado com sucesso!', 'success')
            return redirect(url_for('index_jogos'))
        except Exception as e:
            flash(f'Ocorreu um erro ao cadastrar o jogo: {str(e)}', 'danger')

    return render_template('jogos/novo.html')

@app.route('/jogos/editar/<jogo_uuid>', methods=['GET', 'POST'])
@login_required
def editar_jogo(jogo_uuid):
    jogo = jogo_model.buscar_jogo_por_uuid(jogo_uuid)
    if not jogo:
        flash('Jogo não encontrado para alteração.', 'danger')
        return redirect(url_for('index_jogos'))

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        plataforma = request.form.get('plataforma', '').strip()
        ano_lancamento = request.form.get('anoLancamento', '').strip()
        file = request.files.get('imagem')

        if not nome or not plataforma or not ano_lancamento:
            flash('Preencha todos os campos obrigatórios!', 'warning')
            return render_template('jogos/editar.html', jogo=jogo)

        jogo_existente = jogo_model.buscar_jogo_por_nome(nome)
        if jogo_existente and jogo_existente['uuid'] != jogo_uuid:
            flash('Já existe outro jogo registrado com este mesmo nome.', 'danger')
            return render_template('jogos/editar.html', jogo=jogo)

        local_imagem = None
        if file and file.filename != '':
            if allowed_file(file.filename):
                filename = secure_filename(f"{nome.replace(' ', '_')}_{file.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                local_imagem = f"uploads/{filename}"
            else:
                flash('Formato de imagem inválido.', 'danger')
                return render_template('jogos/editar.html', jogo=jogo)

        try:
            jogo_model.atualizar_jogo(jogo_uuid, nome, plataforma, ano_lancamento, local_imagem)
            flash(f'Jogo "{nome}" foi alterado com sucesso!', 'success')
            return redirect(url_for('index_jogos'))
        except Exception as e:
            flash(f'Erro ao atualizar o jogo: {str(e)}', 'danger')

    return render_template('jogos/editar.html', jogo=jogo)

@app.route('/jogos/remover/<jogo_uuid>', methods=['POST'])
@login_required
def remover_jogo(jogo_uuid):
    jogo = jogo_model.buscar_jogo_por_uuid(jogo_uuid)
    if not jogo:
        flash('Jogo não encontrado para exclusão.', 'danger')
        return redirect(url_for('index_jogos'))

    try:
        jogo_model.deletar_jogo(jogo_uuid)
        flash(f'Jogo "{jogo["nome"]}" foi removido com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao excluir o jogo: {str(e)}', 'danger')

    return redirect(url_for('index_jogos'))

# ==========================================
# TRATAMENTO DE ERRO 404
# ==========================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
