import streamlit as st
import re
import math
import random
import string

# ----------------- Page Config -----------------
st.set_page_config(page_title="Pass Guardian", page_icon="🔐", layout="centered")

# ----------------- Theme Toggle -----------------
mode = st.sidebar.radio("🌗 Choose Theme", ["Dark Mode", "Light Mode"])

if mode == "Dark Mode":
    page_bg = """
    <style>
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    .stApp {
        background: linear-gradient(270deg, #1E3C72, #2A5298, #FF512F);
        background-size: 600% 600%;
        animation: gradientBG 15s ease infinite;
        color: white;
    }
    h1, h2, h3, h4, label {
        color: #fff !important;
    }
    .glass-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 15px;
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }
    .password-wrapper {
        position: relative;
        width: 100%;
        margin-bottom: 10px;
    }
    .password-input {
        width: 100%;
        padding: 10px 40px 10px 10px;
        border-radius: 8px;
        border: 1px solid #ccc;
    }
    .toggle-btn {
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        cursor: pointer;
        font-size: 18px;
        color: #888;
    }
    </style>
    """
else:
    page_bg = """
    <style>
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    .stApp {
        background: linear-gradient(270deg, #f8f9fa, #e9ecef, #dee2e6);
        background-size: 600% 600%;
        animation: gradientBG 15s ease infinite;
        color: #000;
    }
    h1, h2, h3, h4, label {
        color: #000 !important;
    }
    .glass-card {
        background: rgba(255,255,255,0.4);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 15px;
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    }
    .password-wrapper {
        position: relative;
        width: 100%;
        margin-bottom: 10px;
    }
    .password-input {
        width: 100%;
        padding: 10px 40px 10px 10px;
        border-radius: 8px;
        border: 1px solid #ccc;
    }
    .toggle-btn {
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        cursor: pointer;
        font-size: 18px;
        color: #555;
    }
    </style>
    """

st.markdown(page_bg, unsafe_allow_html=True)

# ----------------- Password Functions -----------------
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
    entropy = len(password) * math.log2(pool) if pool > 0 else 0
    return round(entropy, 2)

def generate_strong_password(length=16):
    chars = string.ascii_letters + string.digits + "@$!%*?&#"
    return ''.join(random.choices(chars, k=length))

# ----------------- UI -----------------
st.title("🔐 Pass Guardian")
st.subheader("AI-Enhanced Password Strength Checker")

# ----------------- Password Input with Eye Icon -----------------
password_value = ""
form = st.form("password_form")
with form:
    form.markdown("""
    <div class="password-wrapper">
        <input type="password" id="pwd" class="password-input" placeholder="Enter your password">
        <span class="toggle-btn" onclick="togglePassword()">👁️</span>
    </div>
    <script>
    const input = window.parent.document.getElementById('pwd');
    function togglePassword() {
        const pwd = document.getElementById('pwd');
        if (pwd.type === 'password') { pwd.type = 'text'; }
        else { pwd.type = 'password'; }
    }
    </script>
    """, unsafe_allow_html=True)

    submitted = form.form_submit_button("Check Password")

# ----------------- Strong Password Generator -----------------
if st.button("Generate Strong Password"):
    password_value = generate_strong_password()
    st.text_input("Generated Password:", value=password_value, key="gen_pass")

# ----------------- Password Evaluation -----------------
if submitted:
    try:
        # grab value from html input via JS workaround
        password_value = st.session_state.get('pwd_input', '')
    except:
        pass

    if password_value:
        strength, score, suggestions = check_password_strength(password_value)
        entropy = estimate_entropy(password_value)

        progress = score / 7
        strength_colors = {"Weak":"#FF4B4B","Moderate":"#FFA500","Strong":"#FFD700","Very Strong":"#00C853"}

        st.markdown(f"""
        <div style="background-color: #e0e0e0; border-radius:5px; padding:3px; margin-bottom:10px;">
            <div style="width:{progress*100}%; background-color:{strength_colors[strength]};
                        text-align:center; padding:5px 0; border-radius:5px; color:white;">
                {strength}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"### 🔑 Entropy: **{entropy} bits**")
        if suggestions:
            st.markdown('<div class="glass-card"><h3>🔎 Suggestions to Improve:</h3></div>', unsafe_allow_html=True)
            for s in suggestions: st.markdown(f"- {s}")
        else:
            st.success("Your password is very strong! 🚀")
    else:
        st.warning("Please enter a password first.")
