from init import app
from flask import render_template
from article.models import *


@app.route('/')
@app.route('/index/')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('hello.html', posts=posts)
