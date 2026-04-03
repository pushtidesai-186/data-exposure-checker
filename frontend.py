import streamlit as st
from analyzer import run_audit

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="Data Exposure Checker", layout="centered")

# -------------------------
# CUSTOM CSS (🔥 PREMIUM UI)
# -------------------------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    background: linear-gradient(to right, #38bdf8, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.1);
}

.badge {
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 14px;
    display: inline-block;
}

.green { background: #16a34a; }
.yellow { background: #facc15; color:black; }
.red { background: #dc2626; }

</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER
# -------------------------
st.markdown('<div class="title">🔐 Data Exposure Checker</div>', unsafe_allow_html=True)
st.write("### Check your email exposure & password security")

# -------------------------
# EMAIL CHECKER
# -------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📧 Email Breach Checker")

email = st.text_input("Enter your email")

if st.button("Check Email Breach"):
    result = run_audit(email, "Dummy123!")

    if "error" in result:
        st.error(result["error"])

    elif result["breaches"]:
        st.markdown('<span class="badge red">⚠ Breach Found</span>', unsafe_allow_html=True)

        for breach in result["breaches"]:
            st.warning(f"🔎 {breach}")

    else:
        st.markdown('<span class="badge green">✅ Safe</span>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# PASSWORD CHECKER
# -------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🔑 Password Strength Checker")

password = st.text_input("Enter password", type="password")

if st.button("Check Password Strength"):
    result = run_audit("test@gmail.com", password)
    strength = result["password_strength"]

    if strength == "Weak":
        st.markdown('<span class="badge red">Weak Password</span>', unsafe_allow_html=True)
        st.info("💡 Try: CyberSafe@2026!")

    elif strength == "Medium":
        st.markdown('<span class="badge yellow">Medium Password</span>', unsafe_allow_html=True)

    else:
        st.markdown('<span class="badge green">Strong Password</span>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# RISK SCORE
# -------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📊 Privacy Risk Score")

risk_email = st.text_input("Email for Risk Analysis")
risk_password = st.text_input("Password for Risk Analysis", type="password")

if st.button("Check Risk Score"):
    result = run_audit(risk_email, risk_password)

    score = result["privacy_score"]
    level = result["risk_level"]

    st.write(f"### Score: {score}/100")

    # 🔥 VISUAL BAR
    st.progress(score)

    if level == "High":
        st.markdown('<span class="badge red">🔴 High Risk</span>', unsafe_allow_html=True)

    elif level == "Medium":
        st.markdown('<span class="badge yellow">🟡 Medium Risk</span>', unsafe_allow_html=True)

    else:
        st.markdown('<span class="badge green">🟢 Low Risk</span>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)