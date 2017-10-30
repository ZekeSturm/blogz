from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from checker import postChecker, logSignChecker

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogginaway@localhost:8888/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'A very secret key'
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(5000))
    owner_id = db.Column(db.Integer, ForeignKey('user.id'))

    def __init__(self, name, body, user):
        self.name = name
        self.body = body
        self.owner_id = user.id


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = relationship("Blog")

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allowed_routes = ['login','bloglist','index','signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/',methods=['POST','GET'])
def index():
    users = User.query.all()
    return render_template('index.html',title='Blogz',users=users)


@app.route('/blog', methods=['POST', 'GET'])
def bloglist():

    if Blog.query.count() and request.args.get('id'):
        blogID = request.args.get('id')
        theBlog = Blog.query.get(blogID)
        poster = User.query.get(theBlog.owner_id)
        poster = poster.username
        return render_template('singleblog.html',title="Blogz",blog=theBlog,poster=poster)
    elif Blog.query.count() and request.args.get('userId'):
        userID = request.args.get('userId')
        blogs = Blog.query.filter_by(owner_id=userID).all()
        for blog in blogs:
            ownerObj = User.query.get(blog.owner_id)
            if ownerObj is not None:
                blog.owner_name = ownerObj.username
        return render_template('userbloglist.html',title='Blogz',blogs=blogs)
    else:
        blogs = Blog.query.all()
        for blog in blogs:
            ownerObj = User.query.get(blog.owner_id)
            if ownerObj is not None:
                blog.owner_name = ownerObj.username
        return render_template('bloglist.html',title="Blogz",blogs=blogs)


@app.route('/login', methods=['POST','GET'])
def login():

    if request.method == 'POST':
        user_name = request.form['username']
        pass_word = request.form['password']

        checkvals = logSignChecker(user_name,pass_word,"notSignIn")

        if checkvals["error"]:
            return render_template('login.html',title="Blogz",uname=user_name,unameerror=checkvals["nameerror"],passerror=checkvals["passerror"])
        else:
            userq = User.query.filter_by(username=user_name).first()
            if userq is not None:
                passquery = userq.password
                if passquery == pass_word:
                    session['username'] = userq.username
                    return redirect('/newpost')
                else:
                    return render_template('login.html',title="Blogz",uname=user_name,unameerror="",passerror="The password you entered was incorrect!")
            else:
                return render_template('login.html',title="Blogz",uname=user_name,unameerror="The username you entered does not exist!",passerror="")

    return render_template('login.html',title='Blogz',uname='',unameerror='',passerror='')


@app.route('/signup',methods=['POST','GET'])
def signup():

    if request.method == 'POST':
        user_name = request.form['username']
        pass_word = request.form['password']
        pass_conf = request.form['confirm']

        checkvals = logSignChecker(user_name,pass_word,pass_conf)

        if checkvals['error']:
            return render_template('signup.html',title="Blogz",uname=user_name,unameerror=checkvals['nameerror'],passerror=checkvals['passerror'],confirmerror=checkvals['confirmerror'])
        else:
            userq = User.query.filter_by(username=user_name).first()
            if userq is not None:
                return render_template('signup.html',title="Blogz",uname=user_name,unameerror='This username is already taken!',passerror='',confirmerror='')
            else:
                if pass_word == pass_conf:
                    new_user = User(user_name,pass_word)
                    db.session.add(new_user)
                    db.session.commit()
                    session['username'] = new_user.username
                    return redirect('/newpost')
                else:
                    return render_template('signup.html',title="Blogz",uname=user_name,unameerror='',passerror='Both password fields must match!',confirmerror='')

    return render_template('signup.html',title='Blogz',uname='',unameerror='',passerror='',confirmerror='')    


@app.route('/logout',methods=['POST','GET'])
def logout():
    del session['username']
    return redirect('/blog')    


@app.route('/newpost',methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':
        blog_name = request.form['blogname']
        blog_body = request.form['blogbody']
        userq = User.query.filter_by(username=session['username']).first()

        checkvals = postChecker(blog_name,blog_body)

        if checkvals["error"]:
            return render_template('newblog.html',title="Blogz",blogtitle=blog_name,blogbody=blog_body,nameerror=checkvals["nameerror"],blogerror=checkvals["blogerror"])
        else:
            new_blog = Blog(blog_name, blog_body, userq)
            db.session.add(new_blog)
            db.session.commit()
            return redirect ('/blog?id={}'.format(new_blog.id))

    return render_template('newblog.html',title="Blogz",blogtitle="",blogbody="",nameerror="",blogerror="")


if __name__ == '__main__':
    app.run()