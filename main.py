from flask import Flask,render_template, url_for
from forms import FormLogin, FormCriarConta

app = Flask(__name__)

lista_usuarios =['Fernando', 'Laise', 'Davi', 'Allan']

app.config['SECRET_KEY'] = '9356fb9a7a879a9a5ecac7cdcdcaab1a'

@app.route("/")
def home():
    return render_template('home.html')


@app.route("/contatos")
def contatos():
    return render_template('contatos.html')


@app.route("/usuarios")
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route("/login")
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


if __name__ == '__main__':
    app.run(debug=True)
