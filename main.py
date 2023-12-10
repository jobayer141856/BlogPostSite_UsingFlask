from flask import *
from flask import Flask, request, redirect, render_template, session
from bson.objectid import ObjectId
import pymongo


myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["mydatabase2"]

users_table = mydb["users_blog"]
users_table2 = mydb["users_info"]


app = Flask(__name__)

@app.route('/login', methods=['GET', "POST"])

def login():
    if request.method == "POST":
        form_data = dict(request.form)
        form_username = form_data['username']
        form_password = form_data['password'] 

        db_found = users_table2.find({'username': form_username})
        if db_found:
            if form_password != db_found['password']:
                return 'password does not match'
            else:
                return 'login in successfull'
        else:
            return 'username not found'
    return render_template("login.html", **locals())

@app.route('/register', methods=['GET', "POST"])
def register():
    if request.method == "POST":
        form_data = dict(request.form)
        print(request.form)
        form_username = form_data['username']
        form_name = form_data['name']
        form_emai = form_data['email']
        form_pass = form_data['password']
        form_pass2 = form_data['conf_password']

        db_found = users_table2.find_one({'username': form_username})
        if db_found:
            return 'username already exist'
        else:
            if form_pass != form_pass2:
                return 'password does not match'
            else:
                users_table2.insert_one(form_data)
                return 'registration successful'
    return render_template("register.html", **locals())
            



@app.route('/blog', methods=['GET', "POST"])
def blog():
    if request.method == "POST":
        form_data = dict(request.form)
        form_title = form_data["title"]
        form_textarea = form_data["blog"]
        users_table.insert_one(
            {"title": form_title, "blog": form_textarea})
        return redirect(url_for('blog_list'))
    return render_template("blog.html", **locals())

@app.route('/blog_list', methods=['GET', "POST"])
def blog_list():
    title_list = []
    title_id = []
    len_list = 0
    blog_list = {}
    i = 0
    for blog_title in users_table.find():
        title_list.append(blog_title["title"])
        title_id.append(blog_title["_id"])
        blog_list[i] = [blog_title["_id"], str(blog_title["title"])]
        i+=1
    len_list = len(title_list)
    # print(blog_list[0][0])
    # print(len_list)
    # print(title_list)
    is_post = False
    is_blog = False
    view_blog = []
    if request.method == 'POST':
        is_post = True
        form_data = dict(request.form)
        id = form_data["id"]
        id =str(id)
        print("str "+id)
        blogs = []
        for blog_view in users_table.find({"_id": ObjectId(id)}):
            blogs.append(blog_view["title"])
            blogs.append(blog_view["blog"])
            is_blog = True
        print(blogs)
    return render_template("blog_list.html", **locals())

@app.route('/edit/<string:s>', methods=['GET', "POST"])
def edit(s):
    s =str(s)
    p = 2
    edblog = []
    ed = users_table.find_one({"_id": ObjectId(s)})
    edblog.append(ed["title"])
    edblog.append(ed["blog"])
    edblog.append(ed["_id"])
    if request.method=='POST':
        print("blog")
        print(request.form["blog2"])
        users_table.update_one({"_id": ObjectId(s)},  {"$set" : {"blog" :request.form["blog2"]}})
        users_table.update_one({"_id": ObjectId(s)}, {"$set" : {"title" :request.form["title1"]}})
        print("Updated")
        return redirect(url_for('blog_list'))

    return render_template("edit_blog.html", **locals())


@app.route('/delete/<string:s>', methods=['GET', "POST"])
def delete(s):
    s =str(s)
    if users_table.delete_many({'_id': ObjectId(s)}):
        return redirect(url_for('blog_list'))

    return render_template("blog_list.html")

@app.route('/', methods=['GET', "POST"])
def index():

    return render_template("home.html", **locals())

if __name__ == '__main__':
    app.run(debug=True)