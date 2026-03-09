import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:5000"

st.title("🔐 Data Exposure Checker")

# -------------------------
# Email Breach Checker
# -------------------------

st.header("Email Breach Checker")

email = st.text_input("Enter Email")

if st.button("Check Email Breach"):

    response = requests.post(
        f"{BACKEND_URL}/check-email",
        json={"email": email}
    )

    data = response.json()

    st.write(data["message"])

    if data["breaches"]:

        st.subheader("Breached Platforms")

        for breach in data["breaches"]:
            st.warning(breach)


# -------------------------
# Password Strength Checker
# -------------------------

st.header("Password Strength Checker")

password = st.text_input("Enter Password", type="password")

if st.button("Check Password Strength"):

    response = requests.post(
        f"{BACKEND_URL}/check-password",
        json={"password": password}
    )

    if response.status_code == 200:

        data = response.json()
        strength = data["passwordStrength"]

        if strength == "Weak":

            st.error(f"Password Strength: {strength}")

            st.info(
                "Suggested Strong Password Example: CyberSafe@2026!"
            )

            st.caption(
                "Tip: Use at least 8 characters including uppercase, lowercase, numbers and special symbols."
            )

        elif strength == "Medium":

            st.warning(f"Password Strength: {strength}")

            st.caption(
                "Tip: Add special characters like ! @ # $ to make your password stronger."
            )

        else:

            st.success(f"Password Strength: {strength}")

            st.caption(
                "Great! Your password follows good security practices."
            )

    else:
        st.error("Unable to check password strength.")


# -------------------------
# Risk Score Dashboard
# -------------------------

st.header("Risk Score Checker")

risk_email = st.text_input("Email for Risk Check")
risk_password = st.text_input("Password for Risk Check", type="password")

if st.button("Check Risk Score"):

    response = requests.post(
        f"{BACKEND_URL}/risk-score",
        json={
            "email": risk_email,
            "password": risk_password
        }
    )

    if response.status_code == 200:

        data = response.json()

        st.subheader("Risk Result")

        st.write(f"Privacy Score: {data['privacy_score']}")
        st.write(f"Risk Level: {data['risk_level']}")
        st.write(f"Password Strength: {data['password_strength']}")

        if data["risk_level"] == "High":
            st.error("High Risk 🔴")

        elif data["risk_level"] == "Medium":
            st.warning("Medium Risk 🟡")

        else:
            st.success("Low Risk 🟢")

    else:
        st.error("Backend error")