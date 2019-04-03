from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world!'


@app.route('/123')
def minharota():
    return 'Bem vindo ao 123'

app.run()

# CRUD + L
"""
L: listar
C: criar (create)
R: consultar (read)
U: alterar (update)
D: deletar (delete)
"""


