import os
import google.generativeai as genai
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

app = Flask(__name__, static_folder=".", static_url_path="")

# ✅ Allow only your frontend domain
CORS(app, resources={
    r"/chat": {"origins": "https://my-chatbot-3pmw.onrender.com"}
})

# ✅ Load API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise Exception("GEMINI_API_KEY environment variable is not set!")

genai.configure(api_key=api_key)

# ✅ Initialize Gemini model
model = genai.GenerativeModel(model_name="gemini-2.5-flash")

# ✅ Serve frontend (index.html)
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

# ✅ Chat endpoint (POST + OPTIONS for preflight CORS)
@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        # Preflight CORS request
        response = jsonify({"status": "ok"})
        response.headers.add("Access-Control-Allow-Origin", "https://my-chatbot-3pmw.onrender.com")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "POST,OPTIONS")
        return response, 200

    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "Invalid request format"}), 400

        user_message = data["message"].strip()
        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        print("👉 User message:", user_message)  # Debug log

        # ✅ Call Gemini API (string, not list)
        response = model.generate_content(user_message)

        print("👉 Gemini raw response:", response)  # Debug log

        return jsonify({"reply": response.text.strip()})
    #except Exception as e:
        # Print error in logs for Render
        #print("❌ Exception:", e)
       # return jsonify({"error": "Server error occurred"}), 500
    except Exception as e:
        error_message = str(e)
        print("❌ Exception:", error_message)  # Logs in Render
        return jsonify({"error": f"Server error: {error_message}"}), 500


# ✅ Render deployment entry
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
