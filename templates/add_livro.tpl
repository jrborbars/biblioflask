{% extends "base.tpl" %}
{% import 'bootstrap/wtf.html' as wtf %}

{% block title %}Adiciona Livros{% endblock %}

{% block content %}
        <h2>Livro</h2>
                {{ wtf.quick_form( form=formtpl) }}
{% endblock %}
