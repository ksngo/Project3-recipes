from flask import Flask, render_template, request, redirect, url_for
import os 
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
from jinja2 import Template
load_dotenv()

MONGO_URI = os.environ.get('MONGO_URI')
print(MONGO_URI)
DB_NAME ='project3'

client =pymongo.MongoClient(MONGO_URI)

app = Flask(__name__)

@app.route('/')
def index():

    get_recipes = client[DB_NAME].recipes.find()

    return render_template('index.html', get_recipes = get_recipes)


@app.route('/<username>/add_recipe/')
def add_recipe(username) :

    username=username

    return render_template('add_my_recipe.html', username=username)



@app.route('/recipes/')
def recipes():

    get_recipes = client[DB_NAME].recipes.find()
    get_users = list(client[DB_NAME].users.find())
    
    
    
    # get_average_likes = client[DB_NAME].recipes.aggregate(
    #     [
    #         {
    #          $group:
    #             {
    #              _id: "$item",
    #              avglikes: {$avg: "$likes"}
    #             }
    #         }
    #     ]
    # )
    
    return render_template('public_all_recipes.html', get_recipes= get_recipes , get_users= get_users )

@app.route('/recipes/<recipe_id>')
def recipe_display(recipe_id):

    #####get object type recipe document base on given recipe_id#####
    get_recipe = client[DB_NAME].recipes.find_one({'_id': ObjectId(recipe_id)})
    #####prepare a lists from 0 to variable wher variable is number of steps in recipe####### 
    recipe_list= list(range(0,len(get_recipe['steps'])))
    #####get object type user document base on the recipe's user_id######
    get_creator = client[DB_NAME].users.find_one({'_id' : ObjectId(get_recipe['user_id'])})
    # creator_recipes_list = list(range(0,len(get_creator['my_recipes'])))

    ######store all the recipes id from the creator into a list##### 
    recipes_id_list =[]
    for r in get_creator['my_recipes'] :
        recipes_id_list.append(r)
        
    print(recipes_id_list)
    print('-------------------------')

    ######retrieve the recipes names into a list from the recipes id######
    recipes_id_list_names =[]
    for r in recipes_id_list :
        recipes_id_list_names.append(find_recipe_name(r))

    print(recipes_id_list_names)
    print('-------------------------')

    # print(results.recipe_name)
    # print(results['recipe_name'])
    # get_recipe = client[DB_NAME].recipes.find_one({ _id : recipe_id } )

    return render_template('public_recipe.html', get_recipe=get_recipe, recipe_list=recipe_list, get_creator=get_creator, recipes_id_list_names=recipes_id_list_names )

#----------------------------------------------------functions--------------------------------------------#

def find_recipe_name (recipe_id) :
    
    recipe_name = client[DB_NAME].recipes.find_one({'_id':ObjectId(recipe_id)}, {'recipe_name':1})
    print (recipe_name)

    return recipe_name

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)

