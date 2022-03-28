#import Flask class from flask package
from crypt import methods
from operator import index
from flask import Flask, render_template, abort, jsonify, request, redirect, url_for
from model import db, save_db

""" Flask constructor. create a global Flask application object.
dunder name: special variable containing the name of the current module
__name__ is String of flashcards (file name) """
app = Flask(__name__)

""" 
change the welcome function into a "view function".
@ is decorator.
@app.route is an attribute of the app object.
assigning an URL to the function.
view method.
The function below the decorator is "view function"
URL name = function name in practice
"""


@app.route("/")
def top():
    return render_template(
        "top.html",
        articles=db
        )

""" 
special piece of syntax: <~> 
assume the parameter will be integer, and will be assigned into index parameter
"""

@app.route("/article/<int:index>")
def article_view(index):
    try:
        article = db[index]
        return render_template("article.html",
        article=article,
        index=index,
        max_index=len(db)-1
        )
    except IndexError:
        abort(404)


""" 
request class;
it retrieve the data submitted via form
"""
@app.route('/add_article/', methods=["GET", "POST"])
def add_article():
    if request.method == "POST":
        article = {
                "date": request.form['date'],
                "title": request.form['title'],
                "body": request.form['body']
                }
        db.append(article)
        save_db()
        return redirect(url_for('article_view', index=len(db)-1))
    else:
        return render_template("add_article.html")


@app.route('/remove_aritcle/<int:index>', methods=["GET", "POST"])
def remove_card(index):
    try:
        if request.method == "POST":
            del db[index]
            save_db()
            return redirect(url_for('top'))
        else:
            return render_template("remove_article.html", article=db[index])
    except IndexError:
        abort(404)


""" REST-API """
@app.route("/api/card/")
def api_card_list():
    return jsonify(db)

@app.route('/api/card/<int:index>')
def api_card_detail(index):
    try:
        return db[index]
    except IndexError:
        abort(404)