from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, update, func
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Email, Length,  ValidationError, EqualTo
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from datetime import timedelta, date, time, datetime

app  = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meudb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = '5fbc1554-8b78-4080-98b4-5035b8469fee-042c5b51-5024-4bd5-af69-d2ab00debd6b'
# Gerar o secret-key com o UUID
db = SQLAlchemy(app) # inicializa o ORM
migrate = Migrate(app, db) # inicializa as migrations
bootstrap = Bootstrap(app) # inicializa o Bootstrap

login_manager = LoginManager(app)
login_manager.login_view = 'login_get'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.filter_by(id=user_id).first()

PERIODO_EMPRESTIMO =  timedelta(days=7)

emprestimo = db.Table('emprestimos',
            db.Column('id',db.Integer, primary_key=True),
            db.Column('usuario_id',db.Integer, db.ForeignKey('usuarios.id')),
            db.Column('livro_id',db.Integer, db.ForeignKey('livros.id')),
            db.Column('data_emprestimo',db.DateTime(),default=datetime.now),
            db.Column('data_provavel_devolucao',db.DateTime(),default=datetime.now()+PERIODO_EMPRESTIMO),
            db.Column('data_efetiva_devolucao',db.DateTime())
            )

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(250))
    email = db.Column(db.String(250))
    password_hash = db.Column(db.String(250))
    telefone = db.Column(db.String(50))
    cpf = db.Column(db.String(20))
    usuario = db.relationship('Livro', secondary=emprestimo, backref=db.backref('emprestado', lazy='dynamic'))

    def __repr__(self):
        return '<Usuario: {}>'.format(self.nome)

    def __init__(self, nome,email,password,telefone, cpf):
        self.nome = nome
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.telefone = telefone
        self.cpf = cpf

class Livro(db.Model):
    __tablename__ = 'livros'
    id = db.Column(db.Integer, primary_key=True)
    autor = db.Column(db.String(250))
    titulo = db.Column(db.String(250))
    isbn = db.Column(db.String(250))
    editora = db.Column(db.String(150))
    sinopse = db.Column(db.String(2048))
    ano = db.Column(db.Integer)
    status = db.Column(db.Integer,default=0)
    

    def __repr__(self):
        return '<Livro: {} /{} >'.format(self.titulo, self.ano)

    def __init__(self, autor,titulo,isbn,editora,sinopse,ano, status):
        self.autor      = autor
        self.titulo     = titulo
        self.isbn       = isbn
        self.editora    = editora
        self.sinopse    = sinopse
        self.ano        = ano
        self.status     = status

class InsereUsuarioForm(FlaskForm):
    nome      = StringField('Nome',validators=[InputRequired(),Length(min=3)])
    email     = StringField('Email',validators=[InputRequired(),Email(message='Insira um email válido.')])
    password  = PasswordField('Senha',validators=[InputRequired(),Length(min=6)])
    password1 = PasswordField('Confirme a senha',validators=[InputRequired(), EqualTo('password')])
    telefone  = StringField('Telefone',validators=[InputRequired(),Length(min=6)])
    cpf       = StringField('CPF',validators=[InputRequired(),Length(min=11,max=11)])
    enviar    = SubmitField('Enviar')

def check_year(form, field):        # Validador WTF NOVO!
    y = datetime.today().year
    if field.data > y:
        raise ValidationError('O campo deve estar com valor inferior ou igual ao ano corrente. ')

class InsereLivroForm(FlaskForm):
    autor = StringField('Autor',validators=[InputRequired(),Length(min=3)])
    titulo = StringField('Titulo',validators=[InputRequired()])
    isbn = StringField('ISBN',validators=[InputRequired(),Length(min=6)])
    editora = StringField('Editora',validators=[InputRequired(),Length(min=6)])
    ano = IntegerField('Ano',validators=[InputRequired(), check_year])
    sinopse = StringField('Sinopse',validators=[InputRequired(),Length(min=20,max=2048)])
    enviar = SubmitField('Enviar')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[InputRequired(),Email(message='Insira um email válido.')],render_kw={"placeholder": "Entre com seu email"})
    senha = PasswordField('Senha',validators=[InputRequired()],render_kw={"placeholder": "Insira a sua senha"})
    enviar = SubmitField('Login', render_kw={"_class": "btn btn-info"} )

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.tpl'), 404

@app.route('/')
def index():
    return render_template('index.tpl')


@app.route('/registro',methods=['GET'])
def registro_get():
    form = InsereUsuarioForm()
    return render_template('registra.tpl', formtpl = form)


@app.route('/registro',methods=['POST'])
def registro_post():
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
    return redirect('/registro')

########################################################################
# USUÁRIOS
########################################################################

@app.route('/usuarios')
@login_required
def lista_usuarios():
    dados = Usuario.query.all()
    return render_template('usuarios.tpl', dadostpl = dados)    

