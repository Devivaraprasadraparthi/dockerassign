from flask import Flask, render_template, redirect, url_for
from flask import request, jsonify
from datetime import datetime
from dotenv import load_dotenv
import os
import pymongo
from flask_cors import CORS

load_dotenv()  # Load environment variables from .env file
MONGO_URI = os.getenv('MONGO_URI', "mongodb://127.0.0.1:27017/")  # Get the MongoDB URI from environment variables

client = pymongo.MongoClient(MONGO_URI )
db = client.test
collection = db['mydb']
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    day_of_week = [datetime.today().strftime("%A")]  # Placeholder for the current day of the week
    current_time = datetime.now().strftime("%I:%M %p")  # Get current time in 12-hour format

    return render_template("index.html", day_of_week=day_of_week, current_time=current_time)


@app.route("/api/users", methods=["GET"])
def get_users():
    try:
        users = list(collection.find())
        for user in users:
            user["_id"] = str(user["_id"])
        return jsonify(users), 200
    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500


@app.route("/login", methods=["POST", "GET"])
def login():
    try:
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template("index.html", error="Username and password are required.")

        collection.insert_one({
            "username": username,
            "password": password
        })

        return redirect(url_for("success"))

    except Exception as error:
        return render_template("index.html", error=f"Error: {error}")


@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0' , port=5000)
    