# 文章模板

创建新文章时，在 `_posts` 目录下新建文件，命名格式：`YYYY-MM-DD-title.md`

```yaml
---
layout: post-toc
title: "文章标题"
date: 2026-03-11 16:00:00 +0800
categories: [learning]
tags: []
toc: |
  <a href="#1-标题1">1. 标题1</a>
  <a href="#2-标题2">2. 标题2</a>
---

## 1. 标题1

内容...

## 2. 标题2

内容...
```

**注意**：
- `layout`: 使用 `post-toc`（有目录）或 `post`（无目录）
- `date`: 必须包含精确时间，格式为 `YYYY-MM-DD HH:MM:SS +0800`
- `toc`: 目录链接需与正文中 `##` 标题的 id 对应（用小写英文、数字、连字符）
