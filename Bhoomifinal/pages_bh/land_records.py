import streamlit as st
import folium
from streamlit_folium import st_folium
import db

LAYER_COLORS = {
    "Land Use": "green",
    "Soil Health": "orange",
    "Water Availability": "blue",
    "Vegetation Cover": "darkgreen",
    "Climate Vulnerability": "red",
}


def render():
    st.markdown("## 🗺️ Land Records")
    st.caption("Interactive map with land-use, risk, and dispute data by state.")

    records = db.get_land_records()

    filt_col1, filt_col2, filt_col3 = st.columns([2, 2, 1])
    with filt_col1:
        state_filter = st.selectbox("State", ["All States"] + sorted(records["state"].unique().tolist()))
    with filt_col2:
        layer = st.selectbox("Map Layer", list(LAYER_COLORS.keys()))
    with filt_col3:
        st.write("")
        st.write("")
        if st.button("Reset Map"):
            st.rerun()

    filtered = records if state_filter == "All States" else records[records["state"] == state_filter]

    map_col, detail_col = st.columns([2, 1])

    with map_col:
        m = folium.Map(location=[22.5, 80.0], zoom_start=5, tiles="cartodbpositron")
        color = LAYER_COLORS.get(layer, "green")
        for _, row in filtered.iterrows():
            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=8 + row["risk_score"] / 15,
                popup=folium.Popup(
                    f"<b>{row['state']}</b><br>"
                    f"Risk score: {row['risk_score']}<br>"
                    f"Disputes: {row['land_disputes']}<br>"
                    f"Parcels: {row['total_parcels']:,}",
                    max_width=250,
                ),
                tooltip=row["state"],
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7,
            ).add_to(m)
        st_folium(m, width=None, height=480)

    with detail_col:
        st.markdown("##### Details")
        if state_filter == "All States":
            st.info("Select a state above to view detailed land records.")
        else:
            row = filtered.iloc[0]
            st.metric("Risk Score", f"{row['risk_score']:.0f}")
            st.metric("Land Disputes", f"{int(row['land_disputes'])}")
            st.metric("Total Parcels", f"{int(row['total_parcels']):,}")
            st.write(f"**Region:** {row['region']}")
            st.write(f"**Agricultural:** {row['agricultural_pct']}%  |  **Forest:** {row['forest_pct']}%")
            st.write(f"**Urban:** {row['urban_pct']}%  |  **Wasteland:** {row['wasteland_pct']}%")

    st.markdown("#### Land Records Table")
    st.dataframe(
        filtered[[
            "state", "region", "risk_score", "land_disputes", "total_parcels",
            "agricultural_pct", "forest_pct", "urban_pct", "wasteland_pct", "water_pct",
        ]],
        use_container_width=True,
        hide_index=True,
    )
