# from flask import Flask, render_template, request, redirect, url_for, flash
# import os 
# import pymongo
# import datetime
# from bson.objectid import ObjectId
# from dotenv import load_dotenv
# from jinja2 import Template
# load_dotenv()

# MONGO_URI = os.environ.get('MONGO_URI')
# # print(MONGO_URI)
# DB_NAME ='project3'

# client =pymongo.MongoClient(MONGO_URI)

# app = Flask(__name__)
# app.secret_key = "secret key"

# @app.route("/recipes/filter_by_date/")
# def filter_date() :

#     get_filter_date = client[DB_NAME].recipes.find().sort( "date_posted" , -1)
#     get_users = list(client[DB_NAME].users.find())

#     return render_template("public_all_recipes_filter_date.html", get_filter_date =get_filter_date , get_users=get_users)


# if __name__ == '__main__':
#     app.run(host=os.environ.get('IP'),
#             port=int(os.environ.get('PORT')),
#             debug=True)
