from flask import Flask, request, jsonify
from flask_cors import CORS
from analyzer import run_audit

app = Flask(__name__)
CORS(app)

# -------------------------
# Home Route
# -------------------------

@app.route("/")
def home():
    return jsonify({"message": "Data Exposure Checker Backend Running"})


# -------------------------
# Email Breach Checker
# -------------------------

@app.route("/check-email", methods=["POST"])
def check_email_breach(email):
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {"User-Agent": "streamlit-app"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return "Email found in breaches"
    elif response.status_code == 404:
        return "No breach found"
    else:
        return "Error checking breach"


# -------------------------
# Password Strength Checker
# -------------------------

@app.route("/check-password", methods=["POST"])
def check_password():

    data = request.json
    password = data.get("password")

    if (
        len(password) >= 8
        and any(c.isupper() for c in password)
        and any(c.isdigit() for c in password)
        and any(c in "!@#$%^&*" for c in password)
    ):
        strength = "Strong"

    elif len(password) >= 6:
        strength = "Medium"

    else:
        strength = "Weak"

    return jsonify({
        "passwordStrength": strength
    })


# -------------------------
# Risk Score
# -------------------------

@app.route("/risk-score", methods=["POST"])
def risk_score():

    data = request.json

    email = data.get("email")
    password = data.get("password")

    result = run_audit(email, password)

    return jsonify({
        "privacy_score": result["privacy_score"],
        "risk_level": result["risk_level"],
        "password_strength": result["password_strength"]
    })


# -------------------------
# Run Server
# -------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)