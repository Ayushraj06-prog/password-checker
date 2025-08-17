import streamlit as st
import re

# ----------------- Page Config -----------------
st.set_page_config(page_title="Pass Guardian", page_icon="🔐", layout="centered")

# ----------------- Theme Toggle -----------------
mode = st.sidebar.radio("🌗 Choose Theme", ["Dark Mode", "Light Mode"])

if mode == "Dark Mode":
    page_bg = """
    <style>
    .stApp {
        background: linear-gradient(135deg, #1E3C72 0%, #2A5298 50%, #FF512F 100%);
        color: white;
    }
    h1, h2, h3, h4, label {
        color: #fff !important;
    }
    </style>
    """
else:
    page_bg = """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 50%, #dee2e6 100%);
        color: #000;
    }
    h1, h2, h3, h4, label {
        color: #000 !important;
    }
    </style>
    """

st.markdown(page_bg, unsafe_allow_html=True)

# ----------------- Password Strength Function -----------------
def check_password_strength(password):
    suggestions = []
    score = 0

    # Length check
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 12 characters for better security.")

    # Uppercase
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Add uppercase letters.")

    # Lowercase
    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Add lowercase letters.")

    # Numbers
    if re.search(r"[0-9]", password):
        score += 1
    else:
        suggestions.append("Include numbers.")

    # Special characters
    if re.search(r"[@$!%*?&#]", password):
        score += 2
    else:
        suggestions.append("Use special characters (@, #, $, %, etc.).")

    # Final Strength
    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Moderate"
    elif score <= 6:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return strength, score, suggestions

# ----------------- UI -----------------
st.title("🔐 Pass Guardian")
st.subheader("AI-Enhanced Password Strength Checker")

password = st.text_input("Enter your password:", type="password")

if password:
    strength, score, suggestions = check_password_strength(password)

    # Progress bar (max score = 7)
    progress = score / 7
    st.progress(progress)

    # Strength result
    st.markdown(f"### ✅ Strength: **{strength}**")

    # Suggestions
    if suggestions:
        st.markdown("### 🔎 Suggestions to Improve:")
        for s in suggestions:
            st.markdown(f"- {s}")
    else:
        st.success("Your password is very strong! 🚀")
