from flask_app import app
from flask import render_template, request,redirect,flash,session
from flask_app.models import user,liter
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dash():
    user_from_db=user.User.get_by_id({"id":int(session['logged_in'])})
    all_litters = liter.Litters.get_all()
    return render_template('dashboard.html', user=user_from_db, all_litters=all_litters)

@app.route('/register', methods=['POST'])
def register():
    if not user.User.is_valid(request.form):
        return redirect('/login')
    else:
        data = {
            "name":request.form['name'],
            "email":request.form['email'],
            "password": bcrypt.generate_password_hash(request.form['password'])
        }
        
        user.User.create(data)
    
    return redirect('/dashboard')

@app.route('/user/login', methods=['POST'])
def user_login():
    data={
        'email':request.form['email']
    }
    
    user_from_db=user.User.get_by_email(data)
    if not user_from_db:
        flash('this is not you')
        return redirect('/login')
    if not bcrypt.check_password_hash(user_from_db.password, request.form['pwd']):
        flash('Invalid login')
        return redirect('/login')
    session['logged_in'] = user_from_db.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

