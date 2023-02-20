from flask import render_template
from flasktodo import app, db

todolist = [ 
    {
        'subject': 'Znaleźć mieszkanie',
        'more_info': 'lokalizacja: goc,  ok 60m, 3 pokoje',
        'when_todo': '22.02.2023',
        'date_created': '19.02.2023',
    },
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', todolist=todolist)


@app.route("/add")
def add_to_list():
    return render_template("add.html", title='Add')