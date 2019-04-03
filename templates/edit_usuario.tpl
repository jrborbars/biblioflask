{% extends "base.tpl" %}
{% import 'bootstrap/wtf.html' as wtf %}

{% block title %}Edita Usuário{% endblock %}

{% block content %}
        <h2>Usuário</h2>
                {{ wtf.quick_form( form=formtpl, action=url_for('edit_usuario_post') )}}
{% endblock %}
