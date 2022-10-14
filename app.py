from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from newsapi import NewsApiClient


app = Flask(__name__)    #Create the database, using sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)   #have a unique id for each Todo things
    title = db.Column(db.String(100))    #100 is the max character can be typed in add box
    complete = db.Column(db.Boolean) 

#Set the nav bar for everypage
@app.route("/")
def base():
    return render_template('base.html')

#Set the home page
@app.route("/home")
def home():
    return render_template('home.html')

#Set the ToDo List page
@app.route("/todolist")
def index():
    todo_list = Todo.query.all()
    print(todo_list)
    return render_template('todolist.html', todo_list=todo_list)
#Set the ToDo List page -- ADD function
@app.route("/add", methods = ["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))
#Set the ToDo List page -- Mark as Complete function
@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))
#Set the ToDo List page -- Delete function
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

#Set the Movie page
@app.route('/movie')
def movie():
    data = pd.read_csv('/Users/tianyuelun/Desktop/web craw/web flask project/venv/2021movies.csv')
    data = data.rename(columns={'Release': 'name', 'Theaters':'value'})
    data = data.to_dict(orient='records')
    print(data)
    return render_template('movie.html', data = data)

#Set News page(use api)
@app.route('/news')
def news():
    newsapi = NewsApiClient(api_key='172128187a4b4cc5a0d5f1789072c325')
    topheadlines = newsapi.get_top_headlines(sources = 'bbc-news')
    articles = topheadlines['articles']

    desc = []
    news = []
    img = []

    for i in range(len(articles)):
        myarticles = articles[i]
        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])

    mylist = zip(news, desc, img)

    return render_template('news.html', context=mylist)

#Set Quotes page
@app.route('/bestquotes')
def travel():
    return render_template('bestquotes.html')

#Set Contact page
@app.route("/contact")
def contact():
    return render_template('contact.html')

#main
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)