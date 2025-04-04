from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeLocalField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadecdl.models import Usuario, Evento
from flask_wtf.file import FileAllowed

class FormCriarConta(FlaskForm):
    username = StringField('Nome Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(4, 20)])
    confirmacao_senha = PasswordField('Confirmação de Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Digite outro e-mail')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(4, 20)])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    botao_submit_login = SubmitField('Fazer Login')


class FormCriarEvento(FlaskForm):
    nome_evento = StringField('Nome do Evento', validators=[DataRequired()])
    data = DateTimeLocalField('Data e Hora', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    local = TextAreaField('Local (Endereço)', validators=[DataRequired()])
    organizador = StringField('Organizador', validators=[DataRequired()])
    foto1 = FileField('Foto 1', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    foto2 = FileField('Foto 2', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    foto3 = FileField('Foto 3', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    botao_submit_criar_evento = SubmitField('Criar Evento')


class FormsParticiparEvento(FlaskForm):
    nome_completo = StringField('Nome Completo', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    evento = SelectField('Evento', coerce=int, validators=[DataRequired()])  # Alterado para SelectField
    botao_submit_participar = SubmitField('Participar do Evento')
