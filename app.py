from flask import Flask, render_template, request, redirect, url_for, flash
import os
import pymongo
import datetime
import string
from bson.objectid import ObjectId
from dotenv import load_dotenv
from jinja2 import Template
load_dotenv()

MONGO_URI = os.environ.get('MONGO_URI')
# print(MONGO_URI)
DB_NAME = 'project3'

client = pymongo.MongoClient(MONGO_URI)

app = Flask(__name__)
app.secret_key = "secret key"

# ---------------------------------Index /Home page-----------------------------------------


@app.route('/')
def index():

    get_recipes = client[DB_NAME].recipes.find()
    return render_template('index.html', get_recipes=get_recipes)


# -------------------------------Public recipes page ---------------------------------------

@app.route('/recipes/')
def recipes():

    get_recipes = client[DB_NAME].recipes.find()
    get_users = list(client[DB_NAME].users.find())

    return render_template('public_all_recipes.html', get_recipes=get_recipes, get_users=get_users)

## ----------------------------Public recipes page POST --------------------------------

@app.route('/recipes/search/', methods=["POST"])
def recipes_search() :

    user_query = request.form.get("user_query")
    get_recipes = client[DB_NAME].recipes.find( {"$text" : { "$search" : user_query}})
    
    if user_query =="" :
        return redirect( url_for("recipes"))
    elif list(get_recipes) :
        flash("Search results for "+'"'+user_query+'"')
    else :
        flash("No results for "+'"'+user_query+'"')
        return redirect( url_for("recipes"))
        
    return redirect(url_for("recipes_search_results", user_query=user_query))

###---------------------------Display Search results --------------------------------------------

@app.route("/recipes/search/<user_query>")
def recipes_search_results( user_query) :

    
    get_recipes = client[DB_NAME].recipes.find( {"$text" : { "$search" : user_query}})
    get_users = list(client[DB_NAME].users.find())

    return render_template("search_recipes.html", get_recipes=get_recipes, get_users=get_users)

####-------------------------Public recipes page Frames view------------------------------------

@app.route("/recipes/frames")
def recipes_frames () :
    get_recipes = client[DB_NAME].recipes.find()
    get_users = list(client[DB_NAME].users.find())

    return render_template('public_all_recipes_frames.html', get_recipes=get_recipes, get_users=get_users)

#####-----------------------Public recipes page Frames view POST (search)------------------------

@app.route('/recipes/frames/search/', methods=["POST"])
def recipes_frames_search() :

    user_query = request.form.get("user_query")
    get_recipes = client[DB_NAME].recipes.find( {"$text" : { "$search" : user_query}})
    
    if user_query =="" :
        return redirect( url_for("recipes_frames"))
    elif list(get_recipes) :
        flash("Search results for "+'"'+user_query+'"')
    else :
        flash("No results for "+'"'+user_query+'"')
        return redirect( url_for("recipes_frames"))
    
    get_recipes = client[DB_NAME].recipes.find( {"$text" : { "$search" : user_query}})
    get_users = list(client[DB_NAME].users.find())

    return render_template('public_all_recipes_frames.html', get_recipes=get_recipes, get_users=get_users)

# -------------------------------Public each recipe page------------------------------------


