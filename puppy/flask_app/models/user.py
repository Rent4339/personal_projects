from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db="puppy"
    def __init__(self,data):
        self.id=data['id']
        self.name=data['name']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.litters=[]
        
    @classmethod
    def create(cls,data):
        query='''
            INSERT INTO users(name,email,password)
            VALUES(%(name)s,%(email)s,%(password)s)
        '''
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def get_by_email(cls,data):
        query='''
            SELECT * FROM users
            WHERE email= %(email)s;
        '''
        results=connectToMySQL(cls.db).query_db(query,data)
        
        if results:
            user_from_db = results[0]
            return cls(user_from_db)
        else:
            return False
        
    @classmethod
    def get_by_id(cls,data):
        query='''
            SELECT * FROM users
            WHERE id = %(id)s;
        '''
        results=connectToMySQL(cls.db).query_db(query,data)
        
        if results:
            user_from_db = results[0]
            return cls(user_from_db)
        else:
            return False
        
    
    
    @staticmethod
    def is_valid(user):
        is_valid = True
        
        if len(user['name']) < 2:
            is_valid = False
            flash('Name must be longer than 2 charecters')
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email address')
        if len(user['password']) < 6:
            is_valid = False
            flash('Password must be longer than 6 charecters')
        if user['password_confirmation'] != user['password']:
            is_valid = False
            flash('Password must match')
        return is_valid