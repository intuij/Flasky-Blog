from init import app
from flask import render_template, request
from article.models import *


@app.route('/', methods=['GET', 'POST'])
@app.route('/index/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_NUM_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('hello.html', posts=posts, pagination=pagination)
