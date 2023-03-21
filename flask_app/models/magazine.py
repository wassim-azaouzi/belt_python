from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

from flask_app import DATABASE


class Magazine :
    def __init__(self, data) :
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.subscriber = data['subscriber']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner = user.User.get_by_id({'id':self.user_id})
        self.users=[]

        # --        QUERIES                        

        #        insert new magazine into the database
    @classmethod
    def create_magazine(cls,data):
        query = """
            INSERT INTO magazines (user_id,name, description, subscriber) 
            VALUES  (%(user_id)s,%(name)s, %(description)s, 0) ;
        """
        return connectToMySQL(DATABASE).query_db(query,data)


#                 get all magazines 
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM magazines LEFT JOIN users ON users.id= magazines.user_id; "
        results = connectToMySQL(DATABASE).query_db(query)
        recipes= []
        for row in results:
            m={
                'id': row['id'],
                'name': row['name'],
                'first_name': row['first_name'],
            }
            recipes.append(m)
        return recipes

#             get magazine by its id
    @classmethod
    def get_by_id(cls, data):
        query = """
            SELECT * FROM magazines 
            WHERE id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        print(results)
        if len(results)<1:
            return False
        return cls(results[0])

#             get subscriber by id
    @classmethod
    def get_by_ids(cls, data):
        query = """
            SELECT * FROM subscribers 
            WHERE user_id = %(user_id)s and magazine_id=%(magazine_id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        print(results)
        if len(results)<1:
            return False
        return True


#              get all subscribers of a magazine
    @classmethod
    def get_magazine_subscribers(cls, data ):
        query = """
        SELECT * FROM magazines 
        LEFT JOIN subscribers ON magazines.id = subscribers.magazine_id  
        LEFT JOIN users ON users.id = subscribers.user_id WHERE  magazines.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        print(results)
        magazine = cls(results[0])
        for row in results:
            s = {
                'id': row['id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
            }
            magazine.users.append(user.User(s))
        return magazine.users

#               delete a magazine
    @classmethod
    def delete_subscribers(cls, data):
        query = """ 
        DELETE FROM subscribers WHERE magazine_id=%(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def delete_magazines(cls, data):
        query = """ 
        DELETE FROM magazines WHERE id=%(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)


#               add a subscriber to a magazine
    @classmethod
    def subscribe(cls, data):
        query = """ 
        INSERT INTO subscribers (user_id, magazine_id)
        VALUES (%(user_id)s, %(magazine_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def subscribe_count(cls, data):
        query = """ 
        UPDATE magazines SET subscriber= subscriber+1
        WHERE id=%(magazine_id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)

    #               VALIDATIONS
    @staticmethod
    def mag_validate(data):
        is_valid = True
        if len(data['name'])<2:
            flash("Title must be at least 2 characters")
            is_valid = False
        if len(data['description'])<10:
            flash("Description must be at least 10 characters" )
            is_valid = False
        return is_valid

    @staticmethod
    def subscribe_validate(data):
        is_valid = True
        if Magazine.get_by_ids(data):
            is_valid = False
        return is_valid



