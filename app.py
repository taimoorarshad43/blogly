"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

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
def adduser():

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
def getuser(userid):
    user = User.query.filter_by(id = userid).first()
    return render_template('edituser.html', user=user)


@app.route('/users/<int:userid>/edit', methods = ['POST'])
def getuser(userid):

    user = User.query.filter_by(id = userid).first()

    user.firstname = request.form['firstname']
    user.lastname = request.form['lastname']
    user.image_url = request.form['imgurl']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


'''
**GET */ :*** Redirect to list of users. (We’ll fix this in a later step).
DONE

**GET */users :*** Show all users. Make these links to view the detail page for the user. Have a link here to the add-user form.
DONE

**GET */users/new :*** Show an add form for users
DONE

**POST */users/new :*** Process the add form, adding a new user and going back to ***/users***
TO-DO

**GET */users/[user-id] :***Show information about the given user. Have a button to get to their edit page, and to delete the user.
DONE

**GET */users/[user-id]/edit :*** Show the edit page for a user. Have a cancel button that returns to the detail page for a user, and a save button that updates the user.
DONE

**POST */users/[user-id]/edit :***Process the edit form, returning the user to the ***/users*** page.
DONE

**POST */users/[user-id]/delete :*** Delete the user.
TO-DO

'''