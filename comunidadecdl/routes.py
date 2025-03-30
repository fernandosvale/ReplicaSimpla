from flask import render_template, redirect, url_for, flash, request
from comunidadecdl import app, database, bcrypt
from comunidadecdl.forms import FormLogin, FormCriarConta, FormCriarEvento, FormsParticiparEvento
from comunidadecdl.models import Usuario, Evento, Participacao
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime


lista_usuarios =['Forró no sitio', 'Kangalha', 'G4', 'Síara Hall']

@app.route("/")
def home():
    return render_template('home.html')


@app.route("/contatos")
def contatos():
    return render_template('contatos.html')


@app.route("/eventos")
@login_required
def usuarios():
    return render_template('eventos.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

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

    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada com sucesso no e-mail:{form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout realizado com sucesso', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')

@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_evento():
    form_criarevento = FormCriarEvento()
    if form_criarevento.validate_on_submit():
        nome_evento = form_criarevento.nome_evento.data
        data = form_criarevento.data.data
        local = form_criarevento.local.data
        organizador = form_criarevento.organizador.data
        # Correção: Passando o ID do usuário logado para id_usuario
        evento = Evento(titulo=nome_evento, organizador=organizador, endereco=local, data=data, id_usuario=current_user.id)
        database.session.add(evento)
        database.session.commit()
        flash('Evento criado com sucesso!', 'success')
        return redirect(url_for('home'))  # Redirecione para a página apropriada
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
        participacao = Participacao.query.filter_by(usuario_id=current_user.id, evento_id=evento_id).first()
        if participacao:
            flash('Você já está participando deste evento!', 'warning')
            return redirect(url_for('home'))

        nova_participacao = Participacao(
            usuario_id=current_user.id,
            evento_id=evento_id,
            nome_completo=nome_completo,  # Usar nome_completo
            email=email
        )
        database.session.add(nova_participacao)
        database.session.commit()

        flash('Participação confirmada com sucesso!', 'success')
        return redirect(url_for('home'))

    return render_template('participarevento.html', form_participar_evento=form_participar_evento)

