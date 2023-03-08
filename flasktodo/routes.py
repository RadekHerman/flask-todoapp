import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from flasktodo import app, db, bcrypt
from flasktodo.forms import RegistrationForm, LoginForm, UpdateAccountForm, TaskForm, \
                            ChangePasswordForm, ResetPasswordForm
from flasktodo.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import datetime
import calendar


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')


@app.route("/todolist")
@login_required
def list():
    # todolist = Post.query.all()
    todolist = Post.query.filter_by(user_id=current_user.id).all()
    return render_template('todolist.html', title='Your List', todolist=todolist)

@app.route("/todolist/add", methods=["GET", "POST"])
@login_required
def add_to_list():
    form = TaskForm()
    if form.validate_on_submit():
        post = Post(subject=form.subject.data, content=form.content.data, date_todo=form.date_todo.data, hour_todo=form.hour_todo.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Added to list.', 'success')
        return redirect(url_for('list'))
    return render_template("add.html", title='Add To List', form=form, legend="Add To List")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        flash('New password has been send to your email address. Please change it as soon as you login again', 'danger')

    return render_template('reset-password.html', title='Reset Password', form=form)



@app.route("/login", methods=["GET", "POST"])
def login():    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.username.data != '':
            current_user.username = form.username.data
        if form.email.data != '':      
            current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


@app.route("/change-password", methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('change_password'))
    return render_template('change-password.html', title='Change Password', form=form)


@app.route("/todolist/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update(post_id):
    post = Post.query.get_or_404(post_id)
    form = TaskForm()
    if form.validate_on_submit():
        post.subject = form.subject.data
        post.content = form.content.data
        post.date_todo = form.date_todo.data
        post.hour_todo = form.hour_todo.data
        db.session.commit()
        flash('Your list has been updated.', 'success')
        return redirect(url_for('list'))
    elif request.method == 'GET':
        form.subject.data = post.subject
        form.content.data = post.content
        form.date_todo.data = post.date_todo
        form.hour_todo.data = post.hour_todo

    return render_template("add.html", title='Update', form=form, legend='Update')

@app.route("/todolist/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Your list has been updated!', 'success')
    return redirect(url_for('list'))


@app.route('/calendar')
def show_calendar():
      # Create a list of month names and their corresponding calendars
    now = datetime.datetime.now()
    year = now.year
    current_month = calendar.month_name[now.month]
    months = []
    for month in range(1, 13):
        cal = calendar.monthcalendar(year, month)
        months.append({
            'month': calendar.month_name[month],
            'calendar': cal
        })

    return render_template('calendar.html', current_month=current_month, months=months, now=now)