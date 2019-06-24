from runapp import db

class User(db.Model):
	id= db.Column(db.Integer,primary_key=True)
	public_id=db.Column(db.String(50),unique=True)
	name=db.Column(db.String(50))
	password=db.Column(db.String(80))
	admin=db.Column(db.Boolean)

class Event(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(50),nullable=False)
	event_date=db.Column(db.DateTime,nullable=False)
	description=db.Column(db.String(100),nullable=False)
	creater=db.Column(db.Integer,db.ForeignKey('user.id'))