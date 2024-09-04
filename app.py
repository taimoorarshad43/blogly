"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post
from pic import pic

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

with app.app_context():                                         # New in Flask 3. You need the app_context to work with the application object.
    connect_db(app)
    db.drop_all()                                               # Start with fresh db.
    db.create_all()

################################################### User Routes ####################################################

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
    imgurl = request.form['imgurl'] if len(request.form['imgurl']) > 0 else pic

    # Allows for a default picture

    user = User(firstname = firstname, lastname = lastname, image_url = imgurl)

    db.session.add(user)
    db.session.commit()

    users = User.query.all()

    return redirect('/users')

@app.route('/users/<int:userid>')
def getuser(userid):
    user = User.query.filter_by(id = userid).first()
    posts = Post.query.filter_by(user_id = userid)

    print("Post are: ", posts)

    return render_template('userdetail.html', user=user, posts = posts)

@app.route('/users/<int:userid>/edit')
def getuseredit(userid):
    user = User.query.filter_by(id = userid).first()
    return render_template('edituser.html', user=user)


@app.route('/users/<int:userid>/edit', methods = ['POST'])
def getusereditpost(userid):

    user = User.query.filter_by(id = userid).first()

    user.firstname = request.form['firstname'] if len(request.form['firstname']) > 0 else user.firstname
    user.lastname = request.form['lastname'] if len(request.form['lastname']) > 0 else user.lastname
    user.image_url = request.form['imgurl'] if len(request.form['imgurl']) > 0 else user.image_url
    
    # That should allow for user to retain previous changes if they didn't want to change certain fields.

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:userid>/delete', methods = ['POST'])
def deleteuser(userid):

    User.query.filter_by(id = userid).delete()
    db.session.commit()

    users = User.query.all()                    # Not sure if we need this

    return redirect('/')


################################################### Blog Post Routes ####################################################

@app.route('/users/<int:userid>/posts/new')
def addnewpost(userid):
    user = User.query.filter_by(id = userid).first()

    return render_template("newpost.html", user = user)

@app.route('/users/<int:userid>/posts/new', methods = ['POST'])
def addnewpost_post(userid):
    user = User.query.filter_by(id = userid).first()

    title = request.form['title']
    content = request.form['content']
    user_id = user.id

    post = Post(title = title, content = content, user_id = user_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user.id}')

@app.route('/posts/<int:postid>')
def getpost(postid):
    post = Post.query.filter_by(id = postid).first()

    return render_template('postdetail.html', post = post)

@app.route('/posts/<int:postid>/edit')
def editpost(postid):
    post = Post.query.filter_by(id = postid).first()

    return render_template('editpost.html', post = post)

@app.route('/posts/<int:postid>/edit', methods = ['POST'])
def editpost_post(postid):
    post = Post.query.filter_by(id = postid).first()

    post.title = request.form['title'] if len(request.form['title']) > 0 else post.title
    post.content = request.form['content'] if len(request.form['content']) > 0 else post.content

    db.session.add(post)
    db.session.commit()

    # That should allow for user to retain previous changes if they didn't want to change certain fields.

    return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:postid>/delete', methods = ['POST'])
def deletepost(postid):
    post = Post.query.filter_by(id = postid)
    userid = post.first().users.id

    post.delete()

    db.session.commit()

    return redirect(f'/users/{userid}')
