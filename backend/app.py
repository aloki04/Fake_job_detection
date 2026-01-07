from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import pickle
from keras.preprocessing.sequence import pad_sequences
import os

app = Flask(__name__)
CORS(app)

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths
MODEL_PATH = os.path.join(BASE_DIR, "model", "fake_job_bilstm.keras")
TOKENIZER_PATH = os.path.join(BASE_DIR, "model", "tokenizer.pkl")

# Load model and tokenizer
model = tf.keras.models.load_model(MODEL_PATH)

with open(TOKENIZER_PATH, "rb") as f:
    tokenizer = pickle.load(f)

print("🔥 Model and tokenizer loaded successfully 🔥")

MAX_LEN = 300
THRESHOLD = 0.7


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    text = data.get("text", "").lower()

    if text.strip() == "":
        return jsonify({"error": "No text provided"}), 400

    sequence = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(sequence, maxlen=MAX_LEN)

    prob_fake = float(model.predict(padded)[0][0])

    # Three-zone decision logic
    if prob_fake >= 0.85:
        result = "Fake Job"
        confidence = prob_fake * 100

    elif prob_fake <= 0.35:
        result = "Real Job"
        confidence = (1 - prob_fake) * 100

    else:
        result = "Suspicious / Needs Review"
        confidence = 50.0

    return jsonify({
        "prediction": result,
        "confidence": round(confidence, 2)
    })




if __name__ == "__main__":
    app.run(debug=True)
