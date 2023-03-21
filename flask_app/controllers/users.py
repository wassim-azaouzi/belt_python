from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.magazine import Magazine

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/users/register', methods =['post'])
def register():
    if not User.validate(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    user_data = {
        **request.form,
        'password':pw_hash
    }
    user_id = User.create_user(user_data)
    session["user_id"] = user_id
    return redirect('/dashboard')

@app.route('/users/login' , methods=['post'])
def login():
    user = User.get_by_email({'email': request.form["email"]})
    if not user :
        flash("Invalid Email/ Password", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email/Password", "login")
        return redirect('/')
    session["user_id"] = user.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    all_magazines = Magazine.get_all()
    logged_in_user = User.get_by_id({'id': session['user_id']})
    return render_template("dashboard.html", user = logged_in_user, all_magazines = all_magazines)

@app.route('/user/account')
def view_account():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_by_id({'id':session['user_id']})
    user_magazine= User.get_user_magazines({'id':session['user_id']})
    return render_template("account.html", user = user, user_magazine=user_magazine)

@app.route('/user/update', methods=['post'])
def update():
    if not User.update_validate(request.form):
        return redirect('/user/account')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email':request.form['email'],
        'id': session["user_id"]
    }
    User.update_user(data)
    return redirect('/dashboard')