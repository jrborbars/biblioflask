{% extends "base.tpl" %}
{% import 'bootstrap/wtf.html' as wtf %}

{% block title %}Visualizar Usuários{% endblock %}

{% block content %}
        <h2>Usuário</h2>
                    <p>Nome: {{ d.nome }}</p>
                    <p>Email: {{ d.email }}</p>
                    <p>CPF: {{ d.cpf }}</p>
                    <p>Fone: {{ d.telefone }}</p>
                <a class="btn btn-info" href="{{ url_for('lista_usuarios') }}" >Voltar</a>
{% endblock %}
