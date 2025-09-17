import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='static')
CORS(app)  # ✅ Allow requests from all origins

# Load API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY environment variable is not set!")

genai.configure(api_key=api_key)

# Initialize Gemini model
model = genai.GenerativeModel(model_name="gemini-2.5-flash")

# Serve frontend files
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

        # Generate response using Gemini API
        response = model.generate_content([user_message])
        return jsonify({"reply": response.text.strip()})

    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# Render deployment port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
