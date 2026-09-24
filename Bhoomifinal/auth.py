"""
auth.py — login, signup, and role gating for BHUMI-INSIGHT.
Mirrors the original repo's auth.py: session-based roles, PBKDF2-hashed
credentials, Guest / Researcher / Policymaker / Administrator tiers.
"""

import streamlit as st
import db

ROLES = ["Researcher", "Policymaker", "Administrator"]

DEMO_CREDENTIALS = [
    ("Researcher", "researcher@bhumi.in", "demo123"),
    ("Policymaker", "policymaker@bhumi.in", "demo123"),
    ("Administrator", "admin@bhumi.in", "demo123"),
]


def init_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "role" not in st.session_state:
        st.session_state.role = None
    if "page" not in st.session_state:
        st.session_state.page = "📊 Dashboard"
    if "prefill_email" not in st.session_state:
        st.session_state.prefill_email = ""
    if "prefill_password" not in st.session_state:
        st.session_state.prefill_password = ""


def login(email: str, password: str) -> bool:
    user = db.get_user_by_email(email.strip().lower())
    if user and db.verify_password(password, user["password_hash"]):
        st.session_state.logged_in = True
        st.session_state.user = {"name": user["name"], "email": user["email"]}
        st.session_state.role = user["role"]
        return True
    return False


def login_as_guest():
    st.session_state.logged_in = True
    st.session_state.user = {"name": "Guest User", "email": "guest@bhumi.in"}
    st.session_state.role = "Guest"


def signup(name: str, email: str, password: str, role: str) -> bool:
    return db.create_user(name, email.strip().lower(), password, role)


def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None
    st.session_state.page = "📊 Dashboard"


def require_login():
    """Call at the top of any protected page."""
    if not st.session_state.get("logged_in"):
        st.warning("Please sign in to access this page.")
        st.stop()


def is_guest() -> bool:
    return st.session_state.get("role") == "Guest"
