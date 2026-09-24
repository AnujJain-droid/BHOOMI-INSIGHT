import streamlit as st
import folium
from streamlit_folium import st_folium
import db

LAYERS = ["Land Use", "Soil Health", "Water Availability", "Vegetation Cover", "Climate Vulnerability"]

LAYER_LEGEND = {
    "Land Use": {"Agricultural": "#22c55e", "Forest": "#166534", "Urban": "#92400e", "Wasteland": "#a16207", "Water": "#0ea5e9"},
    "Soil Health": {"Good": "#22c55e", "Moderate": "#eab308", "Poor": "#dc2626"},
    "Water Availability": {"High": "#0284c7", "Medium": "#38bdf8", "Low": "#f87171"},
    "Vegetation Cover": {"Dense": "#14532d", "Moderate": "#4ade80", "Sparse": "#d9f99d"},
    "Climate Vulnerability": {"Low": "#22c55e", "Medium": "#f59e0b", "High": "#dc2626"},
}


def _marker_color(row, layer):
    if layer == "Land Use":
        return "#22c55e" if row["agricultural_pct"] >= row["forest_pct"] else "#166534"
    if layer == "Climate Vulnerability":
        return "#dc2626" if row["risk_score"] >= 65 else ("#f59e0b" if row["risk_score"] >= 45 else "#22c55e")
    if layer == "Water Availability":
        return "#0284c7" if row["water_pct"] >= 7 else "#f87171"
    return "#22c55e"


def render():
    st.markdown("## GIS Explorer")
    st.caption("Interactive map with land-use, soil, water, and climate layers.")

    records = db.get_land_records()

    f1, f2, f3 = st.columns([2, 2, 1])
    with f1:
        state = st.selectbox("State", ["Select State"] + sorted(records["state"].unique().tolist()))
    with f2:
        district = st.selectbox("District", ["Select District"], disabled=(state == "Select State"))
    with f3:
        st.write("")
        st.write("")
        if st.button("Reset Map", use_container_width=True):
            st.rerun()

    st.markdown("**Map Layers**")
    layer_cols = st.columns(len(LAYERS))
    if "gis_layer" not in st.session_state:
        st.session_state.gis_layer = "Land Use"
    for i, layer in enumerate(LAYERS):
        with layer_cols[i]:
            active = st.session_state.gis_layer == layer
            if st.button(layer, key=f"layer_{layer}", type="primary" if active else "secondary", use_container_width=True):
                st.session_state.gis_layer = layer
                st.rerun()

    active_layer = st.session_state.gis_layer
    map_col, detail_col = st.columns([2, 1])

    with map_col:
        m = folium.Map(location=[22.5, 80.0], zoom_start=4.6, tiles="cartodbpositron")
        for _, row in records.iterrows():
            color = _marker_color(row, active_layer)
            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=9,
                popup=folium.Popup(f"<b>{row['state']}</b><br>Risk score: {row['risk_score']}", max_width=220),
                tooltip=row["state"],
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.85,
                weight=1,
            ).add_to(m)

        legend_items = "".join(
            f'<div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">'
            f'<span style="width:12px;height:12px;background:{c};border-radius:3px;display:inline-block;"></span>'
            f'<span style="font-size:12px;">{label}</span></div>'
            for label, c in LAYER_LEGEND.get(active_layer, {}).items()
        )
        legend_html = f"""
        <div style="position: fixed; bottom: 30px; left: 30px; z-index:9999;
                    background: white; padding: 10px 14px; border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.15); font-family: sans-serif;">
            <div style="font-weight:700;font-size:12px;margin-bottom:6px;">{active_layer} Legend</div>
            {legend_items}
        </div>
        """
        m.get_root().html.add_child(folium.Element(legend_html))

        st_folium(m, width=None, height=480, key="gis_map")

    with detail_col:
        st.markdown("##### District Insights")
        if state == "Select State":
            st.info("Select a state to view detailed insights.")
        else:
            row = records[records["state"] == state].iloc[0]
            st.metric("Risk Score", f"{row['risk_score']:.0f}")
            st.metric("Land Disputes", f"{int(row['land_disputes'])}")
            st.write(f"**Region:** {row['region']}")
            st.write(f"**Total Parcels:** {int(row['total_parcels']):,}")
            st.progress(min(int(row["risk_score"]), 100) / 100, text="Relative risk level")