@app.route('/usuarioadd',methods=['GET'])
@login_required
def add_usuario_get():
    form = InsereUsuarioForm()
    return render_template('add_usuario.tpl', formtpl = form)


@app.route('/usuarioadd',methods=['POST'])
@login_required
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
@login_required
def edit_usuario_get(_id):
    u = Usuario.query.filter_by(id=_id).first()
    form = InsereUsuarioForm(obj=u)
    return render_template('edit_usuario.tpl', formtpl = form, _id = _id)


@app.route('/usuarioedit/<_id>',methods=['POST'])
@login_required
def edit_usuario_post(_id):
    form = InsereUsuarioForm(request.form)
    u = Usuario.query.filter_by(id=_id).first()
    if form.validate_on_submit():
        form.populate_obj(u)
        db.session.commit()
        flash('Usuário alterado com sucesso.','success')
    else :
        flash('Não alterado. Problemas nos dados.'+str(form.errors),'danger')
    return redirect('/usuarios')

@app.route('/usuarioview/<_id>',methods=['GET'])
@login_required
def view_usuario_get(_id):
    u = Usuario.query.filter_by(id=_id).first()
    return render_template('view_usuario.tpl', d = u)

@app.route('/usuariodel/<_id>',methods=['GET'])
@login_required
def del_usuario_get(_id):
    u = Usuario.query.filter_by(id=_id).first()
    return render_template('del_usuario.tpl', d = u)

@app.route('/usuariodel/<_id>',methods=['POST'])
@login_required
def del_usuario_post(_id):
    u = Usuario.query.filter_by(id=_id).first()
    db.session.delete(u)
    db.session.commit()
    flash('Usuário excluído com sucesso.','success')
    return redirect('/usuarios')

########################################################################
# LIVROS
########################################################################

@app.route('/livros')
def lista_livros():
    dados = Livro.query.all()
    return render_template('livros.tpl', dadostpl = dados)    

@app.route('/livroadd',methods=['GET'])
@login_required
def add_livro_get():
    form = InsereLivroForm()
    return render_template('add_livro.tpl', formtpl = form)


@app.route('/livroadd',methods=['POST'])
@login_required
def add_livro_post():
    form = InsereLivroForm(request.form)
    if form.validate_on_submit():
        novo_livro = Livro(	autor 	= form.autor.data,
                            titulo 	= form.titulo.data,
                            isbn 	= form.isbn.data,
                            editora 	= form.editora.data,
                            ano 		= form.ano.data,
                            sinopse 	= form.sinopse.data)
        db.session.add(novo_livro)
        db.session.commit()
        flash('Livro inserido com sucesso.','success')
    else :
        flash('Não inserido. Problemas nos dados.'+str(form.errors),'danger')
    return redirect('/livros')

@app.route('/livroedit/<_id>',methods=['GET'])
@login_required
def edit_livro_get(_id):
    u = Livro.query.filter_by(id=_id).first()
    form = InsereLivroForm(obj=u)
    return render_template('edit_livro.tpl', formtpl = form, _id = _id)


@app.route('/livroedit/<_id>',methods=['POST'])
@login_required
def edit_livro_post(_id):
    form = InsereLivroForm(request.form)
    u = Livro.query.filter_by(id=_id).first()
    if form.validate_on_submit():
        form.populate_obj(u)
        db.session.commit()
        flash('Livro alterado com sucesso.','success')
    else :
        flash('Não alterado. Problemas nos dados.'+str(form.errors),'danger')
    return redirect('/livros')

@app.route('/livroview/<_id>',methods=['GET'])
def view_livro_get(_id):
    u = Livro.query.filter_by(id=_id).first()
    return render_template('view_livro.tpl', d = u)

@app.route('/livrodel/<_id>',methods=['GET'])
@login_required
def del_livro_get(_id):
    u = Livro.query.filter_by(id=_id).first()
    return render_template('del_livro.tpl', d = u)

@app.route('/livrodel/<_id>',methods=['POST'])
@login_required
def del_livro_post(_id):
    u = Livro.query.filter_by(id=_id).first()
    db.session.delete(u)
    db.session.commit()
    flash('Livro excluído com sucesso.','success')
    return redirect('/livros')

########################################################################
# EMPRESTIMOS
# https://stackoverflow.com/questions/6044309/sqlalchemy-how-to-join-several-tables-by-one-query
########################################################################

@app.route('/emprestimolivro')

