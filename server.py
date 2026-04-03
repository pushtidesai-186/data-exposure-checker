from flask import Flask, request, jsonify
from flask_cors import CORS
from analyzer import run_audit

# ✅ Create app FIRST
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
def check_email():

    try:
        data = request.json
        email = data.get("email")

        result = run_audit(email, "Dummy123!")

        breaches = result.get("breaches", [])

        if breaches:
            message = f"⚠ Email found in {len(breaches)} breach(es)"
        else:
            message = "✅ No breach found"

        return jsonify({
            "message": message,
            "breaches": breaches
        })

    except Exception as e:
        return jsonify({
            "message": "Error checking email",
            "error": str(e),
            "breaches": []
        }), 500


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