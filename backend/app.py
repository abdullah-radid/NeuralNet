from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    # TODO: load your model and run inference here
    return jsonify({"prediction": "placeholder"})

if __name__ == "__main__":
    app.run(debug=True)
