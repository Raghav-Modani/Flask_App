from flask import Flask,request,render_template,flash
from flask.helpers import flash
from flask_login.utils import logout_user
from werkzeug.utils import redirect
from .models import db,login,Users,Posts
from flask_login import login_required,current_user,login_user

app = Flask(__name__)
app.secret_key='secret'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'

db.init_app(app)
login.init_app(app)
login.login_view='signin'


@app.before_first_request
def create_table():
    db.create_all()

@app.route("/")
def index():
    return render_template('index.html',loggedin=current_user)

@app.route("/signin",methods=['POST','GET'])
def signin():
    if current_user.is_authenticated:
        return redirect('/dashboard')
    if request.method=='POST':
        email=request.form['email']
        user=Users.query.filter_by(email=email).first()
        if user is not None and Users.check_password(user,request.form.get('password')):
            login_user(user)
            return redirect('/dashboard')

    return render_template('sign_in.html',loggedin=current_user)



@app.route("/signup",methods=['POST','GET'])
def signup():
    if current_user.is_authenticated:
        return redirect('/dashboard')
    
    if request.method=='POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        
        # print(email,name,password)

        if Users.query.filter_by(email=email).first():
            flash('Email already present',category='error')
            return render_template('sign_up.html',loggedin=current_user)


        user=Users(email=email,username=name,password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/signin')

        

    return render_template('sign_up.html',loggedin=current_user)


@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')



@app.route("/dashboard")
@login_required
def dashboard():
    posts=Posts.query.filter_by(author=current_user.id).all()
    return render_template('dashboard.html',loggedin=current_user,posts=posts)

@app.route("/createpost",methods=['GET','POST'])
@login_required
def createpost():
    if request.method=='POST':
        title=request.form.get('title')
        content=request.form.get('content')
        post=Posts(title=title,text=content,author=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Created Successfully',category='success')
        return redirect('/dashboard')

    return render_template('create_post.html',loggedin=current_user)


@app.route("/deletepost/<id>")
@login_required
def deletepost(id):
    post=Posts.query.filter_by(id=id).first()
    if post:
        db.session.delete(post)
        db.session.commit()
        flash('Blog Deleted Successfully',category='success')

    posts=Posts.query.filter_by(author=current_user.id).all()

    return render_template('dashboard.html',loggedin=current_user,posts=posts)

@app.route("/editpost/<id>",methods=['GET','POST'])
@login_required
def editpost(id):
    post=Posts.query.filter_by(id=id).first()
    if request.method=='POST':
        post.title=request.form.get('title')
        post.text=request.form.get('content')
        db.session.commit()
        flash('Blog Edited Successfully',category='success')
        return redirect('/dashboard')


    return render_template('edit_post.html',loggedin=current_user,post=post)


if __name__=="__main__":
    app.run(debug=True)
