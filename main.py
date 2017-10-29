from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from checker import checker

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildthatblog@localhost:8888/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

#blogs = []

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(5000))

    def __init__(self, name, body):
        self.name = name
        self.body = body


@app.route('/blog', methods=['POST', 'GET'])
def bloglist():

    if Blog.query.count() and request.args.get('id'):
        blogID = request.args.get('id')
        theBlog = Blog.query.get(blogID)
        return render_template('singleblog.html',title="Build-A-Blog!",blog=theBlog)
    else:
        blogs = Blog.query.all()
        return render_template('bloglist.html',title="Build-A-Blog!",blogs=blogs)


@app.route('/newpost',methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':
        blog_name = request.form['blogname']
        blog_body = request.form['blogbody']

        checkvals = checker(blog_name,blog_body)

        if checkvals["error"]:
            return render_template('newblog.html',title="Build-A-Blog!",blogtitle=blog_name,blogbody=blog_body,nameerror=checkvals["nameerror"],blogerror=checkvals["blogerror"])
        else:
            new_blog = Blog(blog_name, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            return redirect ('/blog?id={}'.format(new_blog.id))

    return render_template('newblog.html',title="Build-A-Blog!",blogtitle="",blogbody="",nameerror="",blogerror="")


if __name__ == '__main__':
    app.run()