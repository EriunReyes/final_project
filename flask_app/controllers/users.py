from flask_app import app
import requests
from flask import render_template,request,session,redirect,flash       
from flask_app.models.user import User       
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def login_reg():
    return render_template('registration.html')

@app.route('/loginn')
def login_template():
    return render_template('login.html')

@app.route('/register_user', methods=['POST'])
def register_user():
    if not User.validate_user(request.form):
        return redirect('/')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = User.save(data)
    session['user_id'] = user_id 
    return redirect('/dashboard')


@app.route('/login', methods=['POST']) #Gets a form with the login information
def login():
    user_in_db = User.get_by_email(request.form) #Requesting the specific email 
    if not user_in_db: #If the email method is not in, flash
        flash('Invalid Email/Password', 'login')
        return redirect('/loginn')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password', 'login')
        return redirect('/loginn')
    session['user_id'] = user_in_db.id   
    return redirect('/dashboard')  


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/') 
    data = {
        'id': session['user_id']
    }
    user = User.get_one(data)
    users = User.get_all()
    return render_template('dashboard.html', user = user, users = users)

@app.route('/community')
def community():
    if 'user_id' not in session:
        return redirect('/') 
    data = {
        'id': session['user_id']
    }
    users = User.get_all()
    return render_template('community.html', users = users)

# About Us Route 
@app.route('/contact')
def contact():
    return render_template('contact_us.html')

@app.route('/add_user')
def create():
    return render_template('create.html')

# coding.template
@app.route('/coding')
def coding():
    return render_template('coding.html')


@app.route('/create_user', methods=['POST'])
def create_form():
    User.savde(request.form)
    print(request.form)
    return redirect('/community')


@app.route('/user/read_on/<int:id>') #Gets one user
def read_one(id):
    data = {
        'id': id
    }
    return render_template('read_one.html',user=User.get_one(data)) 

@app.route('/user/edit/<int:id>')
def edit(id):
    data = {
        'id': id
    }
    return render_template('edit.html', user = User.get_one(data))


@app.route('/user/update', methods=['POST'])
def update():
    User.update(request.form)
    return redirect('/community')

@app.route('/show/likes/<int:user_id>')
def likes(user_id):
    likes_data = {
        'user_id': session['user_id'],
    }
    likes = User.create_likes(likes_data)
    return redirect('/dashboard')


@app.route('/show/unlikes/<int:user_id>')
def unlikes(user_id):
    likes_data = {
        'user_id': session['user_id'],
    }
    likes = User.delete_likes(likes_data)
    return redirect('/dashboard')



@app.route('/delete/<int:id>')
def delete(id):
    data = {
        'id':id
    }
    User.delete(data)
    return redirect('/community')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# API
@app.route('/api')
def api():
    return render_template('api.html')


@app.route('/get_user', methods=['POST'])
def api_form():
    user = request.form['user']
    url = f'https://swapi.dev/api/people/{user}'
    response = requests.get(url)
    # print(response.json()['name'])
    session['name'] = response.json()['name']
    session['height'] = response.json()['height']
    return redirect('/api')
