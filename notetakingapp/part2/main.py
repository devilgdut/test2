from flask import Flask, render_template, redirect, request,url_for
from flask_sqlalchemy import SQLAlchemy 
from flask_login import login_user, logout_user, current_user, login_required,LoginManager
import os
import json
import traceback
from AlchemyEncoder import AlchemyEncoder
from forms import LoginForm

app = Flask(__name__)

app.config.from_object('config')

# if( not os.path.exists(app.config['SQLALCHEMY_DATABASE_URI']))
# db.create_all()
db = SQLAlchemy(app)
lm = LoginManager()
#lm.login_view = 'userlogin'
lm.init_app(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)


@app.route("/home")
@app.route("/")
#@login_required
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
@login_required
def ajaxCreate():
    title = request.form["title"]
    body = request.form["body"]
    note = Note(title=title, body=body)
    db.session.add(note)
    db.session.commit()
    # return json.dumps(note.__dict__)
    return json.dumps(note, cls=AlchemyEncoder)
    # return "ok"

@app.route("/login",methods=["POST","GET"])
def userlogin():

    form = LoginForm()
        #if form.validate_on_submit():
        #session['remember_me'] = form.remember_me.data
        #print(form.remember_me.data)
    return render_template("login.html",form=form)

@app.errorhandler(401)
def unauthorized_error(error):
    #return render_template("login.html"), 401
    return redirect(url_for("userlogin"))

if __name__ == "__main__":

    app.run(debug=True)
