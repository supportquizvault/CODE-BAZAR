from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to CodeBazaar API on Vercel!", "status": "active"})

if __name__ == "__main__":
    app.run()
