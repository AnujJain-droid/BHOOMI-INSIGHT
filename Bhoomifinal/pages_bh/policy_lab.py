import streamlit as st
import plotly.express as px
import pandas as pd
import db


def render():
    st.markdown("## 🧪 Policy Lab")
    st.caption("Adjustable-weight scenario simulation for testing land-policy trade-offs.")

    records = db.get_land_records()
    state = st.selectbox("Select state to simulate", sorted(records["state"].unique().tolist()))
    row = records[records["state"] == state].iloc[0]

    st.markdown("#### Adjust policy weights")
    c1, c2 = st.columns(2)
    with c1:
        irrigation = st.slider("Irrigation investment priority", 0, 100, 50)
        forest = st.slider("Forest cover protection priority", 0, 100, 50)
    with c2:
        urbanization = st.slider("Urbanization control priority", 0, 100, 50)
        dispute = st.slider("Dispute resolution priority", 0, 100, 50)

    if st.button("▶ Run Simulation", type="primary"):
        base_risk = row["risk_score"]
        # simple weighted adjustment — illustrative only, not a real policy model
        adjustment = (
            (irrigation - 50) * -0.08
            + (forest - 50) * -0.06
            + (urbanization - 50) * 0.05
            + (dispute - 50) * -0.07
        )
        simulated_score = max(0, min(100, base_risk + adjustment))

        db.save_policy_simulation(
            st.session_state.user["email"], state, irrigation, forest, urbanization, dispute, simulated_score
        )

        st.success(f"Simulation complete for {state}.")
        m1, m2, m3 = st.columns(3)
        m1.metric("Current Risk Score", f"{base_risk:.0f}")
        m2.metric("Simulated Risk Score", f"{simulated_score:.0f}", delta=f"{simulated_score - base_risk:+.1f}")
        m3.metric("Land Disputes (current)", f"{int(row['land_disputes'])}")

        chart_df = pd.DataFrame({
            "Scenario": ["Current", "Simulated"],
            "Risk Score": [base_risk, simulated_score],
        })
        fig = px.bar(chart_df, x="Scenario", y="Risk Score", color="Scenario",
                     color_discrete_sequence=["#0b3d6b", "#f57c20"])
        fig.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Recent Simulations")
    conn = db.get_connection()
    df = pd.read_sql_query(
        "SELECT state, irrigation_weight, forest_weight, urbanization_weight, "
        "dispute_resolution_weight, resulting_score, created_at "
        "FROM policy_simulations ORDER BY created_at DESC LIMIT 10",
        conn,
    )
    conn.close()
    if df.empty:
        st.caption("No simulations run yet this session.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)
