from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
import math

class Message:
    db = 'final_project'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.content = db_data['content']
        self.sender_id = db_data['sender_id']
        self.sender = db_data['sender']
        self.receiver_id = db_data['receiver_id']
        self.receiver = db_data['receiver']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    def time_span(self):
        now = datetime.now()
        delta = now - self.created_at
        print(delta.days)
        print(delta.total_seconds())
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"

    @classmethod
    def get_user_messages(cls,data):
        query = "SELECT users.first_name as sender, user2.first_name as receiver, messages.* FROM users INNER JOIN messages ON users.id = messages.sender_id INNER JOIN users as user2 ON user2.id = messages.receiver_id WHERE user2.id =  %(id)s"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        messages = []
        for message in results:
            print(message)
            messages.append( cls(message) )
        return messages

    @classmethod
    def save(cls,data):
        query = "INSERT INTO messages (content,sender_id,receiver_id) VALUES (%(content)s,%(sender_id)s,%(receiver_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM messages WHERE messages.id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod #This method is static and it's not alterable by @classmethod/Using validations through Conditionals
    def validate_message(message):
        is_valid = True # we assume this is true
        if "content" not in message:
            is_valid = False
            flash("Please enter a message", 'message')
        if len(message["content"]) == 0:
            is_valid = False
            flash("Please enter a message", 'message')
        return is_valid