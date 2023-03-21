from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import magazine

from flask_app import DATABASE
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User :
    def __init__(self, data) :
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.magazines=[]

#                     QUERIES                        

#          Add user to the database
    @classmethod
    def create_user(cls,data):
        query = """
        INSERT INTO users (first_name, last_name, email, password) 
        VALUES  (%(first_name)s, %(last_name)s,%(email)s, %(password)s) ;
        """
        return connectToMySQL(DATABASE).query_db(query,data)
        
        #      get one user by his email
    @classmethod
    def get_by_email(cls, data):
        query = """
            SELECT * FROM users WHERE email = %(email)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results)<1:
            return False
        return cls(results[0])
        
        #     get one user by  his id
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s; "
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results)<1:
            return False
        return cls(results[0])

    @classmethod
    def update_user(cls,data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s ;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_user_magazines(cls, data ):
        query = "SELECT * FROM users LEFT JOIN magazines ON users.id = magazines.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        print(results)
        user = cls(results[0])
        for row in results:
            m = {
                'id': row['magazines.id'],
                'user_id': row['user_id'],
                'name': row['name'],
                'description': row['description'],
                'subscriber': row['subscriber'],
                'created_at': row['magazines.created_at'],
                'updated_at': row['magazines.updated_at']
            }
            user.magazines.append(magazine.Magazine(m))
        return user.magazines

    

    #               VALIDATIONS
    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['first_name'])<3:
            flash("First Name must be at least 3 characters","register")
            is_valid = False
        if len(data['last_name'])<3:
            flash("Last Name must be at least 3 characters" ,"register")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!" ,"register")
            is_valid = False,
        elif User.get_by_email({'email':data['email']}):
            flash("Email already exist","register")
            is_valid = False
        if len(data['password'])<8:
            is_valid = False
            flash("Password must be more than 8" ,"register")
        elif data["confirm_password"] != data["password"]:
            is_valid = False
            flash("Password and Confirm Password must match","register")
        return is_valid

    def update_validate(data):
        is_valid = True
        if len(data['first_name'])<3:
            flash("First Name must be at least 3 characters")
            is_valid = False
        if len(data['last_name'])<3:
            flash("Last Name must be at least 3 characters")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!")
            is_valid = False
        return is_valid