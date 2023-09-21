{% extends 'women/base.html' %}

{% block content %}
<ul class="list-articles">
	{% for p in posts %}
			<li><div class="article-panel">
	<p class="first">Категория: {{p.cat}}</p>
	<p class="last">Дата: {{p.time_update|date:"d-m-Y H:i:s"}}</p>
</div>
{% if p.photo %}
	<p><img class="img-article-left thumb" src="{{p.photo.url}}"></p>
{% endif %}
			   <h2>{{p.title}}</h2>
	 {% autoescape on %}
	 <p>{{p.content|linebreaks|truncatewords:50}}</p>
	 {% endautoescape %}
			<div class="clear"></div>
			<p class="link-read-post"><a href="{{ p.get_absolute_url }}">Читать пост</a></p>
			</li>
	{% endfor %}
</ul>
{% endblock %}
