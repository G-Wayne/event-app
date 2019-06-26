from runapp import db

class User(db.Model):
	id=  db.Column(db.Integer, primary_key=True)
	public_id= db.Column(db.String(50), unique=True)
	name= db.Column(db.String(50))
	password= db.Column(db.String(80))
	admin= db.Column(db.Boolean)


class Event(db.Model):   #Additional Attributes - Question 5
	id=  db.Column(db.Integer, primary_key=True)
	title= db.Column(db.String(100),nullable=False)
	name= db.Column(db.String(50))
	description= db.Column(db.String(100))
	category= db.Column(db.String(50))
	start_date_start_time = db.Column(db.String(50))  #was giving problems in Postman as DateTime
	end_date_end_time = db.Column(db.String(50)) #was giving problems in Postman as DateTime
	cost= db.Column(db.Float)
	venue= db.Column(db.String(100))
	flyer= db.Column(db.String(50))
	visible= db.Column(db.Boolean)
	creator= db.Column(db.Integer,db.ForeignKey('user.id'))

