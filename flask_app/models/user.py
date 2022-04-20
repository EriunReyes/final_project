from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
db = 'belt_db'
class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod # this method should insert all my information from users to the database
    def save(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        return connectToMySQL(db).query_db(query, data)



    @classmethod  #This method get all the users columns from the db
    def get_all(cls):
        query = 'SELECT * FROM users;'
        result = connectToMySQL(db).query_db(query)
        users = []
        for row in result:
            users.append(cls(row))
        return users


    @classmethod  #method to get the specific email from the query
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = connectToMySQL(db).query_db(query, data)
        #Didn't find a matching user
        print(result)
        if len(result) < 1:
            return False
        return cls(result[0]) #It is found and return the query


    @classmethod #returns the id number from the users table
    def get_one(cls, data): 
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        if len(results) < 1:
            return False
        return cls(results[0])


    @classmethod  #This method should updated the columns from my users table
    def update(cls, data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)


    @classmethod #This method should delete the specific id  from my users table
    def delete(cls, data):
        query='DELETE FROM users WHERE id = %(id)s;'
        return connectToMySQL(db).query_db(query, data)


    @staticmethod #This method is static and it's not alterable by @classmethod/Using validations through Conditionals
    def validate_user(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 3:
            flash("first name must be at least 3 characters.", 'register_user')
            is_valid = False
        if len(user['last_name']) < 3:
            flash("last name must be at least 3 characters.", 'register_user')
            is_valid = False
        if len(user['email']) < 3:
            flash("email must be at least 3 characters.", 'register_user')
            is_valid = False
        query = 'SELECT * FROM users WHERE email= %(email)s;'  #this specify the email from our query
        results = connectToMySQL(db).query_db(query, user)   
        if not EMAIL_REGEX.match(user['email']):           #if the email.regex thoses not match with the input.->A flash will show up
            flash('Invalid email address', ' register_user')                  
            is_valid = False 

        if len(results) >= 1:
            flash('This email is already taken', 'register_user')
            is_valid = False

        if len(user['password']) < 8:
            flash("password must be at least 8 characters.", 'register_user')
            is_valid = False

        if re.search('[0-9]',user['password']) is None:   #if an integer is not in->Will flash an error.
            flash("Make sure your password has a number in it", 'register_user')
            is_valid = False

        # if re.search('[A-Z]', user['password']) is None: #If there's not uppercase->will flash an error.
        #     flash('Make sure you enter upper case a letter', ' register_user')
        #     is_valid = False

        if user['password'] != user['confirm_password']: # If password is not the same as confirm_password.-> return a flash message
            flash("Passwords don't match","register_user")
            is_valid = False
        return is_valid  # If all this True.->No validation should show up.


