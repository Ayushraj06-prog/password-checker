import streamlit as st
import re
import math
import random
import string

# ----------------- Page Config -----------------
st.set_page_config(page_title="Pass Guardian", page_icon="🔐", layout="centered")

# ----------------- Theme & Style -----------------
mode = st.sidebar.radio("🌗 Choose Theme", ["Dark Mode", "Light Mode"])

if mode == "Dark Mode":
    st.markdown("""
    <style>
    .stApp {background: linear-gradient(270deg,#1E3C72,#2A5298,#FF512F); background-size:600% 600%; animation: gradientBG 20s ease infinite; color:white;}
    h1,h2,h3,h4,label {color:#fff !important;}
    .glass-card {background: rgba(255,255,255,0.1); backdrop-filter: blur(12px); padding: 20px; border-radius: 15px; margin-bottom: 15px; transition: all 0.3s ease;}
    .strength-bar {border-radius:10px; height:20px;}
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .stApp {background: linear-gradient(270deg,#f8f9fa,#e9ecef,#dee2e6); background-size:600% 600%; animation: gradientBG 20s ease infinite; color:#000;}
    h1,h2,h3,h4,label {color:#000 !important;}
    .glass-card {background: rgba(255,255,255,0.4); backdrop-filter: blur(12px); padding: 20px; border-radius: 15px; margin-bottom: 15px; transition: all 0.3s ease;}
    .strength-bar {border-radius:10px; height:20px;}
    </style>
    """, unsafe_allow_html=True)

# ----------------- Functions -----------------
def check_password_strength(password):
    suggestions = []
    score = 0
    if len(password) >= 12: score += 2
    elif len(password) >= 8: score += 1
    else: suggestions.append("Use at least 12 characters.")
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

def copy_to_clipboard(text):
    st.markdown(f"""
    <input type="text" value="{text}" id="pwd_copy" style="opacity:0; position:absolute; left:-1000px;">
    <script>
    var copyText = document.getElementById("pwd_copy");
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    document.execCommand("copy");
    </script>
    """, unsafe_allow_html=True)

# ----------------- UI -----------------
st.title("🔐 Pass Guardian")
st.subheader("AI-Enhanced Password Strength Checker")

# --- Password Generator (Outside Form) ---
length = st.slider("Password Length for Generator", 8, 24, 16)
if st.button("Generate Strong Password"):
    password_generated = generate_strong_password(length)
    st.session_state['generated_password'] = password_generated
    st.success("Strong password generated! ✅")

# --- Password Form ---
with st.form("password_form"):
    password_input = st.text_input("Enter your password:", value=st.session_state.get('generated_password', ''), type="password")
    submitted = st.form_submit_button("Check Password")

# --- Evaluation after Enter ---
if submitted and password_input:
    strength, score, suggestions = check_password_strength(password_input)
    entropy = estimate_entropy(password_input)
    progress = score / 7
    colors = {"Weak":"#FF4B4B","Moderate":"#FFA500","Strong":"#FFD700","Very Strong":"#00C853"}
    
    # Strength bar
    st.markdown(f"""
    <div class="strength-bar" style="background-color:#e0e0e0;">
        <div style="width:{progress*100}%; background-color:{colors[strength]}; text-align:center; padding:3px 0; color:white;">{strength}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Entropy
    st.markdown(f"### 🔑 Entropy: **{entropy} bits**")
    
    # AI Suggestions
    if suggestions:
        st.markdown('<div class="glass-card"><h3>🔎 Suggestions to Improve:</h3></div>', unsafe_allow_html=True)
        for s in suggestions: st.markdown(f"- {s}")
    else:
        st.success("Your password is very strong! 🚀")
    
    # Copy Button appears only after suggestions
    if st.button("📋 Copy Password"):
        copy_to_clipboard(password_input)
        st.success("Password copied to clipboard!")
