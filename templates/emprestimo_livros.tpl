{% extends "base.tpl" %}
{% block title %}Lista Livros Livros{% endblock %}
 
{% block content %}
        {% if current_user.is_authenticated %}
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
                    <td>{{ dado[0] }}</td>
                    <td>{{ dado[2] }}</td>
                    <td>{{ dado[1] }}</td>
                    <td>{{ dado[3] }}</td>
                    <td>{{ dado[4] }}</td>
                    <td>{{ dado[5] }}</td>
                    <td>{{ dado[6] | truncate(40, True)}}</td>
                    <td>
                    {% if dado[7] == 0 %}
                        <a class="btn btn-success" href="/emprestimousuario/{{ dado[0] }}">Emprestar</a>
                        <a class="btn btn-light" href="">Devolver</a>
                    {% else %}
                        <a class="btn btn-light" href="">Emprestar</a>
                        <a class="btn btn-success" href="/devolveemprestimo/{{ dado.eid }}">Devolver</a>
                    {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
{% endblock %}
