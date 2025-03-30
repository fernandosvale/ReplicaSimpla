from comunidadecdl import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    eventos = database.relationship('Evento', backref='autor', lazy=True)

class Evento(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    organizador = database.Column(database.String, nullable=False)
    endereco = database.Column(database.String, nullable=False)
    data = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)


class Participacao(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    usuario_id = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    evento_id = database.Column(database.Integer, database.ForeignKey('evento.id'), nullable=False)
    data_inscricao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    nome_completo = database.Column(database.String, nullable=False) # Adicionado nome_completo e email
    email = database.Column(database.String, nullable=False)
    usuario = database.relationship('Usuario', backref='participacoes', lazy=True)
    evento = database.relationship('Evento', backref='participantes', lazy=True)



