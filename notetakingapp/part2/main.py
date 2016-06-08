from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy 
import os
import json
import traceback
from AlchemyEncoder import AlchemyEncoder

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'app.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# if( not os.path.exists(app.config['SQLALCHEMY_DATABASE_URI']))
# db.create_all()
db = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)


@app.route("/home")
@app.route("/")
def home():
    '''for line in traceback.format_stack():
        print(line.strip())'''
    notes = Note.query.all()
    return render_template("home.html", notes=notes)


@app.route("/notes/create", methods=["GET", "POST"])
def create_note():
    if request.method == "GET":
        return render_template("create_note.html")
    else:
        title = request.form["title"]
        body = request.form["body"]

        note = Note(title=title, body=body)

        db.session.add(note)
        db.session.commit()
        return redirect("/notes/create")


@app.route("/delete", methods=["GET", "POST"])
def delete():
    id = request.args.get('id')
    Note.query.filter(Note.id == id).delete()
    db.session.commit()
    notes = Note.query.all()
    return render_template("home.html", notes=notes)


@app.route("/ajaxCreate", methods=["POST"])
def ajaxCreate():
    title = request.form["title"]
    body = request.form["body"]
    note = Note(title=title, body=body)
    db.session.add(note)
    db.session.commit()
    # return json.dumps(note.__dict__)
    return json.dumps(note, cls=AlchemyEncoder)
    # return "ok"


if __name__ == "__main__":

    app.run(debug=True)
