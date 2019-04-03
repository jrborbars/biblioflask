{% extends "base.tpl" %}
{% import 'bootstrap/wtf.html' as wtf %}

{% block title %}Visualizar Livro{% endblock %}

{% block content %}
        <h2>Livro</h2>
                    <p>Autor: {{ d.autor }}</p>
                    <p>Título: {{ d.titulo }}</p>
                    <p>ISBN: {{ d.isbn }}</p>
                    <p>Ano: {{ d.ano }}</p>
                    <p>Editora: {{ d.editora }}</p>
                    <p>Sinopse: {{ d.sinopse }}</p>
                <a class="btn btn-info" href="{{ url_for('lista_livros') }}" >Voltar</a>
{% endblock %}
