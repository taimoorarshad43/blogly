"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

with app.app_context():
    connect_db(app)
    db.create_all()


@app.route('/')
def home():
    return redirect("/users")

@app.route('/users')
def users():
    users = User.query.all()                                    # Will return a blank list for now
    return render_template("users.html", users = users)


@app.route('/users/new')
def adduser():
    return render_template('createuser.html')

@app.route('/users/new', methods = ['POST'])
def adduserpost():

    firstname = request.form['firstname']
    lastname = request.form['lastname']
    imgurl = request.form['imgurl']

    user = User(firstname = firstname, lastname = lastname, image_url = imgurl)

    db.session.add(user)
    db.session.commit()

    users = User.query.all()

    return redirect('/users.html', users = users)

@app.route('/users/<int:userid>')
def getuser(userid):
    user = User.query.filter_by(id = userid).first()
    return render_template('detail.html', user=user)

@app.route('/users/<int:userid>/edit')
def getuseredit(userid):
    user = User.query.filter_by(id = userid).first()
    return render_template('edituser.html', user=user)


@app.route('/users/<int:userid>/edit', methods = ['POST'])
def getusereditpost(userid):

    user = User.query.filter_by(id = userid).first()

    user.firstname = request.form['firstname']
    user.lastname = request.form['lastname']
    user.image_url = request.form['imgurl']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:userid>/delete', methods = ['POST'])
def deleteuser(userid):

    User.query.filter_by(id = userid).delete()
    db.session.commit()

    users = User.query.all()

    return redirect('/', users = users)