from crypt import methods
from flask import render_template, session,flash,redirect, request
import re
from flask_app import app
from flask_app.models.user import User
from flask_app.models.question import Question
from flask_app.models.answer import Answer


@app.route('/questions')
def render_questions():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    user = User.get_one(data)
    users = User.get_all()
    questions = Question.get_all()
    return render_template("questions.html", user=user, users=users, questions=questions)

@app.route('/questions/me')
def render_myquestions():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    user = User.get_one(data)
    users = User.get_all()
    questions = Question.get_by_userid(session["user_id"])
    return render_template("myquestion.html", user=user, users=users, questions=questions)


@app.route('/questions', methods = ['POST'])
def post_question():
    print(request)
    if 'user_id' not in session:
        return redirect('/')
    if not Question.validate_question(request.form):
        return redirect('/questions')
    data = {
        "content": request.form['content'],
        "user_id": session['user_id']
    }
    Question.save(data)
    return redirect('/questions')

@app.route('/questions/delete/<int:id>', methods = ['POST'])
def delete_question(id):
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "id": request.form['id']
    }
    Question.destroy(data)
    return redirect('/questions/me')

@app.route('/questions/edit', methods = ['POST'])
def edit_question():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "id": request.form['id'],
        "content": request.form['content']
    }
    Question.edit(data)
    return redirect('/questions/me')

@app.route('/single/<int:id>')
def render_single_question(id):
    if 'user_id' not in session:
        return redirect('/')
    question = Question.get_by_id(id)
    answers = Answer.get_by_question({
        "question_id": id
    })
    return render_template("singlequestion.html", question=question, answers=answers)

@app.route('/questions/answer', methods=['POST'])
def post_answer():
    if 'user_id' not in session:
        return redirect('/')
    if not Answer.validate_answer(request.form):
        return redirect('/questions')
    data = {
        "question_id": request.form['question_id'],
        "content": request.form['content'],
        "user_id": session['user_id']
    }
    Answer.save(data)
    Answer.destroy(data)
    return redirect('/questions' + data["question_id"])


# @app.route('/destroy/<int:id>')
# def destroy(id):
#     if 'user_id' not in session:
#         return redirect('/logout')
#     data = {
#         'id':id
#     }
#     Answer.destroy(data)
#     return redirect('/single/{{id}}')