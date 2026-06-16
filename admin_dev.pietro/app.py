"""
Aplicativo principal Flask integrado com SQLAlchemy e WTForms.
Define a configuração básica, modelos de banco de dados, formulários e rotas.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Inicialização e configuração do aplicativo Flask
app = Flask(__name__)


# A chave secreta é usada para proteger proteger sessões e formulários (CSRF)
app.config['SECRET_KEY'] = 'kfjad fkjasdlkfja;sldkfj39480293afKJ KJD:'
# Configuração do banco de dados SQLite local
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# Desabilita o rastreamento de modificações para otimizar desempenho
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Inicialização da extensão SQLAlchemy
db = SQLAlchemy(app)

import routes

