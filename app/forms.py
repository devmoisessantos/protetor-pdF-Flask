from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class CPFForm(FlaskForm):
    cpf = StringField('CPF', validators=[DataRequired()])
    position = SelectField('Posição', choices=[
        'Esquerda',
        'Centro',
        'Direita',
        'Cima',
        'Baixo',
        'Esquerda-Cima',
        'Esquerda-Baixo',
        'Centro-Cima',
        'Centro-Baixo',
        'Direita-Cima',
        'Direita-Baixo'
    ])
    color = StringField('Cor', validators=[DataRequired()], default='orange')
    submit = SubmitField('Enviar')
