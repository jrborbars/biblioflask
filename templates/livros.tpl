{% extends "base.tpl" %}
{% block title %}Lista Livros{% endblock %}
 
{% block content %}
        {% if current_user.is_authenticated %}
        <p><a class="btn btn-info" href="/livroadd">Cadastra Livro</a></p>
        {% endif %}
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            <ul class="flashes">
            {% for category, message in messages %}
              <li class="alert alert-{{ category }}"  role="alert" >{{ message }}</li>
            {% endfor %}
            </ul>
          {% endif %}
        {% endwith %}
        <table class="table table-stripped">
            <thead>
                <th>#</th>
                <th>Autor</th>
                <th>Título</th>
                <th>Editora</th>
                <th>ISBN</th>
                <th>Ano</th>
                <th>Sinopse</th>
                <th>Ações</th>
            </thead>
            <tbody>
                {% for dado in dadostpl %}
                <tr>
                    <td>{{ dado.id }}</td>
                    <td>{{ dado.autor }}</td>
                    <td>{{ dado.titulo }}</td>
                    <td>{{ dado.editora }}</td>
                    <td>{{ dado.isbn }}</td>
                    <td>{{ dado.ano }}</td>
                    <td>{{ dado.sinopse | truncate(40, True)}}</td>
                    <td>
                        {% if current_user.is_authenticated %}
                        <a class="btn btn-warning" href="/livroedit/{{ dado.id }}">Editar</a>
                        {% endif %}
                        <a class="btn btn-info" href="/livroview/{{ dado.id }}">Visualizar</a>
                        {% if current_user.is_authenticated %}
                        <a class="btn btn-danger" href="/livrodel/{{ dado.id }}">Deletar</a>
                        {% endif %}

                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
{% endblock %}
