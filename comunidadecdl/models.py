from comunidadecdl import database
from datetime import datetime
from flask_login import UserMixin
from comunidadecdl import login_manager

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    eventos = database.relationship('Evento', backref='autor', lazy=True)
    participacoes = database.relationship('Participacao', backref='participacoes_usuario', lazy=True) # Alterado o backref de 'usuario' para 'participacoes_usuario'


class Evento(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    organizador = database.Column(database.String, nullable=False)
    endereco = database.Column(database.String, nullable=False)
    data = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    foto1 = database.Column(database.String, nullable=True)
    foto2 = database.Column(database.String, nullable=True)
    foto3 = database.Column(database.String, nullable=True)
    participantes = database.relationship('Participacao', backref='participantes_evento', lazy=True)


class Participacao(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    usuario_id = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    evento_id = database.Column(database.Integer, database.ForeignKey('evento.id'), nullable=False)
    data_inscricao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    nome_completo = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False)
    usuario = database.relationship('Usuario', backref='usuario', lazy=True) #mantivemos
    evento = database.relationship('Evento', backref='evento', lazy=True)
