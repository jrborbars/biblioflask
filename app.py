# Acesso ao SGBD
# Na disciplina INF8B, usamos o driver nativo do SQLITE3.
# Na disciplina de INF9, vamos utilizar o ORM sqlalchemy, que é independente do banco de dados utilizado.
# ORM quer dizer Object-Relational Mapper, Mapeador Objeto-Relacional.

"""
Bibliotecas instaladas
==============

flask
flask-sqlalchemy    # Acesso ao SGBD
flask-uploads       # Gerencia upload (imagens, arquivos)

flask-bootstrap     # Ativa o bootstrap 
flask-wtf           # Formulários
flask-login     # Login

"""

from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap

app  = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meudb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '5fbc1554-8b78-4080-98b4-5035b8469fee-042c5b51-5024-4bd5-af69-d2ab00debd6b'
# Gerar o secret-key com o UUID
db = SQLAlchemy(app) # inicializa o ORM
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(250))
    email = db.Column(db.String(250))
    password = db.Column(db.String(250))
    telefone = db.Column(db.String(50))
    cpf = db.Column(db.String(20))

    def __repr__(self):
        return '<Usuario: {}>'.format(self.nome)

    def __init__(self, nome,email,password,telefone, cpf):
        self.nome = nome
        self.email = email
        self.password = password
        self.telefone = telefone
        self.cpf = cpf

class InsereUsuarioForm(FlaskForm):
    nome    = StringField('Nome',validators=[InputRequired(),Length(min=3)])
    email   = StringField('Email',validators=[InputRequired(),Email(message='Insira um email válido.')])
    password= PasswordField('Senha',validators=[InputRequired(),Length(min=6)])
    telefone= StringField('Telefone',validators=[InputRequired(),Length(min=6)])
    cpf     = StringField('CPF',validators=[InputRequired(),Length(min=11,max=11)])
    enviar  = SubmitField('Enviar')

@app.route('/')
def index():
    return render_template('index.tpl')


@app.route('/usuarios')
def lista_usuarios():
    dados = Usuario.query.all()
    return render_template('usuarios.tpl', dadostpl = dados)    

@app.route('/usuarioadd',methods=['GET'])
def add_usuario_get():
    form = InsereUsuarioForm()
    return render_template('add_usuario.tpl', formtpl = form)


@app.route('/usuarioadd',methods=['POST'])
def add_usuario_post():
    form = InsereUsuarioForm(request.form)
    if form.validate_on_submit():
        novo_usuario = Usuario( nome = form.nome.data,
                                email = form.email.data,
                                password = form.password.data,
                                telefone = form.telefone.data,
                                cpf = form.cpf.data)
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Usuário inserido com sucesso.','success')
    else :
        flash('Não inserido. Problemas nos dados.'+str(form.errors),'danger')
    return redirect('/usuarios')

@app.route('/usuarioedit/<_id>',methods=['GET'])
def edit_usuario_get(_id):
    u = Usuario.query.filter_by(id=_id).first()
    form = InsereUsuarioForm(obj=u)
    return render_template('edit_usuario.tpl', formtpl = form)


@app.route('/usuarioedit/<_id>',methods=['POST'])
def edit_usuario_post(_id):
    form = InsereUsuarioForm(request.form)
    u = Usuario.query.filter_by(id=_id).first()
    if form.validate_on_submit():
        form.populate_obj(u)
        db.session.add(u)
        db.session.commit()
        flash('Usuário inserido com sucesso.','success')
    else :
        flash('Não inserido. Problemas nos dados.'+str(form.errors),'danger')
    return redirect('/usuarios')
    
if __name__ == "__main__":
    app.run()


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
















