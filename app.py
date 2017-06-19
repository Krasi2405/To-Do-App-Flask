from flask import  (Flask, render_template, make_response,
					redirect, request, url_for, flash)

import json
import pdb

users = []

app = Flask(__name__)
app.secret_key = "ofsajpiofjeiwjg09w0ejgfajodf9hew809g092uja012-$90ash"

def get_saved_data(data_name = "list_info"):
	try:
		data = json.loads(request.cookies.get(data_name))
	except TypeError:
		data = []
	return data

@app.route("/")
@app.route("/index")
@app.route("/index/<string:list_name>")
def index(list_name = "unselected"):
	data = get_saved_data(list_name)
	data = sorted(data, key = lambda x: x['priority'])
	lists = get_saved_data("lists")
	return render_template("index.html", data = data, list_name = list_name, lists = lists)

@app.route("/save/<string:list_name>", methods = ["POST"])
def save(list_name):
	data = get_saved_data(list_name)
	data.append(dict(request.form.items()))
	response = make_response(redirect(url_for("index", list_name = list_name)))
	response.set_cookie(list_name, json.dumps(data))
	return response

@app.route("/delete_all/<string:list_name>", methods = ["POST"])
def delete_all(list_name):
	data = []
	response = make_response(redirect(url_for("index", list_name = list_name)))
	response.set_cookie(list_name, json.dumps(data))
	return response

@app.route("/delete_item/<string:list_name>", methods = ["POST"])
def delete_item(list_name):
	data = get_saved_data(list_name);
	try: 
		index = int(request.form["index"])
		if(index < 1 or index > len(data)):
			flash("Element doesnt exist!")
		else:
			data.pop(index - 1)
	except ValueError:
		flash("Enter a value!");
	
	response = make_response(redirect(url_for("index", list_name = list_name)))
	response.set_cookie(list_name, json.dumps(data))
	return response;


@app.route("/add_list/<string:list_name>", methods = ["POST"])
def add_list(list_name):
	lists = get_saved_data("lists")
	lists.append(request.form["list_name"])
	response = make_response(redirect(url_for("index", list_name = list_name)))
	response.set_cookie("lists", json.dumps(lists))
	return response


@app.route("/remove_list/<string:list_name>", methods = ["POST"])
def remove_list(list_name):
	lists = get_saved_data("lists")
	index = int(request.form["list_index"])
	if index >= 1 and index <= len(lists):
		
		list_name = "unselected"
		response = make_response(redirect(url_for("index", list_name = list_name)))
		response.set_cookie(lists[index - 1], "", expires = 0)
		del lists[index - 1]
		response.set_cookie("lists", json.dumps(lists))

		return response 
	else:
		response = make_response(redirect(url_for("index", list_name = list_name)))
		flash("Index out of range.")
		return response

if __name__ == '__main__':
	app.run(debug = True)
