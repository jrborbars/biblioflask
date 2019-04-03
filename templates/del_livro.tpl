{% extends "base.tpl" %}
{% import 'bootstrap/wtf.html' as wtf %}

{% block title %}Visualizar Livro{% endblock %}

{% block content %}
        <h2>Livro</h2>
        <p class="alert alert-danger"> Você tem certeza que deseja deletar o livro?</p>
            <form action="{{ url_for('del_livro_post', _id = d.id) }}" method="POST">
                    <input type="hidden" name="_id" value="{{ d.id }}" />
                    <p>Autor: {{ d.autor }}</p>
                    <p>Título: {{ d.titulo }}</p>
                    <p>ISBN: {{ d.isbn }}</p>
                    <p>Ano: {{ d.ano }}</p>
                    <button class="btn btn-danger" type="submit">Deletar</button>
                    <a class="btn btn-info" href="{{ url_for('lista_livros') }}" >Voltar</a>
            </form>
{% endblock %}
