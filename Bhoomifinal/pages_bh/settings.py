import streamlit as st
import auth


def render():
    st.markdown("## Settings")
    st.caption("Manage your profile, theme, and preferences.")

    user = st.session_state.user
    role = st.session_state.role

    st.markdown("#### Profile")
    with st.container(border=True):
        col1, col2 = st.columns([1, 4])
        with col1:
            initial = user["name"].strip()[0].upper() if user["name"] else "U"
            st.markdown(
                f"<div style='width:56px;height:56px;border-radius:50%;background:#22c55e;"
                f"color:#06170d;display:flex;align-items:center;justify-content:center;"
                f"font-weight:800;font-size:1.4rem;'>{initial}</div>",
                unsafe_allow_html=True,
            )
        with col2:
            st.write(f"**{user['name']}**")
            st.caption(user["email"])
            st.markdown(f"<span class='bh-badge'>{role}</span>", unsafe_allow_html=True)

        display_name = st.text_input("Display Name", value=user["name"])
        if st.button("Save Changes"):
            st.session_state.user["name"] = display_name
            st.success("Profile updated for this session.")
            if role != "Guest":
                st.caption(
                    "Note: this prototype stores profile edits in-session only; "
                    "it does not write back to the database."
                )

    st.markdown("#### Appearance")
    with st.container(border=True):
        st.radio("Theme", ["Light", "Dark"], horizontal=True, label_visibility="collapsed")
        st.caption("Theme switching is illustrative in this prototype build.")

    st.markdown("#### Preferences")
    with st.container(border=True):
        st.toggle("Notifications — receive updates about new research and projects", value=True)
        st.selectbox("Language", ["English", "Hindi"])
        st.divider()
        st.markdown("**Data Privacy**")
        st.caption(
            "BHUMI-INSIGHT stores all demo data locally in SQLite for this prototype. "
            "No data is sent to any external service."
        )

    st.markdown("#### Account")
    with st.container(border=True):
        st.write(f"Role: **{role}**")
        if st.button("Logout", type="primary"):
            auth.logout()
            st.rerun()
