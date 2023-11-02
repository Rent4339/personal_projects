from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import liter,user
from flask import flash
from pprint import pprint


class Litters:
    db = "puppy"
    def __init__(self,data):
        self.id = data['id']
        self.breed = data['breed']
        self.quantity = data['quantity']
        self.home = data['home']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None
        
    @classmethod
    def get_all(cls):
        query = '''
            SELECT * FROM litters;
        '''
        
        results = connectToMySQL(cls.db).query_db(query)
        all_litters = []
        
        for row in results:
            all_litters.append(cls(row))
            
        return all_litters
    
    @classmethod
    def get_one(cls,data):
        query= '''
            SELECT * FROM litters
            LEFT JOIN users on users.id = litters.user_id
            WHERE litters.id = %(id)s;
        '''
        results = connectToMySQL(cls.db).query_db(query,data)
        pprint (results)
        row = results[0]
        one_liter = cls(row)
        user_data = {
            "id" : row['users.id'],
            "name" : row['name'],
            "email" : row['email'],
            "password" : row['password'],
            "created_at" : row['users.created_at'],
            "updated_at" : row['users.updated_at'],
        }
        one_liter.creator = user.User(user_data)
        pprint (user_data)
        return one_liter
    
    @classmethod
    def create(cls,data):
        query = '''
            INSERT INTO litters(breed,quantity,home,description,user_id)
            VALUES (%(breed)s,%(quantity)s,%(home)s,%(description)s,%(user_id)s);
        '''
        
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query='''
            DELETE FROM litters
            WHERE id = %(id)s;
        '''
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def update(cls,data):
        query='''
            UPDATE litters
            SET breed = %(breed)s, quantity = %(quantity)s, home = %(home)s, description = %(description)s
            WHERE id = %(id)s;
        '''
        return connectToMySQL(cls.db).query_db(query,data)
    
    @staticmethod
    def is_valid(liter):
        is_valid = True
        
        if len(liter['breed']) < 2:
            is_valid = False
            flash('Breed must be longer than 2 charecters')
        if len(liter['quantity']) < 0:
            is_valid = False
            flash('Qantity must be more than 0')
        if len(liter['home']) < 0:
            is_valid = False
            flash('Qantity must be more than 0')
        if len(liter['description']) < 10:
            is_valid = False
            flash('Description must be more than 10 charecters')
        return is_valid