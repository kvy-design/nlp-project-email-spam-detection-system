import os
import sys
import json
from flask import Flask, render_template, request, jsonify

# Add src to sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
from predict import analyze_message

app = Flask(__name__)

# Sample emails for one-click testing
SAMPLE_EMAILS = {
    "legitimate": (
        "Hi team, just a reminder about our project sync scheduled for tomorrow at 10 AM. "
        "Please review the attached sprint progress deck before the call. Let me know if you have questions!"
    ),
    "spam": (
        "CONGRATULATIONS! You have been selected as the grand winner of a $1000 Walmart Gift Card! "
        "Claim your exclusive reward now! 80% discount on luxury watches. Unsubscribe anytime."
    ),
    "phishing": (
        "URGENT: Your PayPal account has been temporarily restricted due to unauthorized login attempts. "
        "Verify your identity immediately at http://192.168.1.10/paypal-verify or your account will be permanently closed!"
    )
}

@app.route("/")
def index():
    return render_template("index.html", samples=SAMPLE_EMAILS)

@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)
        text = data.get("text", "")
        if not text.strip():
            return jsonify({"error": "Please enter an email or message to analyze."}), 400
        
        result = analyze_message(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/metrics", methods=["GET"])
def metrics():
    metrics_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "metrics.json")
    if os.path.exists(metrics_path):
        with open(metrics_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)
    return jsonify({"error": "Metrics not found. Run training first."}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Email Spam & Phishing Detection Web App on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
