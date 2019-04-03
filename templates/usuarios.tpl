{% extends "base.tpl" %}
{% block title %}Lista Usuários{% endblock %}
 
{% block content %}
        <p><a href="/usuarioadd">Cadastra Usuário</a></p>
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
                <th>Nome</th>
                <th>Email</th>
                <th>Password</th>
                <th>Telefone</th>
                <th>CPF</th>
                <th>Ações</th>
            </thead>
            <tbody>
                {% for dado in dadostpl %}
                <tr>
                    <td>{{ dado.id }}</td>
                    <td>{{ dado.nome }}</td>
                    <td>{{ dado.email }}</td>
                    <td>{{ dado.password }}</td>
                    <td>{{ dado.telefone }}</td>
                    <td>{{ dado.cpf }}</td>
                    <td>
                        <a href="/usuarioedit/{{ dado.id }}">Editar</a>
              <!--      
                    <a href="{{ url_for('books', genre='biography') }}">Books</a>

                    Output:

                    1
                        
                    <a href="/books/biography/">Books</a>
                  -->  
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
{% endblock %}
