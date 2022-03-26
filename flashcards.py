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
def welcome():
    return render_template(
        "welcome.html",
        cards=db
        )

""" 
special piece of syntax: <~> 
assume the parameter will be integer, and will be assigned into index parameter
"""

@app.route("/card/<int:index>")
def card_view(index):
    try:
        card = db[index]
        return render_template("card.html",
        card=card,
        index=index,
        max_index=len(db)-1
        )
    except IndexError:
        abort(404)


""" 
request class;
it retrieve the data submitted via form
"""
@app.route('/add_card/', methods=["GET", "POST"])
def add_card():
    if request.method == "POST":
        card = {"question": request.form['question'],
                "answer": request.form['answer']}
        db.append(card)
        save_db()
        return redirect(url_for('card_view', index=len(db)-1))
    else:
        return render_template("add_card.html")


@app.route('/remove_card/<int:index>', methods=["GET", "POST"])
def remove_card(index):
    try:
        if request.method == "POST":
            del db[index]
            save_db()
            return redirect(url_for('welcome'))
        else:
            return render_template("remove_card.html", card=db[index])
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