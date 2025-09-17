import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='static')

# ✅ Allow all origins temporarily — guaranteed no CORS errors
CORS(app)

# Load API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY environment variable is not set!")

genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-2.5-flash")

# Serve frontend
@app.route("/")
def home():
    return app.send_static_file("index.html")

@app.route("/<path:path>")
def static_files(path):
    return app.send_static_file(path)

# Chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "Invalid request: 'message' key is missing"}), 400

        user_message = data["message"].strip()
        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        print(f"User message: {user_message}")

        response = model.generate_content([user_message])
        return jsonify({"reply": response.text.strip()})

    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
