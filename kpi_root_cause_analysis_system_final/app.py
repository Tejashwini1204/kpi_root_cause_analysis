import streamlit as st
from auth import signup_user, login_user
from my_pages import dashboard, analysis, reports

st.set_page_config(layout="wide")

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

[data-testid="stSidebar"] {
    background: #020617;
    border-right: 1px solid #334155;
}

h1, h2, h3 {
    color: #f1f5f9;
}

.stButton>button {
    background: linear-gradient(135deg, #6366f1, #06b6d4);
    color: white;
    border-radius: 10px;
    border: none;
    padding: 8px 16px;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #4f46e5, #0891b2);
}
</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "signup"   # 👈 default page


# ---------------- SIGNUP PAGE ----------------
def signup_page():
    st.title("📝 Signup")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Create Account"):

        if not signup_user(username, password):
            st.error("User already exists")
        else:
            st.success("Account created successfully!")

            # 🔥 Redirect to login
            st.session_state.page = "login"
            st.rerun()

    st.markdown("Already have an account?")
    if st.button("Go to Login"):
        st.session_state.page = "login"
        st.rerun()


# ---------------- LOGIN PAGE ----------------
def login_page():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if login_user(username, password):
            st.session_state.logged_in = True
            st.session_state.user = username
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.markdown("Don't have an account?")
    if st.button("Go to Signup"):
        st.session_state.page = "signup"
        st.rerun()


# ---------------- AUTH ROUTING ----------------
if not st.session_state.logged_in:

    if st.session_state.page == "signup":
        signup_page()

    elif st.session_state.page == "login":
        login_page()

    st.stop()


# ---------------- SIDEBAR ----------------
st.sidebar.success(f"Welcome {st.session_state.user}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.page = "login"
    st.rerun()

page = st.sidebar.radio("Navigation", ["Dashboard", "Analysis", "Reports"])


# ---------------- MAIN TITLE ----------------
st.title("📊 KPI Root Cause Analysis System")


# ---------------- PAGE ROUTING ----------------
if page == "Dashboard":
    dashboard.show()

elif page == "Analysis":
    analysis.show()

elif page == "Reports":
    reports.show()