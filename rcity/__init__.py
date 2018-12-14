import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

#Config de la aplicacion
app = Flask(__name__)
app.config['SECRET_KEY'] = '\xde:J0w\x98|~\x80\xc8z\x8fC\x93,f\x93\xa5?w'
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

#Config de la db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'rcity.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run(debug=True)

from . import views, apis