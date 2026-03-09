import csv
import re


def run_audit(email_input, password_input):

    email_input = email_input.strip().lower()
    breaches_found = []

    # -----------------------------
    # SEARCH EMAIL IN DATASET
    # -----------------------------
    try:
        with open("breach_data.csv", mode="r") as file:

            reader = csv.DictReader(file)

            for row in reader:
                if row["email"].lower() == email_input:
                    breaches_found.append(
                        f"{row['breach']} ({row['year']})"
                    )

    except FileNotFoundError:
        return {
            "error": "breach_data.csv not found"
        }

    # -----------------------------
    # BREACH SCORE (40%)
    # -----------------------------
    num_b = len(breaches_found)

    if num_b == 0:
        breach_score = 0
    elif num_b == 1:
        breach_score = 50
    else:
        breach_score = 80


    # -----------------------------
    # PASSWORD STRENGTH ANALYSIS
    # -----------------------------
    strength = "Weak"
    pw_vulnerability = 100

    # STRONG PASSWORD
    if (
        len(password_input) >= 8
        and re.search(r"[A-Z]", password_input)
        and re.search(r"[a-z]", password_input)
        and re.search(r"[0-9]", password_input)
        and re.search(r"[!@#$%^&*]", password_input)
    ):
        strength = "Strong"
        pw_vulnerability = 20

    # MEDIUM PASSWORD
    elif (
        len(password_input) >= 6
        and (
            re.search(r"[A-Z]", password_input)
            or re.search(r"[0-9]", password_input)
        )
    ):
        strength = "Medium"
        pw_vulnerability = 50

    # WEAK PASSWORD
    else:
        strength = "Weak"
        pw_vulnerability = 100


    # -----------------------------
    # PASSWORD REUSE RISK (30%)
    # -----------------------------
    if strength == "Weak":
        reuse_risk = 80
    elif strength == "Medium":
        reuse_risk = 50
    else:
        reuse_risk = 30


    # -----------------------------
    # FINAL RISK SCORE
    # -----------------------------
    final_score = (
        (0.40 * breach_score)
        + (0.30 * pw_vulnerability)
        + (0.30 * reuse_risk)
    )


    # -----------------------------
    # RISK LEVEL
    # -----------------------------
    if final_score > 60:
        risk_level = "High"
    elif final_score > 30:
        risk_level = "Medium"
    else:
        risk_level = "Low"


    # -----------------------------
    # RETURN RESULT
    # -----------------------------
    return {

        "email": email_input,

        "breaches": breaches_found,

        "password_strength": strength,

        "privacy_score": round(final_score),

        "risk_level": risk_level

    }