@app.route('/recipes/<recipe_id>/')
def recipe_display(recipe_id):

    #####get object type recipe document base on given recipe_id#####
    get_recipe = client[DB_NAME].recipes.find_one({'_id': ObjectId(recipe_id)})

    #####prepare a lists from 0 to variable where variable is number of steps in recipe#######
    recipe_steps_num_list = list(range(0, len(get_recipe['steps'])))

    #####get object type user document base on the recipe's user_id######
    get_creator = client[DB_NAME].users.find_one(
        {'_id': ObjectId(get_recipe['user_id'])})

    ######store all the recipes id from the creator into a list#####
    recipes_id_list = []
    for r in get_creator['my_recipes']:
        recipes_id_list.append(r)

    print(recipes_id_list)
    print('-------------------------')

    ######retrieve the recipes names into a list from the recipes id######
    recipes_id_list_names = []
    for r in recipes_id_list:
        recipes_id_list_names.append(find_recipe_name(r))

    ######prepare a lists from 0 to variable where variable is number of recipes for the creator#####
    # creator_recipes_num_list = list(range(0,len(recipes_id_list_names)))

    print('^^^^^^^^^^^^^^^^whole lists:', recipes_id_list_names)
    print('-------------------------')

    ######find the average likes#####

    if (len(get_recipe["likes"]) > 0):
        sum_likes = 0
        for i in get_recipe['likes']:
            sum_likes = sum_likes+int(i['ratings'])

        avg_likes = round((sum_likes / len(get_recipe['likes'])), 2)

    else:

        avg_likes = "null"

    return render_template('public_recipe.html', get_recipe=get_recipe, recipe_steps_num_list=recipe_steps_num_list, get_creator=get_creator, recipes_id_list_names=recipes_id_list_names, avg_likes=avg_likes)


# --------------------------Public each recipe page Post bookmark---------------------

@app.route("/recipes/<recipe_id>/", methods=["POST"])
def bookmark_post(recipe_id):

    get_user = client[DB_NAME].users.find_one({
                    "email": request.form.get("email"),
                    "password": request.form.get("password")
                })
    
    #####check recipe_id not already in user favourites#####
    existing_bookmark=False
    
    if get_user is not None:
        user_id = get_user["_id"]
        for i in get_user["favourites"] :
            print (i)
            print (i[0])
            print (ObjectId(recipe_id))
            if i[0] == ObjectId(recipe_id) :
                existing_bookmark = True
            
    if get_user is None:
        flash("No matching email and password record.")
    elif existing_bookmark:
        flash("Already bookmarked.")
    else:
        
        client[DB_NAME].users.update_one({
                "_id": user_id
            }, {"$push": {"favourites": [ObjectId(recipe_id) , request.form.get("recipe-name"), request.form.get("get-creator") ] }})

        flash("Added to your bookmark.")
    
    return redirect(url_for("recipe_display", recipe_id = recipe_id))


# ----------------------------my account info page---------------------------------------

@app.route('/<user_id>/')
def account(user_id):

    get_user = client[DB_NAME].users.find_one({'_id': ObjectId(user_id)})
    user_id = get_user['_id']

    return render_template('my_account.html', get_user=get_user, user_id=user_id)

# --------------------------my account info page Post---------------------------------

@app.route('/<user_id>/' , methods=['POST'])
def update_account(user_id):
    
    original_email = request.form.get('email-hidden')
    current_email = (request.form.get('email')).lower()
    
    ##### if user changes his email #####
    if original_email != current_email :
    
        exist_email = client[DB_NAME].users.find_one({
                    "email" : request.form.get('email')
                    })

        ##### if changed email already exists somewhere in database #####
        if exist_email is not None :

            flash(" Failed to update account because email already registered by an existing user.  ")
            return redirect(url_for('account', user_id=user_id))

        #####proceeds to update email in database#####
        else:

            client[DB_NAME].users.update_one({
                '_id':ObjectId(user_id)
            }, {
                "$set": {
                    'user_name' : request.form.get('user-name'),
                    'password' : request.form.get('password'),
                    'email' : current_email,
                    'country' : string.capwords(request.form.get('country')),
                    'birthday' : request.form.get('birthday'),
                    'ethnicity' : string.capwords(request.form.get('ethnic'))
                }
            })

            flash("Your Account has been updated.")

            return redirect(url_for('account', user_id=user_id))

    ##### if user does not make changes to his email #####
    else :

        client[DB_NAME].users.update_one({
            '_id':ObjectId(user_id)
        }, {
            "$set": {
                'user_name' : request.form.get('user-name'),
                'password' : request.form.get('password'),
                'email' : current_email,
                'country' : string.capwords(request.form.get('country')),
                'birthday' : request.form.get('birthday'),
                'ethnicity' : string.capwords(request.form.get('ethnic'))
            }
        })

        flash("Your Account has been updated.")

        return redirect(url_for('account', user_id=user_id))

