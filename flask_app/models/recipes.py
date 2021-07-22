from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.users import User

import re

class Recipe():
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.under = data['under']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.user = []

    @classmethod
    def new_recipe(cls,data):
        query = 'INSERT INTO recipes(name, description, instructions, date, under, users_id) VALUES(%(name)s, %(description)s, %(instructions)s, %(date)s, %(under)s, %(users_id)s);'

        results = connectToMySQL('recipe_site').query_db(query,data)

        return results

    @classmethod
    def get_recipe_by_id(cls,data):
        query = 'SELECT * FROM recipes WHERE id = %(id)s;'

        results = connectToMySQL('recipe_site').query_db(query,data)

        single_recipe = cls(results[0])

        return single_recipe

    @classmethod
    def get_all_recipes(cls):
        query = 'SELECT * FROM recipes JOIN users ON users.id = recipes.users_id;'

        results = connectToMySQL('recipe_site').query_db(query)

        recipes =[]

        for recipe in results:
            show = cls(recipe)
            user_data = {
                'id': recipe['id'],
                'first_name': recipe['first_name'],
                'last_name': recipe['last_name'],
                'email': recipe['email'],
                'password': recipe['password'],
                'created_at': recipe['created_at'],
                'updated_at': recipe['updated_at']
            }
            show.user = User(user_data)
            recipes.append(show)
        
        return recipes

    @classmethod
    def delete_recipe(cls,data):
        query = 'DELETE FROM recipes WHERE id = %(id)s;'

        results = connectToMySQL('recipe_site').query_db(query,data)

    @classmethod
    def update_recipe(cls,data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date = %(date)s, under = %(under)s, users_id = %(users_id)s WHERE id = %(id)s"

        results = connectToMySQL('recipe_site').query_db(query,data)

        return results

    @staticmethod
    def validate_recipe(user):
        is_valid=True

        if len(user['name']) < 3:
            flash('The name needs to be at least 3 characters long')
            is_valid= False

        if len(user['description']) < 3:
            flash('The description needs to be at least 3 characters long')
            is_valid= False

        if len(user['instructions']) < 3:
            flash('The instructions needs to be at least 3 characters long')
            is_valid= False
        

        if len(user['date']) == 0:
            flash('Please select a date')
            is_valid - False
        
        return is_valid