import os

from flask import Flask
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = '.\\rcity\\static\\files'


#Config de la aplicacion
app = Flask(__name__)
app.config['SECRET_KEY'] = '\xde:J0w\x98|~\x80\xc8z\x8fC\x93,f\x93\xa5?w'
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Config de la db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'rcity.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'


if __name__ == '__main__':
    app.run(debug=True)

from . import views, apis


CORS(app, resources={r"/api/*": {"origins": "*"}})