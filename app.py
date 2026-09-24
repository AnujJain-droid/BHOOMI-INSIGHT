"""
app.py — BHUMI-INSIGHT
Streamlit prototype for SIH26019 — Evidence-Based Land Governance.

Restyled clone of the reference repo (bhoominiti-ai) to match the
BHUMI-INSIGHT navy/green design reference. Same stack: Streamlit + SQLite
+ Folium + Plotly. Authentication is mandatory before any module loads.
"""

import streamlit as st

import auth
import db
import style
from pages_bh import dashboard, land_records, gis_explorer, policy_lab, reports, settings

st.set_page_config(page_title="BHUMI-INSIGHT", page_icon="\U0001F30F", layout="wide")

db.init_db()
auth.init_session_state()

# Sidebar is fully collapsed/hidden on the login screen, restored after login.
style.inject_css(hide_sidebar=not st.session_state.logged_in)


def render_login():
    style.login_header()

    left, mid, right = st.columns([1, 1.3, 1])
    with mid:
        st.markdown("<h2 class='login-title'>Welcome Back</h2>", unsafe_allow_html=True)
        st.markdown(
            "<p class='login-subtitle'>Sign in to access the BHUMI-INSIGHT platform</p>",
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])

            with tab_login:
                role = st.selectbox("Role", auth.ROLES, key="login_role")
                email = st.text_input("Email", value=st.session_state.prefill_email, placeholder="you@bhumi.in")
                password = st.text_input(
                    "Password", value=st.session_state.prefill_password, type="password", placeholder="demo123"
                )

                if st.button("Sign In", use_container_width=True, type="primary"):
                    if auth.login(email, password):
                        st.session_state.page = "Dashboard"
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")

                st.markdown(
                    "<div style='text-align:center;color:#94a3b8;margin:10px 0;'>or</div>",
                    unsafe_allow_html=True,
                )
                if st.button("Continue as Guest", use_container_width=True):
                    auth.login_as_guest()
                    st.session_state.page = "Dashboard"
                    st.rerun()

            with tab_signup:
                name = st.text_input("Full Name")
                new_role = st.selectbox("Role", auth.ROLES, key="signup_role")
                new_email = st.text_input("Email", key="signup_email", placeholder="you@bhumi.in")
                new_password = st.text_input("Password", key="signup_password", type="password")

                if st.button("Create Account", use_container_width=True, type="primary"):
                    if not name or not new_email or not new_password:
                        st.error("Please fill in all fields.")
                    elif auth.signup(name, new_email, new_password, new_role):
                        st.success("Account created. Please sign in.")
                    else:
                        st.error("An account with that email already exists.")

        with st.expander("Demo Credentials", expanded=True):
            for role_name, demo_email, demo_pw in auth.DEMO_CREDENTIALS:
                cols = st.columns([1, 2, 1])
                cols[0].write(f"**{role_name}**")
                cols[1].code(f"{demo_email} / {demo_pw}")
                if cols[2].button("Use", key=f"use_{demo_email}"):
                    st.session_state.prefill_email = demo_email
                    st.session_state.prefill_password = demo_pw
                    st.rerun()
            st.caption("Click 'Use' to auto-fill credentials, then press Sign In.")


def render_app():
    style.sidebar_brand()
    style.sidebar_user(st.session_state.user["name"], st.session_state.role)

    nav_options = ["📊 Dashboard", "📍 Land Records", "🌍 GIS Explorer", "🧪 Policy Lab", "📄 Reports", "⚙️ Settings"]
    if st.session_state.page not in nav_options:
        st.session_state.page = "📊 Dashboard"

    choice = st.sidebar.radio(
        "Navigate", nav_options, index=nav_options.index(st.session_state.page), label_visibility="collapsed"
    )
    st.session_state.page = choice

    st.sidebar.markdown("<div style='height:26vh;'></div>", unsafe_allow_html=True)
    style.sidebar_footer()
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        auth.logout()
        st.rerun()
    style.sidebar_prototype_tag()

    if st.session_state.role == "Guest" and choice == "🧪 Policy Lab":
        style.topbar()
        st.warning("Policy Lab requires a Researcher, Policymaker, or Administrator account. Please sign in.")
        return

    style.topbar()

    if choice == "📊 Dashboard":
        dashboard.render()
    elif choice == "📍 Land Records":
        land_records.render()
    elif choice == "🌍 GIS Explorer":
        gis_explorer.render()
    elif choice == "🧪 Policy Lab":
        policy_lab.render()
    elif choice == "📄 Reports":
        reports.render()
    elif choice == "⚙️ Settings":
        settings.render()


if st.session_state.logged_in:
    render_app()
else:
    render_login()
