from flask import Flask, request, jsonify
from flask_cors import CORS
import re
from analyzer import run_audit

app = Flask(__name__)
CORS(app)

# ----------------------
# Home Route
# ----------------------
@app.route("/")
def home():
    return jsonify({"message": "Data Exposure Checker Backend Running"})


# ----------------------
# Email Breach Checker
# ----------------------
@app.route("/check-email", methods=["POST"])
def check_email():

    data = request.json
    email = data.get("email")

    result = run_audit(email, "Dummy123!")

    breaches = result["breaches"]

    if breaches:
        message = f"⚠️ Email found in {len(breaches)} breach(es)"
    else:
        message = "✅ No breach found"

    return jsonify({
        "message": message,
        "breaches": breaches
    })


# ----------------------
# Password Strength Checker
# ----------------------
@app.route("/check-password", methods=["POST"])
def check_password():

    data = request.json
    password = data.get("password", "")

    if (
        len(password) >= 8
        and re.search(r"[A-Z]", password)
        and re.search(r"[0-9]", password)
        and re.search(r"[!@#$%^&*]", password)
    ):
        strength = "Strong"

    elif len(password) >= 6:
        strength = "Medium"

    else:
        strength = "Weak"

    return jsonify({
        "passwordStrength": strength
    })


# ----------------------
# Privacy Risk Score
# ----------------------
@app.route("/risk-score", methods=["POST"])
def risk_score():

    data = request.json

    email = data.get("email")
    password = data.get("password")

    result = run_audit(email, password)

    return jsonify({
        "privacy_score": result["privacy_score"],
        "risk_level": result["risk_level"],
        "password_strength": result["password_strength"],
        "breaches": result["breaches"]
    })


# ----------------------
# Run Server
# ----------------------
if __name__ == "__main__":
    app.run(debug=True)