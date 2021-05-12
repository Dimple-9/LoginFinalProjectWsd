from flask import Flask, render_template, request, Response, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet
import sendgrid
import os
from dotenv import load_dotenv
from sendgrid.helpers.mail import *
import hashlib
import bcrypt
import re

# Initialize App
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'

# Load env Variables
sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
verification_key = os.getenv('VERIFICATION_KEY')

# Configure Database
db = SQLAlchemy(app)

# User Model
class User(db.Model):
	email = db.Column(db.String(100), primary_key=True)
	password = db.Column(db.String(100))
	salt = db.Column(db.String(100))
	isVerified = db.Column(db.Boolean)

# Login Page
@app.route('/', methods = ['POST', 'GET'])
def login():
	if request.method == 'GET':
		return render_template('index.html')
	else:
		credentials = request.json
		email = credentials["email"]
		password = credentials["password"]

		# Check for Required Fields
		if (not email or not password):
			return Response('{"account-error":"Please fill in all reqiured fields."}', status=400, mimetype='application/json')

		user = User.query.filter_by(email=email).first()
		# Check if User Exists
		if (not user):
			return Response('{"account-error":"Email or password is invalid. Please try again."}', status=400, mimetype='application/json')

		# Check for Correct Password
		if (not hashlib.sha256((password + str(user.salt)).encode('utf-8')).hexdigest() == user.password):
			return Response('{"account-error":"Email or password is invalid. Please try again."}', status=400, mimetype='application/json')
			
		# Check if User is Registered but not Verified
		if (user and not user.isVerified):
			return Response('{"account-error":"You must verify your account before logging in. Please check your email for a verification link."}', status=400, mimetype='application/json')

		# Login Successful
		return Response('{"success":"You have succesfully logged in."}', status=200, mimetype='application/json')
			

# Registration Page
@app.route('/register', methods = ['POST', 'GET'])
def register():
	if request.method == 'GET':
		return render_template('register.html')
	else:
		credentials = request.json
		email = credentials["email"]
		password = credentials["password"]

		# Check for Valid Email
		email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
		if(not re.search(email_regex,email)): 
			return Response('{"email-error":"Please enter a valid email"}', status=400, mimetype='application/json')

		# Check to see if Account is already Registered
		user = User.query.filter_by(email=email).first()
		if user:
			return Response('{"email-error":"An account with this email is already registered."}', status=400, mimetype='application/json')

		# Check for Valid Password
		password_regex = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
		if(not re.search(password_regex,password)): 
			return Response('{"password-error":"Password must be at least 8 characters long, contain at least 1 letter, 1 number, and 1 special character."}', status=400, mimetype='application/json')

		# Proceed to Register User
		salt = bcrypt.gensalt()
		new_user = User(email=email, password=hashlib.sha256((password + str(salt)).encode('utf-8')).hexdigest(), salt=salt, isVerified=False)

	    # Add New User
		db.session.add(new_user)
		db.session.commit()
		
		# Send Verification Email
		f = Fernet(verification_key)
		encrypted_token = f.encrypt(email.encode())
		# print(encrypted_token)

		sg = sendgrid.SendGridAPIClient(sendgrid_api_key)
		from_email = Email(os.getenv('SENDGRID_EMAIL_ADDRESS'))
		to_email = To(email)
		subject = "Email Verification for Flask Project"
		content = Content("text/html", "Visit this link to verify your profile: <b>localhost:5000/verify/"+encrypted_token.decode('utf-8')+"</b>")
		try:
			mail = Mail(from_email, to_email, subject, content)
			response = sg.client.mail.send.post(request_body=mail.get())

			print(response.status_code)
			print(response.body)
			print(response.headers)

		except Exception as e:
			print(e)

		return Response('{"success":"Your account has been created. You will be sent a verification email."}', status=200, mimetype='application/json')

# Account Verification Page
@app.route('/verify/<token>', methods = ['GET', 'POST'])
def verify(token):
	if request.method == 'GET':
		return render_template('verify.html')
	else:
		f = Fernet(verification_key)
		email = f.decrypt(token.encode()).decode('utf-8')
		
		user = User.query.filter_by(email=email).first()

		# Invalid Link if no Corresponding User is Found
		if (not user):
			return Response('{"error":"Verification link is invalid", "isVerified": "false"}', status=400, mimetype='application/json')

		# If User is Already Verified
		if (user.isVerified):
			return Response('{"error":"Your email has already been verified.", "isVerified": "true"}', status=400, mimetype='application/json')

		#  Verify User
		user.isVerified = True
		db.session.commit()
		return Response('{"success":"Your email has been verified! Please log in."}', status=200, mimetype='application/json')

# Application Page
@app.route('/application', methods = ['GET'])
def application():
	return render_template('application.html')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')