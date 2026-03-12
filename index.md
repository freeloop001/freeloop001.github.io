---
layout: default
title: 首页
---

<ul class="post-list">
{% for post in site.posts %}
  <li class="post-item">
    <h2 class="post-title">
      <a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a>
    </h2>
    <div class="post-meta">
      <time>{{ post.date | date: "%Y年%m月%d日 %H:%M:%S" }}</time>
      {% if post.categories %}
      <span class="post-category-link">
        {% for cat in post.categories %}
          {% if cat == "tech" %}
            <a href="{{ site.baseurl }}/category/tech/">技术文章</a>
          {% elsif cat == "learning" %}
            <a href="{{ site.baseurl }}/category/learning/">学习笔记</a>
          {% else %}
            <a href="{{ site.baseurl }}/category/{{ cat }}/">{{ cat }}</a>
          {% endif %}
        {% endfor %}
      </span>
      {% endif %}
    </div>
    <p class="post-excerpt">{{ post.excerpt | strip_html | truncate: 150 }}</p>
    {% if post.tags %}
    <div class="post-tags">
      {% for tag in post.tags %}
        <span class="post-tag">{{ tag }}</span>
      {% endfor %}
    </div>
    {% endif %}
  </li>
{% endfor %}
</ul>
