from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_moment import Moment
#from flaskext.markdown import Markdown

app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

migrate = Migrate(app, db)
