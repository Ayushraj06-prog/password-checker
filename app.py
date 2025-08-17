import streamlit as st
import re
import math
import random
import string

# ----------------- Page Config -----------------
st.set_page_config(page_title="Pass Guardian", page_icon="🔐", layout="centered")

# ----------------- Theme -----------------
mode = st.sidebar.radio("🌗 Choose Theme", ["Dark Mode", "Light Mode"])

if mode == "Dark Mode":
    st.markdown("""
    <style>
    @keyframes gradientBG {0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
    .stApp {background: linear-gradient(270deg,#1E3C72,#2A5298,#FF512F); background-size:600% 600%; animation: gradientBG 15s ease infinite; color:white;}
    h1,h2,h3,h4,label {color:#fff !important;}
    .glass-card {background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); padding: 20px; border-radius: 15px; transition: all 0.3s ease;}
    .glass-card:hover {transform: scale(1.02); box-shadow:0 8px 20px rgba(0,0,0,0.3);}
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    @keyframes gradientBG {0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
    .stApp {background: linear-gradient(270deg,#f8f9fa,#e9ecef,#dee2e6); background-size:600% 600%; animation: gradientBG 15s ease infinite; color:#000;}
    h1,h2,h3,h4,label {color:#000 !important;}
    .glass-card {background: rgba(255,255,255,0.4); backdrop-filter: blur(10px); padding: 20px; border-radius: 15px; transition: all 0.3s ease;}
    .glass-card:hover {transform: scale(1.02); box-shadow:0 8px 20px rgba(0,0,0,0.2);}
    </style>
    """, unsafe_allow_html=True)

# ----------------- Functions -----------------
def check_password_strength(password):
    suggestions = []
    score = 0
    if len(password) >= 12: score += 2
    elif len(password) >= 8: score += 1
    else: suggestions.append("Use at least 12 characters for better security.")
    if re.search(r"[A-Z]", password): score += 1
    else: suggestions.append("Add uppercase letters.")
    if re.search(r"[a-z]", password): score += 1
    else: suggestions.append("Add lowercase letters.")
    if re.search(r"[0-9]", password): score += 1
    else: suggestions.append("Include numbers.")
    if re.search(r"[@$!%*?&#]", password): score += 2
    else: suggestions.append("Use special characters (@, #, $, %, etc.).")
    if score <= 2: strength = "Weak"
    elif score <= 4: strength = "Moderate"
    elif score <= 6: strength = "Strong"
    else: strength = "Very Strong"
    return strength, score, suggestions

def estimate_entropy(password):
    pool = 0
    if re.search(r"[a-z]", password): pool += 26
    if re.search(r"[A-Z]", password): pool += 26
    if re.search(r"[0-9]", password): pool += 10
    if re.search(r"[@$!%*?&#]", password): pool += 10
    return round(len(password) * math.log2(pool) if pool>0 else 0, 2)

def generate_strong_password(length=16):
    chars = string.ascii_letters + string.digits + "@$!%*?&#"
    return ''.join(random.choices(chars, k=length))

# ----------------- UI -----------------
st.title("🔐 Pass Guardian")
st.subheader("AI-Enhanced Password Strength Checker")

# --- Strong Password Generator (outside form) ---
if st.button("Generate Strong Password"):
    password_generated = generate_strong_password()
    st.session_state['pwd_input'] = password_generated
    st.success("Strong password generated! Copy it from below.")
    password = password_generated
else:
    password = st.session_state.get('pwd_input', '')

# --- Password Form with Enter Button ---
with st.form("password_form"):
    password_input = st.text_input("Enter your password:", value=password, key="pwd_input_form")
    submitted = st.form_submit_button("Check Password")

# --- Evaluation on Enter ---
if submitted:
    if password_input:
        strength, score, suggestions = check_password_strength(password_input)
        entropy = estimate_entropy(password_input)
        progress = score / 7
        colors = {"Weak":"#FF4B4B","Moderate":"#FFA500","Strong":"#FFD700","Very Strong":"#00C853"}

        # Strength bar
        st.markdown(f"""
        <div style="background-color:#e0e0e0; border-radius:5px; padding:3px; margin-bottom:10px;">
            <div style="width:{progress*100}%; background-color:{colors[strength]};
            text-align:center; padding:5px 0; border-radius:5px; color:white;">{strength}</div>
        </div>
        """, unsafe_allow_html=True)

        # Entropy
        st.markdown(f"### 🔑 Entropy: **{entropy} bits**")

        # AI-style suggestions
        if suggestions:
            st.markdown('<div class="glass-card"><h3>🔎 Suggestions to Improve:</h3></div>', unsafe_allow_html=True)
            for s in suggestions: st.markdown(f"- {s}")
        else:
            st.success("Your password is very strong! 🚀")

        # --- Copy Button ---
        if st.button("📋 Copy Password"):
            st.experimental_set_query_params()  # workaround to refresh
            st.write("Password copied to clipboard!")
            st.experimental_set_clipboard(password_input)

    else:
        st.warning("Please enter a password first.")
