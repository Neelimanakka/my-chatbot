import os
import google.generativeai as genai
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

app = Flask(__name__, static_folder=".", static_url_path="")  
# static_folder="." → serves your index.html, script.js, style.css
CORS(app)  # Allow all origins

# Load API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise Exception("GEMINI_API_KEY environment variable is not set!")

genai.configure(api_key=api_key)

# Initialize Gemini model
model = genai.GenerativeModel(model_name="gemini-2.5-flash")

# Serve frontend
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

# Chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "Invalid request format"}), 400

        user_message = data["message"].strip()
        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        # Call Gemini API
        response = model.generate_content([user_message])
        return jsonify({"reply": response.text.strip()})
    except Exception as e:
        print("Exception:", e)
        return jsonify({"error": "Server error occurred"}), 500

# Render deployment entry
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port)
