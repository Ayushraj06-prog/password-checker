import re
import streamlit as st

def password_strength(password: str):
    score = 0
    remarks = []

    if len(password) >= 8:
        score += 1
    else:
        remarks.append("Password should be at least 8 characters long.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        remarks.append("Add at least one uppercase letter.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        remarks.append("Add at least one lowercase letter.")

    if re.search(r"\d", password):
        score += 1
    else:
        remarks.append("Add at least one digit.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        remarks.append("Add at least one special character (!@#$ etc.).")

    if score <= 2:
        strength = "Weak"
    elif score in [3, 4]:
        strength = "Moderate"
    else:
        strength = "Strong"

    return strength, score, remarks

# Streamlit UI
st.title("🔐 Password Strength Checker")
password = st.text_input("Enter your password:", type="password")

if st.button("Check Strength"):
    strength, score, remarks = password_strength(password)
    st.write(f"**Strength:** {strength}")
    st.write(f"**Score:** {score}/5")
    if remarks:
        st.write("Suggestions:")
        for r in remarks:
            st.write(f"- {r}")
