from flask import Flask, render_template, request, redirect, url_for
import pymongo
from filter import filter_foods as filter
import random

client = pymongo.MongoClient("mongodb://localhost:27017")
d = client["foodpicker"]
db = d["meals"]

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        tag = request.form.getlist("tag")
        if tag:
            tag_string = tag[0]
            print(tag_string)
            foods = filter(tag_string)
            if foods:
                chosen = random.choice(foods)
                return render_template('index.html', food=chosen["food"])
            else:
                return render_template('index.html', food="No foods available for the selected tag!")
        if request.form.get("action") == "redrect":
            return redirect(url_for("add"))
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        if request.form.get("action") == "back":
            return redirect(url_for("home"))

        text = request.form.get("text")
        tag = request.form.get("tag")
        if db.find_one({"food": text}):
            return redirect(url_for("add", text=text, err="error1"))
        elif not tag or text == "":
            return redirect(url_for("add", err="error"))
        else:
            food = {"food": text, "tags": tag}
            db.insert_one(food)
            return redirect(url_for("add", text=text))

    err = request.args.get("err")
    text = request.args.get("text")
    return render_template('add.html', err=err, text=text)

if __name__ == '__main__':
    app.run()
