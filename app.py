#!/usr/bin/env python

import blog
import flask
import os

app = flask.Flask(__name__)

def template_renderer(template: str) -> str:
	# TODO: Do this without pushing a request context
	with app.test_request_context():
		return flask.render_template_string(template)

article_repository = blog.ArticleRepository(
	os.path.join(app.root_path, app.template_folder),
	template_renderer
)

app.url_map.converters["article"] = article_repository.converter()

with app.app_context():
	article_index = blog.ArticleIndex(article_repository)

@app.route("/article/<article:article>")
def article(article: blog.Article) -> str:
	return flask.render_template("article.html", article=article)

@app.route("/")
def index() -> str:
	return flask.render_template("index.html", articles=article_repository.articles)

@app.route("/search")
def search() -> str:
	if "query" in flask.request.args:
		search_query = flask.request.args["query"]
		articles=article_index.search(search_query)
	else:
		search_query = ""
		articles = article_repository.articles

	return flask.render_template("index.html", articles=articles, search_query=search_query)