# ---------------------------my recipes page----------------------------------------

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

    #####get bookmarks from users document#####
    get_bookmarks = client[DB_NAME].users.find_one({
        "_id" :  ObjectId(user_id)
    },{ "favourites" : 1 })

    #####get user name for show login name#####
    get_user_name = client[DB_NAME].users.find_one({
        "_id" : ObjectId(user_id)
    }, {"user_name" : 1})

    user_name = get_user_name["user_name"]

    return render_template('my_recipes.html', get_my_recipes=get_my_recipes, recipes_avg_ratings_list=recipes_avg_ratings_list, user_id=user_id, get_bookmarks_lists=get_bookmarks["favourites"], user_name=user_name )


##---------------------------remove bookmarks from my recipes page --------------------------

@app.route("/<user_id>/my_recipes/remove_bookmark/<recipe_id>")
def remove_bookmark(user_id, recipe_id) :

    client[DB_NAME].users.update ({
        "_id" : ObjectId(user_id)
    },{ "$pull" : { "favourites" : { "$in" : [ObjectId(recipe_id)]}}})

    return redirect(url_for ("my_recipes", user_id = user_id))


# ------------------------------------EDIT recipe page----------------------------------------

@app.route('/<user_id>/my_recipes/<recipe_id>/edit')
def edit_recipe(user_id, recipe_id):

    get_recipe = client[DB_NAME].recipes.find_one({'_id':ObjectId(recipe_id)})

    #####prepare a lists from 0 to variable wher variable is number of steps in recipe####### 
    recipe_steps_num_list= list(range(0,len(get_recipe['steps'])))  

    user_id=user_id
    recipe_id=recipe_id

    #####get user name for show login name#####
    get_user_name = client[DB_NAME].users.find_one({
        "_id" : ObjectId(user_id)
    }, {"user_name" : 1})

    user_name = get_user_name["user_name"]


    return render_template("edit_recipe.html", get_recipe=get_recipe, recipe_steps_num_list=recipe_steps_num_list, user_id=user_id, recipe_id=recipe_id ,user_name=user_name)

## ----------------------------------EDIT recipe Post page-----------------------------------

@app.route('/<user_id>/my_recipes/<recipe_id>/edit', methods=['POST'])
def update_recipe(user_id, recipe_id):
    
    if request.form.get("recipe-name") =="" or request.form.get("cuisine") =="" :
    
        flash("Fail to save the edit due to missing Recipe Name or Cuisine. ")
        return redirect(url_for("update_recipe", user_id=user_id , recipe_id=recipe_id))

    else :
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
                "recipe_name" :  string.capwords(request.form.get("recipe-name")),
                "steps" : steps_list,
                "ingredients" : ing_list,
                "tools" : tools_list,
                "cuisine" : string.capwords(request.form.get("cuisine")),
                "my_rating" : int(request.form.get("my-rating")),
                "number_steps" : request.form.get( "num-steps"),
                "date_last_edited" : datetime.datetime.now().strftime("%Y-%m-%d")
            }
        })

        return redirect(url_for("my_recipes", user_id=user_id))

# ------------------ EDIT images page -----------------------------------------
@app.route('/<user_id>/my_recipes/<recipe_id>/edit_images')
def edit_images(user_id , recipe_id) :

    ##### pass uploadcare key from .env to html template #####
    uploadcare_public_key=os.environ.get("UPLOADCARE_PUBLIC_KEY")

    get_images = client[DB_NAME].recipes.find_one({
                "_id" : ObjectId(recipe_id)
                },{ "photos" : 1})

    get_recipe_name = client[DB_NAME].recipes.find_one({
                "_id" : ObjectId(recipe_id)
    }, { "recipe_name" : 1})

    user_id=user_id
    recipe_id=recipe_id

    #####get user name for show login name#####
    get_user_name = client[DB_NAME].users.find_one({
        "_id" : ObjectId(user_id)
    }, {"user_name" : 1})

    user_name = get_user_name["user_name"]

    return render_template("edit_images.html", get_images = get_images, user_id=user_id, recipe_id=recipe_id, uploadcare_public_key=uploadcare_public_key, get_recipe_name=get_recipe_name, user_name=user_name)

