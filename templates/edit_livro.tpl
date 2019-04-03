{% extends "base.tpl" %}
{% import 'bootstrap/wtf.html' as wtf %}

{% block title %}Edita Livro{% endblock %}

{% block content %}
        <h2>Livro</h2>
                {{ wtf.quick_form( form=formtpl, action=url_for('edit_livro_post', _id = _id) )}}<a class="btn btn-info" href="{{ url_for('lista_livros') }}" >Voltar</a>
                
{% endblock %}

