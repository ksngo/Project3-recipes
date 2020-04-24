from flask import Flask, render_template, request, redirect, url_for
import os 
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.environ.get('MONGO_URI')
print(MONGO_URI)
DB_NAME ='project3'

client =pymongo.MongoClient(MONGO_URI)

app = Flask(__name__)

@app.route('/')
def show_recipes():

    get_recipes = client[DB_NAME].recipes.find()

    return render_template('index.html', get_recipes = get_recipes)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)