# -----------------------EDIT images post page------------------------------------
@app.route('/<user_id>/my_recipes/<recipe_id>/edit_images', methods=["POST"])
def edit_images_post(user_id, recipe_id) :

    user_id = user_id
    recipe_id=recipe_id

    ##### delete any existing photo #####
    get_images = client[DB_NAME].recipes.find_one({
        "_id" : ObjectId(recipe_id)
    },{ "photos" : 1})

    num_exist_images = len(get_images["photos"])

    for i in range(0,num_exist_images) :
        print("step 1-----------------------")
        print("image-exist-"+str(i))
        print(request.form.get("image-exist-"+str(i)))
        if request.form.get("image-exist-"+str(i)) :
            print("step2------------------------")
            client[DB_NAME].recipes.update_one({
                "_id" :ObjectId(recipe_id)
            }, { "$pull" : { "photos" : { "$in" : [request.form.get("image-exist-url-"+str(i))]}}  })

    ##### to add any new photos #####
    num_images = request.form.get("num-images-edit-pg")
    

    for i in range(0, int(num_images)) :
        print("step3---------------------")
        print(request.form.get("image-"+str(i)))
        if request.form.get("image-"+str(i)) :

            client[DB_NAME].recipes.update({
                "_id" : ObjectId(recipe_id)
            },{ 
                "$push" : {"photos" : request.form.get("image-"+str(i)) }
            })
    
    return redirect(url_for("edit_images_post", user_id=user_id, recipe_id= recipe_id))


# ----------------------confirm prompt delete recipe page-----------------------------

@app.route("/<user_id>/my_recipes/<recipe_id>/delete")
def delete_recipe_page (user_id, recipe_id) :

    return render_template("delete_recipe.html", user_id=user_id, recipe_id=recipe_id )

# ----------------------confirm prompt delete recipe page Post-----------------------------

@app.route("/<user_id>/my_recipes/<recipe_id>/process_delete")
def delete_recipe (user_id, recipe_id) :

    get_user = client[DB_NAME].users.find_one({
        "_id" : ObjectId(user_id)
    })
    print("--------HELLO---------------------")
    print(get_user)
    print(get_user['user_name'])
    print(get_user['my_recipes'])
    print(len(get_user['my_recipes']))
    print("-----------------------------")

    #####find which array contains the recipe to be deleted#####
    recipe_pos_in_array = 0
    for i in range(int(len(get_user["my_recipes"]))) :
        if get_user["my_recipes"][i] == recipe_id :
            recipe_pos_in_array = i
        

    print (recipe_pos_in_array)
    print (get_user["my_recipes"][recipe_pos_in_array])

    #####delete the recipe_id in the users data######
    client[DB_NAME].users.update({
        "_id" : ObjectId(user_id)
    }, {
        "$pull" : {
            "my_recipes" : {
                "$in": [ObjectId(recipe_id)]
            }
        }
    })

    
    client[DB_NAME].recipes.remove({
        "_id" : ObjectId(recipe_id)
    })

    return redirect(url_for("my_recipes", user_id=user_id))

# ----------------------------------ADD recipe page--------------------------------------

@app.route("/<user_id>/add_recipe")
def add_recipe(user_id) :

    ##### pass uploadcare key from .env to html template #####
    uploadcare_public_key=os.environ.get("UPLOADCARE_PUBLIC_KEY")
    user_id=user_id
    
    #####get user name for show login name#####
    get_user_name = client[DB_NAME].users.find_one({
        "_id" : ObjectId(user_id)
    }, {"user_name" : 1})

    user_name = get_user_name["user_name"]

    return render_template("add_recipe.html", user_id=user_id, uploadcare_public_key=uploadcare_public_key,  user_name=user_name)

# -------------------------------ADD recipe page post----------------------------------

