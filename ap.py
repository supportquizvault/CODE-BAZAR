from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# MongoDB Configuration
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://localhost:27017/codebazaar")
mongo = PyMongo(app)

# 1. Home / Status Route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to CodeBazaar API", "status": "active"}), 200

# 2. Get All Code Snippets
@app.route("/api/snippets", methods=["GET"])
def get_snippets():
    snippets = []
    for snippet in mongo.db.snippets.find():
        snippets.append({
            "id": str(snippet["_id"]),
            "title": snippet.get("title"),
            "category": snippet.get("category"),
            "price": snippet.get("price"),
            "author": snippet.get("author")
        })
    return jsonify(snippets), 200

# 3. Upload a New Code Snippet (Seller Feature)
@app.route("/api/snippets", methods=["POST"])
def add_snippet():
    data = request.json
    
    if not data or not data.get("title") or not data.get("price"):
        return jsonify({"error": "Missing required fields"}), 400
        
    new_snippet = {
        "title": data.get("title"),
        "category": data.get("category"),
        "price": data.get("price"),
        "author": data.get("author", "Anonymous"),
        "file_url": data.get("file_url")
    }
    
    result = mongo.db.snippets.insert_one(new_snippet)
    return jsonify({"message": "Snippet uploaded successfully", "id": str(result.inserted_id)}), 201

# 4. User Signup Route
@app.route("/api/auth/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    
    if mongo.db.users.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 400
        
    user_id = mongo.db.users.insert_one({
        "username": data.get("username"),
        "email": email,
        "password": data.get("password")  # Note: Hash passwords using bcrypt in production
    })
    
    return jsonify({"message": "User registered successfully", "user_id": str(user_id.inserted_id)}), 201

if __name__ == "__main__":
    app.run(debug=True, port=5000)
