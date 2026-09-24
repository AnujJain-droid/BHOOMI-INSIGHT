Prototype for SIH 2026 · SIH26019 · Land Governance Platform

This is a restyled clone of the bhoominiti-ai reference repo, rebuilt to match the BHUMI-INSIGHT navy/green design reference, with the same stack (Streamlit + SQLite + Folium + Plotly). Built as a clickable prototype for demo/judging purposes — not a production system.

Features included in this build
🔐 Mandatory authentication (Sign In / Create Account / Continue as Guest) — sidebar is fully hidden on this screen
📊 Dashboard — stat cards, land-use chart, state risk chart, quick actions
🗺️ Land Records — map + filterable data table
🌍 GIS Explorer — state/district filters, toggleable map layers (Land Use, Soil Health, Water Availability, Vegetation Cover, Climate Vulnerability) with a live legend
🧪 Policy Lab — adjustable weight sliders + simulated risk scoring
📄 Reports — per-state downloadable brief + national risk overview
⚙️ Settings — edit display name, appearance, notification/language preferences, and Logout
🚪 Logout (in sidebar and in Settings) — returns to the login screen
Quick Start
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
The app opens at http://localhost:8501. A SQLite database (bhoominiti.db) is created and seeded automatically on first run.

Demo Credentials
Role	Email	Password
Researcher	researcher@bhumi.in	demo123
Policymaker	policymaker@bhumi.in	demo123
Administrator	admin@bhumi.in	demo123
You can also click Use next to any row on the login screen to auto-fill the fields, or sign up your own account, or continue as Guest (Guest cannot access Policy Lab).

Project Structure
bhumi-insight/
├── app.py\n               # Entry point — login screen, sidebar nav, routing
├── auth.py\n              # Login / signup / session / role gating
├── db.py                # SQLite schema, seeding, queries
├── style.py             # Navy/green CSS theme injection
├── requirements.txt
├── data/
│   └── land_data.csv    # Synthetic per-state land data (15 states)
├── pages_bh/
│   ├── dashboard.py
│   ├── land_records.py
│   ├── gis_explorer.py
│   ├── policy_lab.py
│   ├── reports.py
│   └── settings.py
└── bhoominiti.db         # Created automatically on first run
Data Notice
All data (land_data.csv) is synthetic demo data created for this prototype. It is not sourced from any official government dataset and should not be presented or cited as real statistics.

Notes for judges / demo
The Policy Lab simulation uses a simple illustrative weighting formula, not a validated policy model — it exists to demonstrate the UX of scenario simulation.
This prototype auth system is fine for a demo but would need HTTPS, rate-limiting, and a production session store before real deployment.
