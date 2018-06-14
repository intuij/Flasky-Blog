from flask import render_template, redirect, request, url_for, flash, abort
from user.forms import LoginForm, RegisterForm, ProfileForm
from flask_login import login_user, login_required, logout_user, current_user
from article.forms import *
from init import app
from user.decorators import admin_required
from article.models import Post


@app.route('/post/<int:id>')
def show_post(id):
    post = Post.query.get_or_404(id)
    return render_template('post/post.html', posts=[post])


@app.route('/post/edit/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and not current_user.check_permission(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.content = form.content.data
        post.title = form.title.data
        db.session.add(post)
        db.session.commit()
        flash('You have changed this article')
        return redirect(url_for('show_post', id=post.id))
    form.content.data = post.content
    form.title.data = post.title
    return render_template('/post/edit_post.html', form=form)
