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


from comunidadecdl import routes
