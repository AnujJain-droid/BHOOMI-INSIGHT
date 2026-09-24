import streamlit as st
import plotly.express as px
import pandas as pd
import db
import style


def render():
    user = st.session_state.user

    head_col, badge_col = st.columns([4, 1])
    with head_col:
        st.markdown(f"## Welcome back, {user['name'].split()[0]}")
        st.caption("Here's an overview of land-governance data on the platform.")
    with badge_col:
        st.markdown(
            "<div style='text-align:right;padding-top:10px;'><span class='bh-badge'>Demo Data</span></div>",
            unsafe_allow_html=True,
        )

    records = db.get_land_records()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        style.stat_card("Land Datasets", f"{len(records)}", "↗ Demo Data", icon="🗄️", chip="chip-blue")
    with col2:
        style.stat_card("Avg. Risk Score", f"{records['risk_score'].mean():.0f}", "↗ Demo Data", icon="⚠️", chip="chip-orange")
    with col3:
        style.stat_card("Active Policy Studies", f"{db_policy_count()}", "↗ Session Data", icon="🧪", chip="chip-teal")
    with col4:
        style.stat_card("States Covered", f"{records['state'].nunique()}", "↗ Demo Data", icon="📍", chip="chip-indigo")

    st.markdown("#### Quick Actions")
    qa1, qa2, qa3, qa4 = st.columns(4)
    with qa1:
        if st.button("📍  Land Records", use_container_width=True):
            st.session_state.page = "📍 Land Records"
            st.rerun()
    with qa2:
        if st.button("🌍  GIS Explorer", use_container_width=True):
            st.session_state.page = "🌍 GIS Explorer"
            st.rerun()
    with qa3:
        if st.button("🧪  Policy Lab", use_container_width=True):
            st.session_state.page = "🧪 Policy Lab"
            st.rerun()
    with qa4:
        if st.button("📄  Generate Report", use_container_width=True):
            st.session_state.page = "📄 Reports"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    _render_workflow_diagram()
    st.markdown("<br>", unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.markdown("##### Land-Use Categories (National Avg.)")
        avg = records[["agricultural_pct", "forest_pct", "urban_pct", "wasteland_pct", "water_pct"]].mean()
        df = pd.DataFrame({
            "Category": ["Agricultural", "Forest", "Urban", "Wasteland", "Water Bodies"],
            "Percent": avg.values,
        })
        fig = px.bar(df, x="Category", y="Percent", color_discrete_sequence=[style.NAVY])
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=320, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with chart_col2:
        st.markdown("##### Risk Score by State")
        top = records.sort_values("risk_score", ascending=False).head(8)
        fig2 = px.bar(top, x="state", y="risk_score", color_discrete_sequence=[style.GREEN])
        fig2.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=320, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)


def db_policy_count():
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM policy_simulations")
    count = cur.fetchone()[0]
    conn.close()
    return count


def _render_workflow_diagram():
    """Simple flowchart of the platform's data pipeline, styled with the app theme.
    Built with plain divs (not inline SVG) since Streamlit's markdown sanitizer
    does not reliably parse raw <svg> child elements."""
    st.markdown("#### How BHUMI-INSIGHT Works")
    nodes = [
        ("🗺️", "Land Data", "State-wise land & GIS records"),
        ("🌍", "GIS Analysis", "Map layers & risk scoring"),
        ("🧪", "Policy Lab", "Scenario simulation"),
        ("📄", "Reports", "Downloadable briefs"),
    ]
    parts = ['<div class="bh-card"><div class="bh-flow-row">']
    for i, (icon, title, sub) in enumerate(nodes):
        parts.append(
            f'<div class="bh-flow-node"><div class="bh-flow-topbar"></div>'
            f'<div class="bh-flow-icon">{icon}</div>'
            f'<div class="bh-flow-title">{title}</div>'
            f'<div class="bh-flow-sub">{sub}</div></div>'
        )
        if i < len(nodes) - 1:
            parts.append('<div class="bh-flow-arrow">&#8594;</div>')
    parts.append("</div></div>")
    html = "".join(parts)
    st.markdown(html, unsafe_allow_html=True)
