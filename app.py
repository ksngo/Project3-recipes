from flask import Flask, render_template, request, redirect, url_for
import os 
import pymongo
import datetime
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


# @app.route('/<username>/add_recipe/')
# def add_recipe (username) :

#     username=username

#     return render_template('add_my_recipe.html', username=username)



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

@app.route('/recipes/<recipe_id>/')
def recipe_display(recipe_id):

    #####get object type recipe document base on given recipe_id#####
    get_recipe = client[DB_NAME].recipes.find_one({'_id': ObjectId(recipe_id)})

    #####prepare a lists from 0 to variable wher variable is number of steps in recipe####### 
    recipe_steps_num_list= list(range(0,len(get_recipe['steps'])))

    #####get object type user document base on the recipe's user_id######
    get_creator = client[DB_NAME].users.find_one({'_id' : ObjectId(get_recipe['user_id'])})
    
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

    ######prepare a lists from 0 to variable where variable is number of recipes for the creator#####
    # creator_recipes_num_list = list(range(0,len(recipes_id_list_names)))

    print('^^^^^^^^^^^^^^^^whole lists:' , recipes_id_list_names)
    print('-------------------------')

    ######find the average likes#####
    sum_likes = 0

    for i in get_recipe['likes'] :
        sum_likes = sum_likes+int(i['ratings'])
        
    avg_likes = sum_likes / len(get_recipe['likes'])

    return render_template('public_recipe.html', get_recipe=get_recipe, recipe_steps_num_list=recipe_steps_num_list, get_creator=get_creator, recipes_id_list_names=recipes_id_list_names, avg_likes=avg_likes)


@app.route('/<user_id>/')
def account(user_id):

    get_user = client[DB_NAME].users.find_one({'_id': ObjectId(user_id)})

    return render_template('my_account.html', get_user=get_user)

@app.route('/<user_id>/' , methods=['POST'])
def update_account(user_id):
    
    user_name = request.form.get('user-name')
    print('------------------------', user_name)

    client[DB_NAME].users.update_one({
        '_id':ObjectId(user_id)
    }, {
        "$set": {
            'user_name' : request.form.get('user-name'),
            'password' : request.form.get('password'),
            'email' : request.form.get('email'),
            'country' : request.form.get('country'),
            'birthday' : request.form.get('birthday'),
            'ethnicity' : request.form.get('ethnic')
        }
    })

    return redirect(url_for('account', user_id=user_id))

@app.route('/<user_id>/my_recipes/')
def my_recipes(user_id):

    get_my_recipes = list(client[DB_NAME].recipes.find({'user_id': user_id}))

    num_of_recipes = len(get_my_recipes)

    recipes_avg_ratings_list =[]

    #####prepare average ratings for each recipe stored in a list######
    for x in range(num_of_recipes):
        recipe_id=get_my_recipes[x]['_id']
        recipe_avg_rating=find_recipe_avg_rating(recipe_id)
        recipes_avg_ratings_list.append(recipe_avg_rating)

    return render_template('my_recipes.html', get_my_recipes=get_my_recipes, recipes_avg_ratings_list=recipes_avg_ratings_list, user_id=user_id )


@app.route('/<user_id>/my_recipes/<recipe_id>')
def edit_recipe(user_id, recipe_id):

    get_recipe = client[DB_NAME].recipes.find_one({'_id':ObjectId(recipe_id)})

    #####prepare a lists from 0 to variable wher variable is number of steps in recipe####### 
    recipe_steps_num_list= list(range(0,len(get_recipe['steps'])))  




    return render_template("edit_recipe.html", get_recipe=get_recipe, recipe_steps_num_list=recipe_steps_num_list )


@app.route('/<user_id>/my_recipes/<recipe_id>', methods=['POST'])
def update_recipe(user_id, recipe_id):
    
    ######retrieves the number of recipe steps from user post######
    x= request.form.get("num-steps") 
    
    steps_list=[]
    ing_list=[]
    tools_list=[]

    for i in range(0,int(x)) :
        steps_list.append(request.form.get("step-"+str(i)))
        ing_list.append(request.form.get("ing-"+str(i)))
        tools_list.append(request.form.get("tools-"+str(i)))
    

    client[DB_NAME].recipes.update({'_id': ObjectId(recipe_id)},{

        '$set' : {
            "recipe_name" :  request.form.get("recipe-name"),
            "steps" : steps_list,
            "ingredients" : ing_list,
            "tools" : tools_list,
            "cuisine" : request.form.get("cuisine"),
            "my_rating" : request.form.get("my-rating"),
            "number_steps" : request.form.get( "num-steps"),
            "date_last_edited" : datetime.datetime.now().strftime("%Y-%m-%d")
        }
    })

    return redirect(url_for("my_recipes", user_id=user_id))


@app.route("/<user_id>/add_recipe")
def add_recipe(user_id) :


    return render_template("add_recipe.html")

@app.route("/<user_id>/add_recipe", methods=["POST"])
def add_recipe_post(user_id) :

    num_steps = request.form.get("num-steps-np")

    steps_list=[]
    ing_list=[]
    tools_list=[]
    photos_list=[]
    likes_list=[]

    for i in range(0, int(num_steps)):
        steps_list.append(request.form.get("step-"+str(i)))
        ing_list.append(request.form.get("ing-"+str(i)))
        tools_list.append(request.form.get("tools-"+str(i)))

    client[DB_NAME].recipes.insert_one({
        "_id" : ObjectId(),
        "recipe_name" : request.form.get("recipe-name"),
        "steps" : steps_list,
        "ingredients" : ing_list,
        "tools" : tools_list,
        "cuisine" : request.form.get("cuisine"),
        "photos" : photos_list,
        "my_rating" : request.form.get("my-rating"),
        "likes" : likes_list,
        "user_id" : user_id,
        "date_posted" : datetime.datetime.now().strftime("%Y-%m-%d"),
        "date_last_edited": "null",
        "number_steps" : request.form.get("num-steps-np")
    })

    return redirect(url_for("my_recipes", user_id=user_id ))

######################################################################    
######--------------------------functions----------------------#######
######################################################################

def find_recipe_name (recipe_id) :
    
    recipe_name = client[DB_NAME].recipes.find_one({'_id':ObjectId(recipe_id)}, {'recipe_name':1})['recipe_name']
    print (recipe_name)

    return recipe_name

def find_recipe_avg_rating (recipe_id) :

    get_my_recipe = client[DB_NAME].recipes.find_one({'_id': ObjectId(recipe_id)})
    
    number_of_ratings = len(get_my_recipe['likes'])

    if (number_of_ratings > 0) :
        rating_sum = 0
        for x in range(number_of_ratings):
            rating_sum = rating_sum + int(get_my_recipe['likes'][x]['ratings'])
    
        recipe_avg_rating = rating_sum / number_of_ratings
    else:

        recipe_avg_rating ="null"


    return recipe_avg_rating




if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)

