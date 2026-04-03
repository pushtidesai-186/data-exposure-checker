import pandas as pd
import re
import os

def run_audit(email_input, password_input):

    try:
        # -------------------------
        # LOAD CSV SAFELY
        # -------------------------
        file_path = os.path.join(os.path.dirname(__file__), "breach_data.csv")

        df = pd.read_csv(file_path)

        # Clean column names
        df.columns = df.columns.str.strip().str.lower()

        # Validate required columns
        required_cols = ["email", "breach", "year"]
        for col in required_cols:
            if col not in df.columns:
                return {"error": f"Missing column: {col}"}

        # -------------------------
        # EMAIL MATCHING
        # -------------------------
        email_input = email_input.strip().lower()

        df["email"] = df["email"].astype(str).str.strip().str.lower()

        matches = df[df["email"] == email_input]

        breaches_found = []

        for _, row in matches.iterrows():
            breaches_found.append(f"{row['breach']} ({row['year']})")

    except Exception as e:
        return {"error": f"CSV Error: {str(e)}"}

    # -------------------------
    # PASSWORD STRENGTH
    # -------------------------
    strength = "Weak"

    if (
        len(password_input) >= 8
        and re.search(r"[A-Z]", password_input)
        and re.search(r"[a-z]", password_input)
        and re.search(r"[0-9]", password_input)
        and re.search(r"[!@#$%^&*]", password_input)
    ):
        strength = "Strong"

    elif len(password_input) >= 6:
        strength = "Medium"

    # -------------------------
    # RISK CALCULATION
    # -------------------------
    breach_score = len(breaches_found) * 40

    if strength == "Weak":
        password_score = 80
    elif strength == "Medium":
        password_score = 40
    else:
        password_score = 10

    final_score = min(100, breach_score + password_score)

    if final_score > 70:
        risk_level = "High"
    elif final_score > 40:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    # -------------------------
    # FINAL OUTPUT
    # -------------------------
    return {
        "breaches": breaches_found,
        "password_strength": strength,
        "privacy_score": final_score,
        "risk_level": risk_level
    }