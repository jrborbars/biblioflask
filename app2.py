# Acesso ao SGBD
# Na disciplina INF8B, usamos o driver nativo do SQLITE3.
# Na disciplina de INF9, vamos utilizar o ORM sqlalchemy, que é independente do banco de dados utilizado.
# ORM quer dizer Object-Relational Mapper, Mapeador Objeto-Relacional.

"""
Bibliotecas instaladas
==============

flask
flask-sqlalchemy	# Acesso ao SGBD
flask-uploads		# Gerencia upload (imagens, arquivos)

flask-bootstrap		# Ativa o bootstrap 
flask-wtf 			# Formulários
flask-login		# Login

"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app  = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meudb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '5fbc1554-8b78-4080-98b4-5035b8469fee-042c5b51-5024-4bd5-af69-d2ab00debd6b'
# Gerar o secret-key com o UUID
db = SQLAlchemy(app) # inicializa o ORM

class Usuario(db.Model):
	__tablename__ = 'usuarios'
	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String(250))
	email = db.Column(db.String(250))
	password = db.Column(db.String(250))

	def __repr__(self):
		return '<Usuario: {} {}>'.format(self.nome,self.email)

	def __init__(self, nome,email,password):
		self.nome = nome
		self.email = email
		self.password = password

@app.route('/')
def index():
	return 'Opa. Esse é o index'

#app.run()


"""
(aulasflask) [ricardo@archarrow aula1]$ python
Python 3.7.2 (default, Jan 10 2019, 23:51:51) 
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from app2 import db
>>> from app2 import Usuario
>>> usu = Usuario(nome='Joao', email='joao@masca.com',password='123')
>>> usu
<Usuario: Joao>
>>> usu.email
'joao@masca.com'
>>> db.session.add(usu)
>>> db.session.commit()
"""
