@app.route("/<user_id>/add_recipe", methods=["POST"])
def add_recipe_post(user_id) :

    if request.form.get("recipe-name") =="" or request.form.get("cuisine") =="" or request.form.get("my-rating") =="Choose..." :
    
        flash("Unable to add recipe because of missing Recipe Name, Cuisine or My Rating.")
        return redirect(url_for("add_recipe_post", user_id=user_id))

    else:

        ##### update info into recipes database ######
        num_steps = request.form.get("num-steps-np")

        steps_list=[]
        ing_list=[]
        tools_list=[]
        likes_list=[]
        

        for i in range(0, int(num_steps)):
            steps_list.append(request.form.get("step-"+str(i)))
            ing_list.append(request.form.get("ing-"+str(i)))
            tools_list.append(request.form.get("tools-"+str(i)))

        num_images = request.form.get("num-images-np")
        images_list=[]
        
        for i in range(0, int(num_images)):
            if request.form.get("image-"+str(i)) : 
                images_list.append(request.form.get("image-"+str(i)))

        client[DB_NAME].recipes.insert_one({
            "_id" : ObjectId(),
            "recipe_name" : string.capwords(request.form.get("recipe-name")),
            "steps" : steps_list,
            "ingredients" : ing_list,
            "tools" : tools_list,
            "cuisine" : string.capwords(request.form.get("cuisine")),
            "photos" : images_list,
            "my_rating" : int(request.form.get("my-rating")),
            "likes" : likes_list,
            "user_id" : user_id,
            "date_posted" : datetime.datetime.now().strftime("%Y-%m-%d"),
            "date_last_edited": "null",
            "number_steps" : request.form.get("num-steps-np"),
            "avg_likes" : 0 ,
            "num_reviews" : 0 

        })

        #####update recipe id into users database#####
        get_recipe_id = client[DB_NAME].recipes.find_one({
                        "user_id" : user_id ,
                        "recipe_name" : string.capwords(request.form.get("recipe-name")),
                        "number_steps" : request.form.get("num-steps-np"),
                        "my_rating" : int(request.form.get("my-rating")),
                        "steps" : steps_list,
                        "ingredients" : ing_list,
                        "tools" : tools_list,
                        })

        recipe_id= get_recipe_id["_id"]
    
        client[DB_NAME].users.update_one(
            { "_id" : ObjectId(user_id)}, 
            { "$push" : { "my_recipes" : recipe_id } }
        )

        return redirect(url_for("my_recipes", user_id=user_id ))

# -----------------------create account page---------------------------------------

@app.route("/create_account/")
def create_account ():

    return render_template("create_account.html")

# ----------------------create account post---------------------------------------

@app.route("/create_account/", methods=["POST"])
def create_account_post ():

    my_recipes_list=[]
    favourites_list=[]
    email = (request.form.get("email")).lower()
    username = request.form.get("user-name")

    exist_email = client[DB_NAME].users.find_one({
                    "email" : email
                    })

    exist_username = client[DB_NAME].users.find_one({
                    "user_name" : username
                    })

    if exist_email is not None :
         flash(" Existing account with this email already in use. ")

         return redirect(url_for("create_account_post"))
    
    elif exist_username is not None :

        flash("Username already exists.")

        return redirect(url_for("create_account_post"))
    else :

        
        client[DB_NAME].users.insert_one({

            "_id" : ObjectId(),
            "user_name" : username,
            "password" : request.form.get("password"),
            "email" : email,
            "country" : string.capwords(request.form.get("country")),
            "birthday" : request.form.get("birthday"),
            "ethnicity" : string.capwords(request.form.get("ethnic")),
            "my_recipes" : my_recipes_list,
            "favourites" : favourites_list,
            "first_joined" : datetime.datetime.now().strftime("%Y-%m-%d")

        })

        get_user = client[DB_NAME].users.find_one({"email" : email})
        user_id = get_user["_id"]
        print("-------------------------",user_id)

        return redirect(url_for("my_recipes", user_id=user_id))

# -------------------------login page--------------------------------

