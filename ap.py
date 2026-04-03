import streamlit as st
import requests

st.set_page_config(page_title="Data Exposure Checker", page_icon="🔐")

st.title("🔐 Data Exposure Checker")
st.write("Check if your email was exposed and evaluate password security.")

# -----------------------------
# Password Strength Function
# -----------------------------

def check_password_strength(password):

    if (
        len(password) >= 8
        and any(c.isupper() for c in password)
        and any(c.isdigit() for c in password)
        and any(c in "!@#$%^&*" for c in password)
    ):
        return "Strong"

    elif len(password) >= 6:
        return "Medium"

    else:
        return "Weak"


# -----------------------------
# Email Breach Checker
# -----------------------------

st.header("📧 Email Breach Checker")

email = st.text_input("Enter your email")

if st.button("Check Email Breach"):

    if email == "":
        st.warning("Please enter an email")

    else:

        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"

        headers = {
            "User-Agent": "data-exposure-checker"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:

            breaches = [b["Name"] for b in response.json()]

            st.error("⚠️ Email found in data breaches!")

            for breach in breaches:
                st.warning(breach)

        elif response.status_code == 404:

            st.success("✅ No breaches found")

        else:

            st.error("Error checking breach database")


# -----------------------------
# Password Strength Checker
# -----------------------------

st.header("🔑 Password Strength Checker")

password = st.text_input("Enter password", type="password")

if st.button("Check Password Strength"):

    strength = check_password_strength(password)

    if strength == "Weak":

        st.error("Password Strength: Weak")

        st.info("Suggested strong password: CyberSafe@2026!")

    elif strength == "Medium":

        st.warning("Password Strength: Medium")

    else:

        st.success("Password Strength: Strong")


# -----------------------------
# Risk Score Calculator
# -----------------------------

st.header("📊 Privacy Risk Score")

risk_email = st.text_input("Email for Risk Analysis")
risk_password = st.text_input("Password for Risk Analysis", type="password")

if st.button("Calculate Risk Score"):

    strength = check_password_strength(risk_password)

    score = 100

    if strength == "Weak":
        score -= 50
    elif strength == "Medium":
        score -= 25

    if "@" not in risk_email:
        score -= 20

    if score >= 70:
        risk = "Low"
    elif score >= 40:
        risk = "Medium"
    else:
        risk = "High"

    st.subheader("Result")

    st.write(f"Privacy Score: {score}")
    st.write(f"Risk Level: {risk}")
    st.write(f"Password Strength: {strength}")

    if risk == "High":
        st.error("High Risk 🔴")
    elif risk == "Medium":
        st.warning("Medium Risk 🟡")
    else:
        st.success("Low Risk 🟢")