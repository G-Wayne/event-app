from flask import Flask,request,jsonify,make_response
from flask_sqlalchemy import SQLAlchemy 
from runapp import app,db
# from models import *
import uuid
from werkzeug.security  import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
import jwt
import datetime
import os
from functools import wraps

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token=None

		if 'x-access-token' in request.headers:
			token= request.headers['x-access-token']

		if not token:
			return jsonify({'message': 'Token is missing'}), 401

		try: 
			data= jwt.decode(token,app.config['SECRET_KEY'])
			current_user= User.query.filter_by(public_id=data['public_id']).first()
		except:
			return jsonify({'message': 'Token is invalid'}), 401

		return f(current_user, *args, **kwargs)

	return decorated


@app.route('/user', methods=['GET'])
@token_required
def get_all_users():

	if not current_user.admin:
		return jsonify({'message': 'Cannot perform that function!'})

	users= User.query.all()

	output = []

	for user in users:
		user_data= {} 
		user_data['public_id']= user.public_id
		user_data['name']= user.name
		user_data['password']= user.password
		user_data['admin']= user.admin

		output.append(user_data)

	return jsonify({'users' : output})  

@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user,public_id):

	if not current_user.admin:
		return jsonify({'message': 'Cannot perform that function!'})

	user= User.query.filter_by(public_id=public_id).first()

	if not user:
		return jsonify({'message:' : 'No user found!'})

	user_data= {} 
	user_data['public_id']= user.public_id
	user_data['name']= user.name
	user_data['password']= user.password
	user_data['admin']= user.admin

	return jsonify({'user' : user_data})


@app.route('/user',methods=['POST'])
@token_required
def create_user(current_user):

	if not current_user.admin:
		return jsonify({'message': 'Cannot perform that function!'})

	data=request.get_json()

	hashed_password= generate_password_hash(data['password'], method='sha256')

	new_user= User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
	db.session.add(new_user)
	db.session.commit()

	return jsonify({'message' : 'New User Created'})

@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user,public_id):

	if not current_user.admin:
		return jsonify({'message': 'Cannot perform that function!'})

	user= User.query.filter_by(public_id=public_id).first()

	if not user:
		return jsonify({'message:' : 'No user found!'})

	user.admin= True
	db.session.commit()

	return jsonify({'message': 'The user has been promoted to Admin!'}) 

@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):

	if not current_user.admin:
		return jsonify({'message': 'Cannot perform that function!'})

	user= User.query.filter_by(public_id=public_id).first()

	if not user:
		return jsonify({'message:' : 'No user found!'})

	db.session.delete(user)
	db.session.commit()

	return jsonify({'user': 'The user has been deleted'})


@app.route('/login')  #Question 1- When the user login it will generate a JSON token where it will be stored in the Headers section in Postman where they can use the diffrernt routes for the API.
def login():
	auth=request.authorization

	if not auth or not auth.username or not auth.password:
		return make_response('Could not verify',401, {'WWW-Authenticate': 'Basic realm= "Login Required!"' })

	user= User.query.filter_by(name=auth.username).first()
	if not user:
		return make_response('Could not verify',401, {'WWW-Authenticate': 'Basic realm= "Login Required!"' })

	if check_password_hash(user.password,auth.password):
		token=jwt.encode({'public_id': user.public_id , 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])

		return jsonify({'token': token.decode('UTF-8')})

	return make_response('Could not verify',401, {'WWW-Authenticate': 'Basic realm= "Login Required!"' })


#Question 2- When the user is login i.e authenticated they can accesss the dfiiferent routes to perfrom CRUD operations(functions are below) on the events(assuming an event is created.)
#Question 2b- The function get_one_event would deal with searching for one particular event
#Questin 3 - 2 Users already have been created with admin roles in Postman where I called the promote_user function so that they are promoted to Admin(in Screenshots).


#Note: The @token_required decorator ensures that the user is authenticated.

