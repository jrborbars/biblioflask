{% extends "base.tpl" %}
{% import 'bootstrap/wtf.html' as wtf %}

{% block title %}Confirma devolucao{% endblock %}

{% block content %}
        {% set d=livro %}
        {% set u=usuario %}
        <form action="{{ url_for('lista_dev_efetua') }}" method="POST" >
            <h2>Livro</h2>
                        <input type="hidden" name="id_livro" value="{{ d.id }}" />
                        <p>Autor: {{ d.autor }}</p>
                        <p>Título: {{ d.titulo }}</p>
                        <p>ISBN: {{ d.isbn }}</p>
                        <p>Ano: {{ d.ano }}</p>
                        <p>Editora: {{ d.editora }}</p>
                        <p>Sinopse: {{ d.sinopse }}</p>
            <h2>Usuário</h2>
                        <input type="hidden" name="id_usuario" value="{{ u.id }}" />
                        <input type="hidden" name="empr" value="{{ empr.id }}" />
                        <p>Nome: {{ u.nome }}</p>
                        <p>Email: {{ u.email }}</p>
            <h2>Empréstimo</h2>
                        <p>Data do empréstimo: {{ empr.data_emprestimo.strftime('%d-%m-%Y') }}</p>
                        <p>Data de devolução : {{ hoje.strftime('%d-%m-%Y') }}</p>                        
                        <input type="submit" value="Devolver" />
        </form>
                <a class="btn btn-info" href="{{ url_for('lista_empr_livros') }}" >Voltar</a>
{% endblock %}
