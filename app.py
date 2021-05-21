
from werkzeug.utils import redirect
from flask import Flask, request
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_marshmallow import Marshmallow
from flask_restful import Api , Resource


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma =Marshmallow(app)
api = Api(app)




class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    desciption = db.Column(db.String(1000), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Blog %r>' % self.title


class BlogSchema(ma.Schema):
    class Meta:
        fields = ['id','title','desciption','author','pub_date']
        model = Blog
blog_schema = BlogSchema()
blogs_schema = BlogSchema(many=True)

@app.route("/", methods=['GET', 'POST'])
def index():
    author = Author.query.all()

    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        auth = request.form['author']

        blog = Blog(title=title, desciption=desc, author=auth)
        db.session.add(blog)
        db.session.commit()
    blogs = Blog.query.all()

    return render_template('index.html', authors=author, blogs=blogs)


@app.route("/add", methods=['GET', 'POST'])
def authoradd():

    if request.method == 'POST':
        name = request.form['author']
        author = Author(name=name)
        db.session.add(author)
        db.session.commit()
    return redirect('/')


@app.route("/author")
def authorform():
    return render_template('author.html')


@app.route("/view/<int:s_no>", methods=['GET', 'POST'])
def viewblog(s_no):
    print(s_no)
    blog = Blog.query.filter_by(id=s_no).first()
    print(blog)

    return render_template('viewblog.html', blog=blog)


@app.route("/delete/<int:s_no>", methods=['GET', 'POST'])
def deleteblog(s_no):
    print(s_no)
    blog = Blog.query.filter_by(id=s_no).first()
    print(blog)

    db.session.delete(blog)
    db.session.commit()

    return redirect('/')


@app.route("/updateform/<int:s_no>", methods=['GET', 'POST'])
def updateform(s_no):
    print(s_no)
    author= Author.query.all()
    blog = Blog.query.filter_by(id=s_no).first()

    return render_template('update.html', authors=author,blog=blog)


@app.route("/update/<int:s_no>", methods=['GET', 'POST'])
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
            title =request.json['title'],
            desciption = request.json['description'],
            author = request.json['author']
        )
        db.session.add(new_blog)
        db.session.commit()
        return blog_schema.dump(new_blog)

api.add_resource(BlogAPi, '/api')



class BlogApiFetch(Resource):

    def get(self,blog_id):

        blog =Blog.query.get(blog_id)
        return blog_schema.dump(blog)

    def patch(self,blog_id):
        blog = Blog.query.get(blog_id)
        
        if 'title' is  request.json:
            blog.title= request.json['title']
        if 'description' is  request.json:
            blog.desciption= request.json['description']
        if 'author' is  request.json:
            blog.title= request.json['author']
        
        db.session.commit()
        return blog_schema.dump(blog)

    def delete(self,blog_id):
        blog = Blog.query.get(blog_id)

        db.session.delete(blog)
        db.session.commit()

        return 'no contain', 204



api.add_resource(BlogApiFetch, '/api/<int:blog_id>')



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)

