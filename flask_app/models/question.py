from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
import math

class Question:
    db = 'final_project'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.content = db_data['content']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod  #This method get all the users columns from the db
    def get_all(cls):
        query = 'SELECT * FROM questions;'
        result = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in result:
            users.append(cls(row))
        return users

    @classmethod
    def get_by_userid(cls, id):
        query = 'SELECT * FROM questions WHERE user_id = %(id)s;'
        data = {
            "id": id
        }
        result = connectToMySQL(cls.db).query_db(query, data)
        users = []
        for row in result:
            users.append(cls(row))
        return users

    @classmethod
    def get_by_id(cls, id):
        query = 'SELECT * FROM questions WHERE id = %(id)s;'
        data = {
            "id": id
        }
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) > 0:
            return cls(results[0])
        else:
            return None

    @classmethod
    def save(cls,data):
        query = "INSERT INTO questions (content,user_id) VALUES (%(content)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def edit(cls, data):
        query = "UPDATE questions set content = %(content)s WHERE id = %(id)s"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query1 = """SET FOREIGN_KEY_CHECKS = 0;"""
        query2 = 'DELETE FROM questions WHERE questions.id = %(id)s;'
        connectToMySQL(cls.db).query_db(query1,data)
        return connectToMySQL(cls.db).query_db(query2,data)

    @staticmethod #This method is static and it's not alterable by @classmethod/Using validations through Conditionals
    def validate_question(question):
        is_valid = True # we assume this is true
        if len(question["content"]) == 0:
            is_valid = False
            flash("Please enter a question", 'question')
        return is_valid