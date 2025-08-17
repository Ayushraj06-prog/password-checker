import streamlit as st
import re
import random
import string

# ---------------- Page Setup ----------------
st.set_page_config(page_title="🔐 Password Guardian", page_icon="🔑", layout="centered")

# ---------------- Custom CSS ----------------
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
    }
    .stTextInput > div > div > input {
        background-color: #1e1e2e;
        color: white;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #45a049;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)


# ---------------- Password Strength Function ----------------
def password_strength(password):
    score = 0
    if len(password) >= 8: score += 1
    if re.search(r"[A-Z]", password): score += 1
    if re.search(r"[a-z]", password): score += 1
    if re.search(r"[0-9]", password): score += 1
    if re.search(r"[@$!%*?&#]", password): score += 1
    return score


# ---------------- Password Suggestions ----------------
def suggest_improvements(password):
    suggestions = []
    if len(password) < 8:
        suggestions.append("➡️ Make it at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        suggestions.append("➡️ Add an uppercase letter (A-Z).")
    if not re.search(r"[a-z]", password):
        suggestions.append("➡️ Add a lowercase letter (a-z).")
    if not re.search(r"[0-9]", password):
        suggestions.append("➡️ Include numbers (0-9).")
    if not re.search(r"[@$!%*?&#]", password):
        suggestions.append("➡️ Use special characters (@, #, $, %, &).")

    if not suggestions:
        suggestions.append("✅ Your password looks strong!")
    return suggestions


# ---------------- Random Strong Password Generator ----------------
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


# ---------------- Streamlit App ----------------
st.title("🔐 Password Guardian")
st.write("Check your password strength and get AI-powered suggestions for improvement.")

password = st.text_input("Enter your password:", type="password")

if st.button("Check Strength"):
    if password:
        score = password_strength(password)
        st.progress(score / 5)

        if score <= 2:
            st.error("🔴 Weak Password")
        elif score == 3:
            st.warning("🟡 Medium Password")
        else:
            st.success("🟢 Strong Password")

        # Show analysis
        st.write("### 🔍 Password Analysis")
        st.write(f"- Length: {len(password)}")
        st.write("✅ Uppercase" if re.search(r"[A-Z]", password) else "❌ No uppercase")
        st.write("✅ Lowercase" if re.search(r"[a-z]", password) else "❌ No lowercase")
        st.write("✅ Number" if re.search(r"[0-9]", password) else "❌ No number")
        st.write("✅ Special Character" if re.search(r"[@$!%*?&#]", password) else "❌ No special character")

        # AI-like Suggestions
        st.write("### 🤖 AI Suggestions")
        for tip in suggest_improvements(password):
            st.write(tip)

# Generate random strong password
if st.button("🔑 Generate Strong Password"):
    new_password = generate_password()
    st.success(f"Here’s a strong password: **{new_password}**")
