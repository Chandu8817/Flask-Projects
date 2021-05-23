
from enum import unique
from werkzeug.utils import redirect
from flask import Flask, request
from flask.templating import render_template
from flask_login import login_required, current_user

from flask_restful import Resource
from .models import Blog, Author
from . import api, ma, db
from flask import Blueprint, render_template, redirect, url_for, request, flash

blog = Blueprint('blog', __name__)


class BlogSchema(ma.Schema):
    class Meta:
        fields = ['id', 'title', 'desciption', 'author', 'pub_date']
        model = Blog


blog_schema = BlogSchema()
blogs_schema = BlogSchema(many=True)


@blog.route("/", methods=['GET','POST'])
def index():
    author = Author.query.all()
    print(author)

    if request.method == 'POST':

        title = request.form['title']
        desc = request.form['desc']
        auth = request.form['author']
        print(title, desc, auth)

        blog = Blog(title=title, desciption=desc, author=auth)
        db.session.add(blog)
        db.session.commit()
    blogs = Blog.query.all()

    return render_template('index.html', authors=author, blogs=blogs)


@blog.route("/add", methods=['GET', 'POST'])
def authoradd():

    if request.method == 'POST':
        name = request.form['author']
        author = Author(name=name)
        db.session.add(author)
        db.session.commit()
    return redirect('/')


@blog.route("/author")
def authorform():
    author = Author.query.all()
    print(author)
    return render_template('author.html', authors=author)


@blog.route("/view/<int:s_no>", methods=['GET', 'POST'])
def viewblog(s_no):
    print(s_no)
    blog = Blog.query.filter_by(id=s_no).first()
    print(blog)

    return render_template('viewblog.html', blog=blog)


@blog.route("/delete/<int:s_no>", methods=['GET', 'POST'])
def deleteblog(s_no):
    print(s_no)
    blog = Blog.query.filter_by(id=s_no).first()
    print(blog)

    db.session.delete(blog)
    db.session.commit()

    return redirect('/')


@blog.route("/updateform/<int:s_no>", methods=['GET', 'POST'])
def updateform(s_no):
    print(s_no)
    author = Author.query.all()
    blog = Blog.query.filter_by(id=s_no).first()

    return render_template('update.html', authors=author, blog=blog)


@blog.route("/update/<int:s_no>", methods=['GET', 'POST'])
def updateblog(s_no):
    print(s_no)
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

        blog = Blog.query.filter_by(id=s_no).first()
        blog.title = title
        blog.desciption = desc
        db.session.commit()

    return redirect(f'/view/{s_no}')


class BlogAPi(Resource):
    def get(self):

        blogs = Blog.query.all()

        return blogs_schema.dump(blogs)

    def post(self):
        new_blog = Blog(
            title=request.json['title'],
            desciption=request.json['description'],
            author=request.json['author']
        )
        db.session.add(new_blog)
        db.session.commit()
        return blog_schema.dump(new_blog)


api.add_resource(BlogAPi, '/api')


class BlogApiFetch(Resource):

    def get(self, blog_id):

        blog = Blog.query.get(blog_id)
        return blog_schema.dump(blog)

    def patch(self, blog_id):
        blog = Blog.query.get(blog_id)

        if 'title' in request.json:
            blog.title = request.json['title']
        if 'description' in request.json:
            blog.desciption = request.json['description']
        if 'author' in request.json:
            blog.title = request.json['author']

        db.session.commit()
        return blog_schema.dump(blog)

    def delete(self, blog_id):
        blog = Blog.query.get(blog_id)

        db.session.delete(blog)
        db.session.commit()

        return 'no contain', 204


api.add_resource(BlogApiFetch, '/api/<int:blog_id>')
