from flask import render_template, redirect, url_for, flash, request, abort
from comunidadecdl import app, database, bcrypt
from comunidadecdl.forms import FormLogin, FormCriarConta, FormCriarEvento, FormsParticiparEvento
from comunidadecdl.models import Usuario, Evento, Participacao
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
import os
import secrets


lista_usuarios = ['Forró no sitio', 'Kangalha', 'G4', 'Síara Hall']


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/contatos")
def contatos():
    return render_template('contatos.html')


@app.route("/eventos")
@login_required
def eventos():  # Alterado o nome da função para 'eventos'
    eventos = Evento.query.all()  # Busca os eventos do banco de dados
    return render_template('eventos.html', eventos=eventos)  # Passa os eventos para o template


@app.route("/login", methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login realizado com sucesso no e-mail:{form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no login! E-mail ou senha incorretos', 'alert-danger')
    return render_template('login.html', form_login=form_login)


@app.route("/criar_conta", methods=['GET', 'POST'])
def criar_conta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data,
                        email=form_criarconta.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash(
            f'Conta criada com sucesso no e-mail:{form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criar_conta.html', form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout realizado com sucesso', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    # Obtém o usuário logado
    usuario = current_user

    # Busca a quantidade de eventos criados por este usuário
    eventos_criados = Evento.query.filter_by(id_usuario=usuario.id).count()

    # Busca a quantidade de eventos em que este usuário está inscrito
    eventos_inscritos = Participacao.query.filter_by(usuario_id=usuario.id).count()

    # Renderiza o template HTML, passando os valores
    return render_template('perfil.html',
                           current_user=usuario,  # Garanta que current_user esteja disponível
                           eventos_criados=eventos_criados,
                           eventos_inscritos=eventos_inscritos)


def salvar_foto(foto):
    if foto:
        formato = foto.filename.split('.')[-1]
        nome_seguro = secrets.token_hex(16) + '.' + formato
        caminho_arquivo = os.path.join(
            app.root_path, 'static/foto_eventos', nome_seguro)
        foto.save(caminho_arquivo)
        return nome_seguro
    return None


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_evento():
    form_criarevento = FormCriarEvento()
    if form_criarevento.validate_on_submit():
        nome_evento = form_criarevento.nome_evento.data
        data_evento = form_criarevento.data.data
        local_evento = form_criarevento.local.data
        organizador_evento = form_criarevento.organizador.data

        foto1_nome = salvar_foto(form_criarevento.foto1.data)
        foto2_nome = salvar_foto(form_criarevento.foto2.data)
        foto3_nome = salvar_foto(form_criarevento.foto3.data)
        evento = Evento(
            titulo=nome_evento,
            organizador=organizador_evento,
            endereco=local_evento,
            data=data_evento,
            id_usuario=current_user.id,
            foto1=foto1_nome,
            foto2=foto2_nome,
            foto3=foto3_nome
        )
        database.session.add(evento)
        database.session.commit()
        flash('Evento criado com sucesso!', 'success')
        return redirect(url_for('home'))
    return render_template('criarevento.html', form_criarevento=form_criarevento)


@app.route('/post/particpar', methods=['GET', 'POST'])
@login_required
def participar_evento():
    form_participar_evento = FormsParticiparEvento()
    eventos = Evento.query.all()
    form_participar_evento.evento.choices = [(e.id, e.titulo) for e in eventos]

    if form_participar_evento.validate_on_submit():
        nome_completo = form_participar_evento.nome_completo.data
        email = form_participar_evento.email.data
        evento_id = form_participar_evento.evento.data

        # Verificar se o evento existe
        evento = Evento.query.get(evento_id)
        if not evento:
            flash('Evento não encontrado!', 'danger')
            return redirect(url_for('home'))

        # Verificar se o usuário já está participando do evento.
        participacao = Participacao.query.filter_by(
            usuario_id=current_user.id, evento_id=evento_id).first()
        if participacao:
            flash('Você já está participando deste evento!', 'warning')
            return redirect(url_for('home'))

        nova_participacao = Participacao(
            usuario_id=current_user.id,
            evento_id=evento_id,
            nome_completo=nome_completo,
            email=email
        )
        database.session.add(nova_participacao)
        database.session.commit()

        flash('Participação confirmada com sucesso!', 'success')
        return redirect(url_for('home'))

    return render_template('participarevento.html', form_participar_evento=form_participar_evento)


@app.route('/evento/<int:evento_id>/participantes')
@login_required
def lista_participantes(evento_id):
    evento = Evento.query.get_or_404(
        evento_id)  # Obtém o evento ou retorna 404 se não encontrado
    # Obtém os participantes do evento
    participantes = Participacao.query.filter_by(evento_id=evento.id).all()
    return render_template('lista_participantes.html', evento=evento, participantes=participantes)


@app.route('/evento/<int:evento_id>/certificados/<int:participante_id>')
@login_required
def certificados(evento_id, participante_id):
    evento = Evento.query.get_or_404(evento_id)
    # Garante que apenas o criador do evento pode acessar esta página
    if evento.id_usuario != current_user.id:
        abort(403)
    participante = Participacao.query.get_or_404(participante_id)
    return render_template('certificados.html', evento=evento, participante=participante)
