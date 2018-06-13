from flask import render_template, redirect, request, url_for, flash, abort
from user.forms import LoginForm, RegisterForm, ProfileForm
from flask_login import login_user, login_required, logout_user, current_user
from article.forms import *
from init import app
from user.decorators import admin_required


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash("Invalid email or password!")
    return render_template('user/login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Register Success!')
        return redirect(url_for('login'))
    return render_template('user/register.html', form=form)


@app.route('/user/<username>')
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    else:
        return render_template('user/profile.html', user=user)


@app.route('/user/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.fullname = form.fullname.data
        current_user.location = form.location.data
        current_user.desc = form.desc.data
        db.session.add(current_user)
        db.session.commit()
        flash('You have modified your profile!')
        return redirect(url_for('user_profile', username=current_user.username))

    form.fullname.data = current_user.fullname
    form.location.data = current_user.location
    form.desc.data = current_user.desc
    return render_template('user/edit_profile.html', form=form)


@app.route('/user/add-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post()
        post.title = form.title.data
        post.content = form.content.data
        post.author = current_user._get_current_object()
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('post/add_post.html', form=form)


@app.route('/user/post-list')
@login_required
def post_list():
    curr_user = User.query.filter_by(username=current_user.username).first()
    posts = curr_user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('post/post_list.html', posts=posts, user=curr_user)


@app.route('/admin')
@login_required
@admin_required
def for_admin():
    return "For admin only!"


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
    else:
        return


