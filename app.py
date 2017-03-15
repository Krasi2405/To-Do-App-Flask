from flask import  (Flask, render_template, make_response,
					redirect, request, url_for, flash)

import json

import pdb

users = []

app = Flask(__name__)
app.secret_key = "ofsajpiofjeiwjg09w0ejgfajodf9hew809g092uja012-$90ash"

def get_saved_data():
	try:
		data = json.loads(request.cookies.get('list_info'))
	except TypeError:
		data = []
	return data

@app.route("/")
@app.route("/index")
def index():
	data = get_saved_data()
	return render_template("index.html", data = data)

@app.route("/save", methods = ["POST"])
def save():
	data = get_saved_data()
	data.append(dict(request.form.items()))
	response = make_response(redirect(url_for("index")))
	response.set_cookie('list_info', json.dumps(data))
	return response

@app.route("/delete_all", methods = ["POST"])
def delete_all():
	data = []
	response = make_response(redirect(url_for("index")))
	response.set_cookie('list_info', json.dumps(data))
	return response

@app.route("/delete_item", methods = ["POST"])
def delete_item():
	data = get_saved_data();
	try: 
		index = int(request.form["index"])
		if(index < 1 or index > len(data)):
			flash("Element doesnt exist!")
		else:
			data.pop(index - 1)
	except ValueError:
		flash("Enter a value!");
	

	response = make_response(redirect(url_for("index")))
	response.set_cookie('list_info', json.dumps(data))
	return response;

app.run(debug = True)