from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome to NeuralNet!"})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    return jsonify({"prediction": "placeholder"})

if __name__ == "__main__":
    app.run(debug=True)
