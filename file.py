import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:8000"])  # Adjust this to your frontend server


# Load API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise Exception("GEMINI_API_KEY environment variable is not set!")

genai.configure(api_key=api_key)

# Initialize Gemini model
model = genai.GenerativeModel(model_name="gemini-2.5-flash")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        print("Received request data:", data)

        if not data or "message" not in data:
            return jsonify({"error": "Invalid request format"}), 400

        user_message = data["message"].strip()
        
        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        print("User message:", user_message)

        # Call Gemini API
        response = model.generate_content([user_message])

        print("Gemini response:", response.text.strip())

        return jsonify({"reply": response.text.strip()})
    except Exception as e:
        print("Exception occurred:", e)
        return jsonify({"error": "Server error occurred"}), 500

#if __name__ == "__main__":
    #app.run(debug=True)
#if __name__ == "__main__":
   # import os
   # port = int(os.environ.get("PORT", 5000))  # Use Render’s PORT or default 5000 locally
    #app.run(host="0.0.0.0", port=port, debug=False)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render provides PORT
    app.run(host="0.0.0.0", port=port)