@app.route('/event', methods=['GET'])
@token_required
def get_all_events(current_user):

	if not current_user.admin:
		return jsonify({'message': 'Cannot perform that function!'})

	events= Event.query.filter_by(creator=current_user.id).all()

	output=[]

	for event in events:
		event_data={}
		event_data['id']= event.id
		event_data['title']= event.title
		event_data['name']= event.name
		event_data['description']= event.description
		event_data['category']= event.category
		event_data['start_date_start_time']= event.start_date_start_time
		event_data['end_date_end_time']= event.end_date_end_time
		event_data['cost']= event.cost
		event_data['venue']= event.venue
		event_data['flyer']= event.flyer
		event_data['visible']= event.visible
		event_data['creator']= event.creator
		output.append(event_data)

	return jsonify({'event': output})

@app.route('/event/<event_id>', methods=['GET'])
@token_required
def get_one_event(current_user,event_id):

	event= Event.query.filter_by(id=event_id, creator=current_user.id).first()

	#When searching for an event we are ensuring that the admin has made that event public.
	if not event.visible:
		return jsonify({'message':' Admin has not yet made this event public to be seen'})

	if not event:
		return jsonify({'message': 'No event found'})

	event_data={}
	event_data['id']= event.id
	event_data['title']= event.title
	event_data['name']= event.name
	event_data['description']= event.description
	event_data['category']= event.category
	event_data['start_date_start_time']= event.start_date_start_time
	event_data['end_date_end_time']= event.end_date_end_time
	event_data['cost']= event.cost
	event_data['venue']= event.venue
	event_data['flyer']= event.flyer
	event_data['visible']= event.visible
	event_data['creator']= event.creator

	return jsonify(event_data)


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


			

@app.route('/event',methods=['POST'])
@token_required
def create_event(current_user):  #Question6- Authenticated users can create an event
	data= request.get_json()
	new_event= Event(public_name=str(uuid.uuid4()),title=data['title'], name=data['name'], description=data['description'], category=data['category'], start_date=data['start_date'],start_time=data['start_time'], end_date= data['end_date'],end_time=data['end_time'], cost=data['cost'],venue=data['venue'],visible=False,creator=data['creator'])
	db.session.add(new_event) 
	db.session.commit()

	return jsonify({"message": "Event created!"})
##   
#IMAGE UPLOAD
##
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
@app.route('/upload_flyer/<public_name>', methods=['PUT'])
def upload_file(public_name):
    if request.method == 'PUT':
        if 'file' not in request.files:
            return jsonify({'message':'No file part'})
        file =request.files['file']
        if allowed_file(file.filename):
            # event=Event.query.filter_by(public_name=public_name).first()
            filename=secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            # if name:
            eventimg=EventFlyer(public_name=public_name,flyerPath=os.path.join(app.config['UPLOAD_FOLDER'],filename))
            db.session.add(eventimg)
            db.session.commit()
            return jsonify({'message':'File upload successful'})

@app.route('/event/<event_id>', methods=['PUT'])
@token_required
def set_visible(current_user, event_id):  #Question 4

	event= Event.query.filter_by(id=event_id, creator=current_user.id).first()

	if not current_user.admin:
		return jsonify({'message': 'Cannot perform that function!'})

	event.visible= True 
	db.session.commit()

	return jsonify({'message': 'Event has been set to visible!'})


@app.route('/event/<event_id>', methods=['DELETE'])
@token_required
def delete_event(current_user, event_id):
	event= Event.query.filter_by(id=event_id, user_id=current_user.id).first()

	if not event:
		return jsonify({'message': 'No Event found!'})

	db.session.delete(event)
	db.session.commit()

	return jsonify({'message': 'Event deleted!'})


#Question 6-Non-authenticated so we dont need the @token_required decorator
@app.route('/event/<event_id>/comment', methods=['POST'])  
def comment_event(event_id):
    event= Event.query.filter_by(id=event_id).first()
    if not event:
		        return jsonify({'message': 'No Event found!'})

    data = request.get_json()
    new_Feedback= EventFeedback(email=data['email'],rating=data['rating'],ename=event.name,comment=data['comment'])
    db.session.add(new_Feedback) 
    db.session.commit()
    return jsonify({"message": "Event created!"})
#Extra attributes for comment and rate in User table to be made..