@app.route("/login/")
def login() :

    print("---------------------hello")

    return render_template("login.html")

# -----------------------login page post---------------------------

@app.route("/login/", methods=["POST"])
def login_post() :

    get_user =client[DB_NAME].users.find_one({
            "email" : request.form.get("email"),
            "password" : request.form.get("password")
            })
    
    if get_user is None :
        
        flash("No matching email and password for account. Please try again.")

        return redirect(url_for("login"))
    else :
        
        user_id = get_user["_id"]

        client[DB_NAME].users.update_one({
            "_id" : ObjectId(user_id)
        }, { "$set" : { "last_login" : datetime.datetime.now().strftime("%Y-%m-%d")}})


        return redirect(url_for("my_recipes", user_id=user_id))

# ----------------------------------review recipe page------------------------

@app.route("/recipes/<recipe_id>/reviews")
def reviews(recipe_id) :

    get_recipe = client[DB_NAME].recipes.find_one({ "_id" : ObjectId(recipe_id)})

    reviews_list = get_recipe["likes"]
    recipe_name = get_recipe["recipe_name"]

    contributor_id = get_recipe["user_id"]
    get_user = client[DB_NAME].users.find_one({ "_id" : ObjectId(contributor_id)})
    contributor_name = get_user["user_name"]
    

    return render_template("reviews.html", reviews_list=reviews_list, recipe_name=recipe_name , contributor_name=contributor_name, recipe_id=recipe_id )

# ------------------------------------review recipe page post--------------------
@app.route("/recipes/<recipe_id>/reviews", methods=["POST"])
def reviews_post(recipe_id) :

    get_valid_user = client[DB_NAME].users.find_one({ 
        "user_name" : request.form.get("username"),
        "password" : request.form.get("password")
    })

    get_ratings = request.form.get("ratings")
  
    
    if get_valid_user == None :
        flash ("Sorry, no valid user with password found. Please try again.")
        
        return redirect(url_for("reviews_post", recipe_id = recipe_id))

    elif get_ratings == "Choose..." :

        flash("Please insert ratings. ") 

        return redirect(url_for("reviews_post", recipe_id = recipe_id))

    else:

        client[DB_NAME].recipes.update_one({
            "_id" : ObjectId(recipe_id)
        }, {
            "$push" : {
                "likes" : {
                    "reviewer_name" : request.form.get("username"),
                    "reviews" : request.form.get("reviews"),
                    "ratings" : request.form.get("ratings"),
                    "date" : datetime.datetime.now().strftime("%Y-%m-%d")
                }
            }
        })
        
        #####update the average ratings and number of reviews in document#####
        get_recipe = client[DB_NAME].recipes.find_one({ "_id" : ObjectId(recipe_id) })

        num_reviews = get_recipe["num_reviews"] + 1
        avg_likes = round(
                (float(get_recipe["avg_likes"])*(int(num_reviews)-1) + int(request.form.get("ratings")))/int(num_reviews)
                ,2)
            

        client[DB_NAME].recipes.update_one({
            "_id" : ObjectId(recipe_id)
        }, {
            "$set" : {
                "avg_likes" : avg_likes ,
                "num_reviews" : num_reviews
            }
        })

        return redirect(url_for("reviews_post", recipe_id=recipe_id))

# ----------------------------Sort order------------------------------------------

# ---------------------------Sort by date descending------------------------
@app.route("/recipes/sort_date_d/")
def sort_date_d() :

    get_recipes = client[DB_NAME].recipes.find().sort( "date_posted" , -1)
    get_users = list(client[DB_NAME].users.find())

    return render_template("public_all_recipes.html", get_recipes = get_recipes , get_users=get_users)

# ----------------------------Sort by date ascending-----------------------
@app.route("/recipes/sort_date_a/")
def sort_date_a() :

    get_recipes = client[DB_NAME].recipes.find().sort( "date_posted" , 1)
    get_users = list(client[DB_NAME].users.find())

    return render_template("public_all_recipes.html", get_recipes = get_recipes, get_users=get_users)


