{% extends "base.tpl" %}
{% import 'bootstrap/wtf.html' as wtf %}

{% block title %}Adiciona Usuários{% endblock %}

{% block content %}
        <h2>Usuário</h2>
                {{ wtf.quick_form( form=formtpl) }}
{% endblock %}
