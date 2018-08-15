import os
from datetime import datetime
from flask import Flask, redirect, render_template, request
import random
import logging
from flask import url_for
app = Flask(__name__)


def write_to_file(filename, data):
    """Handle the process of writing data to a file"""
    with open(filename, "a") as file:
        file.writelines(data)

def get_all():
    dict = {}
    with open("data/guess.txt", "r+") as f:
        for line in f:
            (k, v) = line.split()
            dict[k] = v
    f.close()
    return dict

def get_img(question):
    imgdict = {}
    with open("data/img.txt", "r+") as f:
        for line in f:
            (k, v) = line.split()
            imgdict[k] = v
    return imgdict[question]
    
def check_guess(q, a, username):
    """Add one point to the score associated to the username"""
    dict = get_all()
    if dict[q] == a.lower():
        return True
    else:
        return False
        
def get_users():
    dict = {}
    with open("data/scores.txt", "r+") as f:
        for line in f:
            (u, val) = line.split()
            dict[u] = val
    f.close()
    return dict
    
def add_user(username):
    """Add a user with given username"""
    dict = get_users()
    if not username in dict:
        write_to_file("data/scores.txt", str(username) + ' '+ str(0) + '\n')
        
def add_score(username):
    dict = get_users()
    user_score = int(dict[username])
    user_score = user_score + 1
    dict[username] = str(user_score)
    with open("data/scores.txt", "w") as f:
        for k, v in dict.items():
            f.write(str(k) + ' '+ str(v) + '\n')
    f.close()

def check_score(username):
    dict = get_users()
    user_score = dict[username]
    return user_score
    
def get_another():
    """Get another key inside guess file"""
    dict = get_all()
    k= random.choice(list(dict.keys()))
    return k
    

@app.route('/', methods=["GET", "POST"])
def index():
    """Main page with instructions"""
    # Handle POST request
    if request.method == "POST":
        username = request.form["username"]
        add_user(username)
        question = get_another()
        return redirect(url_for('user_guess', username=username, question=question))
    return render_template("index.html")
    

#@app.route('/<username>', methods=["GET", "POST"])
@app.route('/<username>/<question>', methods=["GET", "POST"])
def user_guess(username, question):
    score = check_score(username)
    img = get_img(question)
    wrong_answer = ""
    if request.method == "POST":
        if check_guess(question, request.form["answer"], username):
            new_question = get_another()
            while (new_question == question):
                new_question = get_another()
            question = new_question
            add_score(username)
            score = check_score(username)
            img = get_img(question)
            wrong_answer = ""
            return redirect(url_for('user_guess', username=username, question=question))
        else:
            wrong_answer = "Incorrect answer, your answer was: " + request.form["answer"] + " , please try again:"
    return render_template("user.html", username=username, question=question, wrong_answer=wrong_answer, score = score, img = img)

app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)