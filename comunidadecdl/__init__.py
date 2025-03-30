from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

lista_usuarios =['Fernando', 'Laise', 'Davi', 'Allan']

app.config['SECRET_KEY'] = '9356fb9a7a879a9a5ecac7cdcdcaab1a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category ='alert-info'


from comunidadecdl import routes, database, app

# RODAR ESSE CÓDIGO APENAS PRA RESETAR O BANCO DE DADOS
# with app.app_context():
#     database.drop_all()
#     database.create_all()
