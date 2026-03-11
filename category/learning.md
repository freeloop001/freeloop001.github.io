---
layout: default
title: 学习笔记
---

<h1 style="font-family: var(--font-display); font-size: 28px; margin-bottom: 32px; text-align: center;">学习笔记</h1>

<ul class="post-list">
{% for post in site.categories.learning %}
  <li class="post-item">
    <h2 class="post-title">
      <a href="{{ post.url }}">{{ post.title }}</a>
    </h2>
    <div class="post-meta">
      <time>{{ post.date | date: "%Y年%m月%d日" }}</time>
      {% if post.categories %}
      <span class="post-category-link">
        {% for cat in post.categories %}
          <a href="/category/{{ cat }}/">{{ cat }}</a>{% unless forloop.last %}, {% endunless %}
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
