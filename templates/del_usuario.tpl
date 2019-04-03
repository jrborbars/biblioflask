{% extends "base.tpl" %}
{% import 'bootstrap/wtf.html' as wtf %}

{% block title %}Visualizar Usuários{% endblock %}

{% block content %}
        <h2>Usuário</h2>
        <p class="alert alert-danger"> Você tem certeza que deseja deletar o usuário?</p>
            <form action="{{ url_for('del_usuario_post', _id = d.id) }}" method="POST">
                    <input type="hidden" name="_id" value="{{ d.id }}" />
                    <p>Nome: {{ d.nome }}</p>
                    <p>Email: {{ d.email }}</p>
                    <p>CPF: {{ d.cpf }}</p>
                    <p>Fone: {{ d.telefone }}</p>
                    <button class="btn btn-danger" type="submit">Deletar</button>
                    <a class="btn btn-info" href="{{ url_for('lista_usuarios') }}" >Voltar</a>
            </form>
{% endblock %}
