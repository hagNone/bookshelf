import streamlit as st
import requests

# ======================= CONFIG =======================
BASE_URL = "http://127.0.0.1:8000"

# ==================== SESSION STATE ===================
if 'page' not in st.session_state:
    st.session_state.page = "Login"

if 'email' not in st.session_state:
    st.session_state.email = None

def set_page(page):
    st.session_state.page = page
    st.rerun()

# ======================== UI =========================
st.markdown(
    """
    <style>
        .big-font {font-size:25px !important; font-weight: bold;}
        .container {max-width: 400px; margin: auto; padding: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); border-radius: 10px;}
    </style>
    """,
    unsafe_allow_html=True
)

# ===================== LOGIN PAGE =====================
if st.session_state.page == "Login":
    st.markdown("<div class='container'><p class='big-font'>Login</p></div>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        response = requests.post(f"{BASE_URL}/login/", json={"username": username, "password": password})
        if response.status_code == 200:
            st.success("Login successful!")
        else:
            error_message = response.json().get("error", "Invalid credentials")
            st.error(error_message)

    if st.button("New User? Sign Up"):
        set_page("SignUp")

    if st.button("Forgot Password? Reset Here"):
        set_page("ForgotPassword")

# ==================== SIGN-UP PAGE ====================
elif st.session_state.page == "SignUp":
    st.markdown("<div class='container'><p class='big-font'>Sign Up</p></div>", unsafe_allow_html=True)

    new_username = st.text_input("New Username")
    new_email = st.text_input("Email")
    new_password = st.text_input("New Password", type="password")

    if st.button("Register"):
        response = requests.post(f"{BASE_URL}/register/", json={"username": new_username, "email": new_email, "password": new_password})
        if response.status_code == 201:
            st.success("OTP sent to your email. Verify it.")
            st.session_state.email = new_email
            set_page("VerifyOTP")
        else:
            error_message = response.json().get("error", "Failed to register.")
            st.error(error_message)

    if st.button("Back to Login"):
        set_page("Login")

# ================ OTP VERIFICATION PAGE ================
elif st.session_state.page == "VerifyOTP":
    st.markdown("<div class='container'><p class='big-font'>Verify OTP</p></div>", unsafe_allow_html=True)

    otp = st.text_input("Enter OTP")
    username = st.text_input("Username")
    password = st.text_input("Set Password", type="password")

    if st.button("Verify"):
        response = requests.post(f"{BASE_URL}/verify-otp/", json={"otp": otp, "username": username, "password": password})
        if response.status_code == 201:
            st.success("User verified successfully! You can now log in.")
            set_page("Login")
        else:
            error_message = response.json().get("error", "Invalid OTP or session expired.")
            st.error(error_message)

    if st.button("Back to Sign Up"):
        set_page("SignUp")

# =============== FORGOT PASSWORD PAGE ================
elif st.session_state.page == "ForgotPassword":
    st.markdown("<div class='container'><p class='big-font'>Forgot Password</p></div>", unsafe_allow_html=True)

    reset_email = st.text_input("Enter your registered email")

    if st.button("Send OTP"):
        response = requests.post(f"{BASE_URL}/send-reset-otp/", json={"email": reset_email})
        if response.status_code == 200:
            st.success("OTP sent to your email.")
            st.session_state.email = reset_email
            set_page("ResetPassword")
        else:
            error_message = response.json().get("error", "Failed to send OTP.")
            st.error(error_message)

    if st.button("Back to Login"):
        set_page("Login")

# =============== RESET PASSWORD PAGE ================
elif st.session_state.page == "ResetPassword":
    st.markdown("<div class='container'><p class='big-font'>Reset Password</p></div>", unsafe_allow_html=True)

    otp = st.text_input("Enter OTP")
    new_password = st.text_input("Enter New Password", type="password")

    if st.button("Reset Password"):
        response = requests.post(f"{BASE_URL}/reset-password/", json={"otp": otp, "new_password": new_password})
        if response.status_code == 200:
            st.success("Password reset successfully! You can log in now.")
            set_page("Login")
        else:
            error_message = response.json().get("error", "Invalid OTP or session expired.")
            st.error(error_message)

    if st.button("Back to Login"):
        set_page("Login")
