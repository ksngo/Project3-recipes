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

    return render_template('public_all_recipes.html', results=get_recipes )




if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)

