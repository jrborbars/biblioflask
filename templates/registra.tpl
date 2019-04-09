{% extends "base.tpl" %}
{% import 'bootstrap/wtf.html' as wtf %}

{% block title %}Registra Usuários{% endblock %}

{% block content %}
                {% with messages = get_flashed_messages(with_categories=true) %}
                  {% if messages %}
                    <ul class="flashes">
                    {% for category, message in messages %}
                      <li class="alert alert-{{ category }}">{{ message }}</li>
                    {% endfor %}
                    </ul>
                  {% endif %}
                {% endwith %}


        <h2>Usuário</h2>
                {{ wtf.quick_form( form=formtpl, action=url_for('registro_post' )) }}
{% endblock %}