# ----------------------------Sort by cuisine descending-----------------------
@app.route("/recipes/sort_cuisine_d/")
def sort_cuisine_d() :

    get_recipes = client[DB_NAME].recipes.find().sort( "cuisine" , -1)
    get_users = list(client[DB_NAME].users.find())

    return render_template("public_all_recipes.html", get_recipes = get_recipes , get_users=get_users)

# ----------------------------Sort by cuisine ascending-----------------------
@app.route("/recipes/sort_cuisine_a/")
def sort_cuisine_a() :

    get_recipes = client[DB_NAME].recipes.find().sort( "cuisine" , 1)
    get_users = list(client[DB_NAME].users.find())

    return render_template("public_all_recipes.html", get_recipes = get_recipes, get_users=get_users)

# ----------------------------Sort by recipe name descending-----------------------
@app.route("/recipes/sort_recipe_d/")
def sort_recipe_d() :

    get_recipes = client[DB_NAME].recipes.find().sort( "recipe_name" , -1)
    get_users = list(client[DB_NAME].users.find())

    return render_template("public_all_recipes.html", get_recipes = get_recipes , get_users=get_users)

# ----------------------------Sort by recipe name ascending-----------------------
@app.route("/recipes/sort_recipe_a/")
def sort_recipe_a() :

    get_recipes = client[DB_NAME].recipes.find().sort( "recipe_name" , 1)
    get_users = list(client[DB_NAME].users.find())

    return render_template("public_all_recipes.html", get_recipes = get_recipes , get_users=get_users)

# --------------------------Sort by average ratings descending-----------------------------
@app.route("/recipes/sort_likes_d")
def sort_ratings_d() :

    get_recipes = client[DB_NAME].recipes.find().sort( "avg_likes" , -1)
    get_users = list(client[DB_NAME].users.find())

    return render_template("public_all_recipes.html", get_recipes = get_recipes , get_users=get_users)

# --------------------------Sort by average ratings acscending-----------------------------
@app.route("/recipes/sort_likes_a")
def sort_ratings_a() :

    get_recipes = client[DB_NAME].recipes.find().sort( "avg_likes" , 1)
    get_users = list(client[DB_NAME].users.find())

    return render_template("public_all_recipes.html", get_recipes = get_recipes , get_users=get_users)

# --------------------------Sort by number reviews descending-----------------------------
@app.route("/recipes/sort_reviews_d")
def sort_reviews_d() :

    get_recipes = client[DB_NAME].recipes.find().sort( "num_reviews" , -1)
    get_users = list(client[DB_NAME].users.find())

    return render_template("public_all_recipes.html", get_recipes = get_recipes , get_users=get_users)

# --------------------------Sort by number reviews ascending-----------------------------
@app.route("/recipes/sort_reviews_a")
def sort_reviews_a() :

    get_recipes = client[DB_NAME].recipes.find().sort( "num_reviews" , 1)
    get_users = list(client[DB_NAME].users.find())

    return render_template("public_all_recipes.html", get_recipes = get_recipes , get_users=get_users)

# --------------------------Sort by self rating descending-----------------------------
@app.route("/recipes/sort_self_rating_d")
def sort_self_rating_d() :

    get_recipes = client[DB_NAME].recipes.find().sort( "my_rating" , -1)
    get_users = list(client[DB_NAME].users.find())

    return render_template("public_all_recipes.html", get_recipes = get_recipes , get_users=get_users)

# --------------------------Sort by self rating ascending-----------------------------
@app.route("/recipes/sort_self_rating_a")
def sort_self_rating_a() :

    get_recipes = client[DB_NAME].recipes.find().sort( "my_rating" , 1)
    get_users = list(client[DB_NAME].users.find())

    return render_template("public_all_recipes.html", get_recipes = get_recipes , get_users=get_users)
   
# --------------------------functions------------------------

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
    
        recipe_avg_rating = round(float(rating_sum / number_of_ratings),2)
    else:

        recipe_avg_rating ="null"


    return recipe_avg_rating




if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)

