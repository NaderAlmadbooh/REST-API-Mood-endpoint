"""
_____Credits & Time____

Nader Almadbooh '23
nalmadb1@swarthmore.edu
Swarthmore College 
Spring 2021
Last edited on: March 24th, 2021   at   11:00 PM

_____Purpose____________

The following code is an implementation of a simple REST API with one endpoint: Mood.
The code has been developed upon the request of NEUROFLOW for a potential internship opportunity.
For more information about assignment, check "Backend_Coding_Assessmest.pdf" at the following 
public git repository: 

_____Notes______________

* This implemetation utalizes open-source and public resources, frameworks, modules, and code snippets.
* Check "READ_ME" document for more information and instructions on testing.  
* Much of the code is documented via the flask framework
* Given shortness of code, no seperate files are included except for testing.
* To ensure functionality, install tools in "requirments.txt"

"""
#importing necessary framework 
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

#Creating web app, defining API and adding database(db)
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)




class MoodDataModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	rating = db.Column(db.Integer, nullable=False)
	user_id = db.Column(db.Integer, nullable=False)
	date = db.Column(db.Integer, nullable=False)
	streak = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return f"Mood(id = {id}, rating = {rating}, date = {date}, streak = {streak} )"

	
#Create Database - Must be deleted after first run to preserve processed data. Otherwise,
#data WILL BE LOST and replaced with a new database.
db.create_all()

#utalizing an argument parser to pass information using data instead of directly 
# embedding it to a URL. The information will still be transformed to a URL string 
requested_arguments = reqparse.RequestParser()
requested_arguments.add_argument("rating", type=int, help="***Field not Filled***", required=True)
requested_arguments.add_argument("user_id", type=int, help="***Field not Filled***", required=True)
requested_arguments.add_argument("date", type=int, help="***Field not Filled***", required=True)
requested_arguments.add_argument("streak", type=int, help="***Field not Filled***", required=True)


mood_update_args = reqparse.RequestParser()
mood_update_args.add_argument("rating", type=int, help="***Field not Filled***")
mood_update_args.add_argument("user_id", type=int, help="***Field not Filled***")
mood_update_args.add_argument("date", type=int, help="***Field not Filled***")
mood_update_args.add_argument("streak", type=int, help="***Field not Filled***")

#Determine serialization & serialization limits
#Serves to limit user access to sensitive information
resource_fields = {
	'id': fields.Integer,
	'rating': fields.Integer,
	'date': fields.Integer
}

#Mood endpoint 
class Mood(Resource):
	@marshal_with(resource_fields)
	def get(self, Mood_id):
		result = MoodDataModel.query.filter_by(id=Mood_id).first()
		if not result:
			abort(404, message="The mood entry you requested does NOT exist")
		return result

	@marshal_with(resource_fields)
	def put(self, Mood_id):
		args = requested_arguments.parse_args()
		result = MoodDataModel.query.filter_by(id=Mood_id).first()
		if result:
			abort(409, message="Mood id taken. Try another.")

		mood = MoodDataModel(id=Mood_id, rating=args['rating'], user_id=args['user_id'], date=args['date'], streak=args['streak'])
		db.session.add(mood)
		db.session.commit()
		return mood, 201

	@marshal_with(resource_fields)
	def patch(self, Mood_id):
		args = mood_update_args.parse_args()
		result = MoodDataModel.query.filter_by(id=Mood_id).first()
		if not result:
			abort(404, message="Mood doesn't exist, cannot update")
        # users are only allowed to change rating
		if args['rating']:
			result.rating = args['rating']
	

		db.session.commit()

		return result


	def delete(self, Mood_id):
		abort_if_Mood_id_doesnt_exist(Mood_id)
		del Mood[Mood_id]
		return '', 204

#creating route for Mood endpoint
api.add_resource(Mood, "/Mood/<int:Mood_id>")


if __name__ == "__main__":
	# pass argument (debug=True) only in development environment 
	# erase argument (debug=True) in production environemnt 
	app.run(debug=True)
