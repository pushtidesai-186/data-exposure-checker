import csv
import re

def run_audit(email_input, password_input):

    email_input = email_input.lower()
    breaches_found = []

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
            "error": "Dataset not found"
        }

    # Breach score
    num_b = len(breaches_found)

    if num_b == 0:
        breach_score = 0
    elif num_b == 1:
        breach_score = 50
    else:
        breach_score = 80

    # Password strength
    strength = "Weak"
    pw_vulnerability = 100

    if (
        len(password_input) >= 8
        and re.search(r"[A-Z]", password_input)
        and re.search(r"[a-z]", password_input)
        and re.search(r"[0-9]", password_input)
        and re.search(r"[!@#$%^&*]", password_input)
    ):
        strength = "Strong"
        pw_vulnerability = 20

    elif len(password_input) >= 6:
        strength = "Medium"
        pw_vulnerability = 50

    else:
        strength = "Weak"
        pw_vulnerability = 100

    reuse_risk = 80 if strength == "Weak" else 40 if strength == "Medium" else 20

    final_score = (0.40 * breach_score) + (0.30 * pw_vulnerability) + (0.30 * reuse_risk)

    if final_score > 60:
        risk_level = "High"
    elif final_score > 30:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {

        "breaches": breaches_found,
        "password_strength": strength,
        "privacy_score": round(final_score),
        "risk_level": risk_level

    }