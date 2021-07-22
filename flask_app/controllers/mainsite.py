from flask_app import app
from flask import render_template, redirect, session, request,flash
from flask_app.models.recipes import Recipe
from flask_app.models.users import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('You must be logged in to see this page')
        return redirect('/')
    all_recipes = Recipe.get_all_recipes()
    return render_template('dashboard.html', all_recipes = all_recipes)

@app.route('/create_recipe')
def create_recipe():
    if 'user_id' not in session:
        flash('You must be logged in to see this page')
        return redirect('/')
    return render_template('create_recipe.html')

@app.route('/new_recipe', methods=["POST"])
def new_recipe():
    if 'user_id' not in session:
        flash('You must be logged in to see this page')
        return redirect('/')
    print(request.form)
    if Recipe.validate_recipe(request.form) == False:
        return redirect("/create_recipe")
    data={
        'name':request.form['name'],
        'description':request.form['description'],
        'date':request.form['date'],
        'under':request.form['under'],
        'instructions':request.form['instructions'],
        'users_id':session['user_id'],
    }
    new_recipe = Recipe.new_recipe(data)

    return redirect(f"/dashboard")

@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    if 'user_id' not in session:
        flash('You must be logged in to see this page')
        return redirect('/')

    data={
        'id': recipe_id
    }
    single_recipe = Recipe.get_recipe_by_id(data)

    return render_template('recipe.html', single_recipe = single_recipe)

@app.route('/delete_recipe/<int:recipe_id>')
def delete_recipe(recipe_id):

    data ={
        'id': recipe_id
    }

    Recipe.delete_recipe(data)

    return redirect('/dashboard')

@app.route('/edit_recipe/<int:recipe_id>')
def edit_recipe(recipe_id):
    if 'user_id' not in session:
        flash('You must be logged in to see this page')
        return redirect('/')

    data = {
        'id':recipe_id
    }

    single_recipe = Recipe.get_recipe_by_id(data)

    if session['user_id'] != single_recipe.users_id:
        return redirect(f'/recipe/{recipe_id}')

    return render_template('edit.html', single_recipe = single_recipe)


@app.route('/update_recipe/<int:recipe_id>', methods=["POST"])
def update_recipe(recipe_id):

    if Recipe.validate_recipe(request.form) == False:
        return redirect(f"/edit_recipe/{recipe_id}")

    data={
        'id':recipe_id,
        'name':request.form['name'],
        'description':request.form['description'],
        'date':request.form['date'],
        'under':request.form['under'],
        'instructions':request.form['instructions'],
        'users_id':session['user_id']
    }
    Recipe.update_recipe(data)
    return redirect('/dashboard')