def lista_empr_livros():
    #dados_e = (db.session.query(emprestimo,Livro, func.max(emprestimo.id).label('empr').scalar()  ) 
    #.filter(emprestimo.c.livro_id == Livro.id)
    #.func.max(emprestimo.id).label('empr').scalar()              # Se o livro está na tabela de empreśtimos
    #.filter(emprestimo.c.data_efetiva_devolucao == None)    # Não foi devolvido (condição suficiente)
    #.filter(Livro.status == 1)                              # status -> emprestado
    #.all())
    sql = text("""select livros.id, livros.titulo, livros.autor, livros.editora, livros.isbn, livros.ano, livros.sinopse, livros.status, data_emprestimo,eid,data_efetiva_devolucao from livros
    join (select data_emprestimo,id as eid,livro_id,data_efetiva_devolucao, max(data_emprestimo) as empr from emprestimos group by livro_id)
    on livro_id = livros.id
    group by (livros.id)""")
    dados = db.engine.execute(sql).fetchall()
    return render_template('emprestimo_livros.tpl', dadostpl = dados)  

@app.route('/emprestimousuario/<_lid>')

def lista_empr_usuarios(_lid):
    dados = Usuario.query.all()
    return render_template('emprestimo_usuarios.tpl', dadostpl = dados, livro_id=_lid)  


@app.route('/emprestimoconfirma/<_uid>/<_lid>')

def lista_empr_confirma(_uid,_lid):
    usuario = Usuario.query.filter_by(id=_uid).first()
    livro   = Livro.query.filter_by(id=_lid).first()
    return render_template('emprestimo_confirma.tpl', usuario=usuario, livro=livro)


@app.route('/emprestimoefetua', methods=['POST'])

def lista_empr_efetua():
    empr = True
    try:
        U = request.form.get('id_usuario')
        L = request.form.get('id_livro')
        usuario = Usuario.query.filter_by(id=U).first()
        livro   = Livro.query.filter_by(id=L).first()
        livro.emprestado.append(usuario)
        livro.status = 1
        db.session.add(livro)
        db.session.commit()
        flash('Emprestado para o usuario [{}] o livro [{}] do autor [{}].'.format(usuario.nome,livro.titulo,livro.autor),'success')
    except Exception as e:
        flash('NÃO emprestado para o usuario {} o livro {} do autor {}.'.format(usuario.nome,livro.titulo,livro.autor), 'danger')
    return redirect(url_for('lista_empr_livros'))

########################################################################
# DEVOLUCOES
########################################################################

@app.route('/devolveemprestimo/<int:_eid>')

def devolucao_confirma(_eid):
    empr = db.session.query(emprestimo).filter_by(id=_eid).first()
    usuario  = Usuario.query.filter_by(id=empr.usuario_id).first()
    livro    = Livro.query.filter_by(id=empr.livro_id).first()
    return render_template('devolucao_confirma.tpl', usuario=usuario, livro=livro, empr = empr, hoje = datetime.now()) 


@app.route('/devolucaoefetua', methods=['POST'])

def lista_dev_efetua():
    E = request.form.get('empr')
    U = request.form.get('id_usuario')
    L = request.form.get('id_livro')
    DEVOLUCAO = datetime.today()
    print("DEV: ",DEVOLUCAO)
    #app.config.update(
    #    SQLALCHEMY_ECHO=True
    #)
    try:
        livro = Livro.query.filter_by(id=L).first()
        livro.status = 0
        
        devolve = db.session.query(emprestimo).filter_by(id=E)
        print("devolve: ",devolve)
        devolve.data_efetiva_devolucao = datetime.now()
        db.session.commit()
        db.session.add(livro)
        #emprestimo.update().where( emprestimo.c.id == int(E) ).values( {"data_efetiva_devolucao" : DEVOLUCAO.strftime('%Y-%m-%d') } )
        db.session.commit()
        #print("DEVOL: ",devolve,"E: ",E, "DEV: ",DEVOLUCAO)
        
        #db.session.commit()
        print("DEV: ",DEVOLUCAO)
        flash('Empréstimo [{}] devolvido.'.format(E),'success')
    except Exception as e:
        flash('NÃO devolvido o empréstimo [{}] {}.'.format(E,str(e)), 'danger')
    return redirect(url_for('lista_empr_livros'))

    
########################################################################

@app.route('/login',methods=['GET'])
def login_get():
    form = LoginForm()
    return render_template('login.tpl', formtpl = form)

@app.route('/login',methods=['POST'])
def login_post():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first() # None se não encontrar
        if usuario is not None:
            if check_password_hash(usuario.password_hash,form.senha.data):
                login_user(usuario)
                return redirect(url_for('index'))
                #print('Login OK')
            else:
                flash('Usuário ou senha incorretos.', 'danger')
                #print('Login NOK1')
        else:
            flash('Usuário ou senha incorretos.', 'danger')
            #print('Login NOK2')
    else:
        msg ='Dados incorretos.'+str(form.errors) 
        flash(msg , 'danger')
        #print('Login NOK3')
    return redirect(url_for('login_get'))
    
@app.route('/logout',methods=['GET'])
def logout():
    logout_user()
    return redirect( url_for('login_get'))
   
if __name__ == "__main__":
    app.run()
