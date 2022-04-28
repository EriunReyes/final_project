from flask import render_template, session,flash,redirect, request
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user import User
from flask_app.models.message import Message

@app.route('/messages')
def render_messages():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    user = User.get_one(data)
    users = User.get_all()
    messages = Message.get_user_messages(data)
    return render_template("messages.html", user=user, users=users, messages=messages)


@app.route('/post_message',methods=['POST'])  #checks if user is logged in
def post_message():
    if 'user_id' not in session:
        return redirect('/')
    if not Message.validate_message(request.form):
        return redirect('/messages')
    print("A")
    print(request.form)
    data = {
        "sender_id":  request.form['sender_id'], #foreign keys
        "receiver_id" : request.form['receiver_id'], #foreign keys
        "content": request.form['content']
    }
    print("B")
    Message.save(data)  #sends message to user
    print("C")
    return redirect('/messages')

@app.route('/destroy/message/<int:id>')  #deletes messages
def destroy_message(id):
    data = {
        "id": id
    }
    Message.destroy(data)
    return redirect('/messages')