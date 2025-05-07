from flask import Flask, request, jsonify
from datetime import datetime
import random

app = Flask(__name__)
discussions = []
def generate_random_username():
    return f"User{random.randint(10000, 99999)}"

@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome to NeuralNet!"})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    return jsonify({"prediction": "placeholder"})

@app.route("/api/discussions", methods=["POST"])
def create_discussion():
    data = request.get_json()

    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({"error": "Title and Content are required"}), 400

    new_discussion = {
        "id": len(discussions) + 1,
        "randomName": generate_random_username(),
        "title": title,
        "content": content,
        "createdAt": datetime.now().isoformat(),
        "upvotes": 0
    }
    discussions.append(new_discussion)
    return jsonify(new_discussion), 201

@app.route("/api/discussions", methods=["GET"])
def get_discussions():
    return jsonify(discussions)

@app.route("/api/discussions/<int:discussion_id>/upvote", methods=["POST"])
def upvote_discussion(discussion_id):
    for discussion in discussions:
        if discussion["id"] == discussion_id:
            discussion["upvotes"] += 1
            return jsonify({"upvotes": discussion["upvotes"]})
    return jsonify({"error": "Discussion not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
