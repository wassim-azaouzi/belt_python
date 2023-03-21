from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.magazine import Magazine
from flask_app.models.user import User


@app.route('/new')
def new_magazine():
    if 'user_id' not in session:
        return redirect('/')
    return render_template("magazine.html")

@app.route('/magazines/create', methods=['post'])
def create_magazine():
    if not Magazine.mag_validate(request.form):
        return redirect('/new')
    data = {
        **request.form,
        'user_id':session['user_id']
    }
    Magazine.create_magazine(data)
    return redirect('/dashboard')

@app.route('/magazines/delete/<int:magazine_id>')
def remove(magazine_id):
    Magazine.delete_subscribers({'id':magazine_id})
    Magazine.delete_magazines({'id':magazine_id})
    return redirect('/dashboard')


@app.route('/subscribe/<int:magazine_id>')
def subscribe(magazine_id):

    data={
        'magazine_id':magazine_id,
        'user_id':session['user_id']
    }
    if Magazine.subscribe_validate(data):
        Magazine.subscribe(data)
        Magazine.subscribe_count(data)
    return redirect('/dashboard')

@app.route('/show/<int:magazine_id>')
def view_magazine(magazine_id):
    if 'user_id' not in session:
        return redirect('/')
    magazine = Magazine.get_by_id({'id':magazine_id})
    user=User.get_by_id({'id':magazine.user_id})
    subscribers=Magazine.get_magazine_subscribers({'id':magazine_id})
    return render_template("show.html", magazine = magazine, user=user, subscribers=subscribers)