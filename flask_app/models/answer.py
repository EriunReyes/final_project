from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
import math
from flask import flash


class Answer:
    db = 'final_project'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.content = db_data['content']
        self.user_id = db_data['user_id']
        self.question_id = db_data['question_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod  #method to get the specific question from the query
    def get_by_question(cls, data):
        query = 'SELECT * FROM answers WHERE question_id = %(question_id)s;'
        result = connectToMySQL(cls.db).query_db(query, data)
        #Didn't find a matching user
        answer = []
        for row in result:
            print(row)
            answer.append(cls(row))
        return answer

    @classmethod
    def save(cls,data):
        query = "INSERT INTO answers (content, user_id, question_id) VALUES (%(content)s,%(user_id)s, %(question_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod  #This method get all the users columns from the db
    def get_all(cls):
        query = 'SELECT * FROM answers;'
        result = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in result:
            users.append(cls(row))
        return users


    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM answers WHERE answer.id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod #This method is static and it's not alterable by @classmethod/Using validations through Conditionals
    def validate_answer(answer):
        is_valid = True # we assume this is true
        if len(answer["content"]) == 0:
            is_valid = False
            flash("Please enter an answer", 'answer')
        return is_valid