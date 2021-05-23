from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api 
from flask_login import LoginManager


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
db = SQLAlchemy()
ma = Marshmallow()
api = Api()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'fgfhfhhyrtgdrgdrgdrtgdr'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
    app.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = False
  
    db.init_app(app)
    api.init_app(app)
    ma.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))


    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)


    from .blog import blog as blog_blueprint    
    app.register_blueprint(blog_blueprint)

    return app