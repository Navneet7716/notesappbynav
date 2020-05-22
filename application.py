from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
	app.debug = True
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:dhruvrishi123@localhost:5432/noteapp'

else:
	app.debug = False
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jkepbppkbomfmb:f11db2ae8f4d51983fbff283e0301dc52ec32b094c119ec8df935ba4e7a92c65@ec2-3-222-150-253.compute-1.amazonaws.com:5432/d713ruits1dbue'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class User(db.Model):
	__tablename__ = "userlist"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, nullable=False)
	password = db.Column(db.String, nullable=False)

	def __init__(self, username, password):
		self.username = username
		self.password = password 


class Notes(db.Model):
	__tablename__ = "notes"
	title = db.Column(db.String, nullable=False)
	content = db.Column(db.String, nullable=False)
	id = db.Column(db.Integer, primary_key=True)
	notes_id = db.Column(db.Integer, db.ForeignKey("userlist.id"), nullable=False)

	def __init__(self, title, content, notes_id):
		self.title = title
		self.content = content
		self.notes_id = notes_id


@app.route("/")
def signup():
	return render_template("signin.html")


@app.route("/success", methods=["POST"])
def success():
	if request.method == "POST":
		email = request.form.get('username')
		password = request.form.get('pass')
		if db.session.query(User).filter(User.username == email).count() != 0:
			return render_template("raw2.html", message="ID ALREADY TAKEN TRY A DIFFERENT ID!!")
		user = User(email, password)
		db.session.add(user)
		db.session.commit()
		return render_template("raw.html", title="SUCCESS", message="HEY, YOUR ID IS CREATED!!")



@app.route("/login", methods=["GET", "POST"])
def login():
	return render_template("login2.html")

@app.route("/login/users", methods=["POST","GET"])
def user():
	if request.method == "POST":
		email = request.form.get('username')
		password = request.form.get('pass')
		y = db.session.query(User).filter(User.username == email and User.password == password).first()
		if y == None:
			return render_template("raw.html", title="FAIL", message="USER DOESN'T EXISTS!")
		
		return redirect(url_for('note', user_id= y.id))


@app.route("/login/users/?jnkjn25<int:user_id>9mnkjb", methods=["POST", "GET"])
def note(user_id):
	if request.method == "POST":
		t = request.form.get('title')
		c = request.form.get('content')
		data = Notes(t,c,user_id)
		db.session.add(data)
		db.session.commit()
	y = db.session.query(Notes).filter(Notes.notes_id == user_id).all()
	return render_template("note.html", notels=y, u_id=user_id)


@app.route("/clear/<int:deletenote>/<int:userid>", methods=["POST"])
def delete(deletenote, userid):
	if request.method == "POST":
		db.session.query(Notes).filter_by(id=deletenote).delete()
		db.session.commit()
		return redirect(url_for('note', user_id= userid))


if __name__ == "__main__":
	app.run()