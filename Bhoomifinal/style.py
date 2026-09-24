"""
style.py — CSS theme for BHUMI-INSIGHT.
Blue + saffron theme inspired by the API Setu (apisetu.gov.in) government
portal reference: deep blue primary, saffron/orange accent, clean white
cards, logo + wordmark inline in a single row, block-style nav items.
"""

import streamlit as st

# ---- Palette (API Setu-inspired: govt blue + saffron accent) ----
PRIMARY = "#0b3d6b"        # deep blue (header/sidebar base)
PRIMARY_MID = "#0f4c81"    # slightly lighter blue for gradient
PRIMARY_DARK = "#062744"   # darkest blue
ACCENT = "#f57c20"         # saffron/orange accent
ACCENT_DARK = "#d9660f"    # darker saffron on hover
TEXT_LIGHT = "#eaf1fb"
MUTED_LIGHT = "#a9c2de"
BG = "#f4f6fa"
CARD_BG = "#ffffff"

# Backwards-compatible aliases (older page modules reference these names)
NAVY = PRIMARY
GREEN = ACCENT
GREEN_DARK = ACCENT_DARK


def inject_css(hide_sidebar: bool = False):
    sidebar_display = "display: none;" if hide_sidebar else ""
    st.markdown(
        f"""
        <style>
        html, body, [class*="css"] {{
            font-size: 16px;
        }}

        .stApp {{
            background-color: {BG};
            background-image: url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20width%3D%2260%22%20height%3D%2260%22%3E%0A%3Crect%20width%3D%2260%22%20height%3D%2260%22%20fill%3D%22none%22/%3E%0A%3Cpath%20d%3D%22M0%200H60V60%22%20fill%3D%22none%22%20stroke%3D%22%230b3d6b%22%20stroke-opacity%3D%220.06%22%20stroke-width%3D%221%22/%3E%0A%3Ccircle%20cx%3D%220%22%20cy%3D%220%22%20r%3D%221.4%22%20fill%3D%22%23f57c20%22%20fill-opacity%3D%220.10%22/%3E%0A%3C/svg%3E");
            background-size: 60px 60px;
            background-repeat: repeat;
            background-attachment: fixed;
        }}

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"] {{
            {sidebar_display}
            background: linear-gradient(180deg, {PRIMARY_DARK} 0%, {PRIMARY} 100%);
            min-width: 270px !important;
            width: 270px !important;
        }}
        section[data-testid="stSidebar"] * {{
            color: {TEXT_LIGHT} !important;
        }}
        section[data-testid="stSidebar"] > div {{
            padding-top: 0;
        }}
        div[data-testid="collapsedControl"] {{
            {sidebar_display}
        }}

        /* Nav items styled as full-width blocks/bars */
        section[data-testid="stSidebar"] div[role="radiogroup"] {{
            gap: 6px;
            padding: 4px 14px;
        }}
        section[data-testid="stSidebar"] div[role="radiogroup"] > label {{
            padding: 12px 16px;
            border-radius: 12px;
            font-size: 1.02rem;
            font-weight: 600;
            background: rgba(255,255,255,0.045);
            border: 1px solid rgba(255,255,255,0.06);
            width: 100%;
            display: flex;
            align-items: center;
            transition: background 0.15s ease, border-color 0.15s ease;
        }}
        /* Hide the native radio circle/mark — icon + label text only */
        section[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {{
            display: none !important;
        }}
        section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {{
            background: rgba(255,255,255,0.1);
            border-color: rgba(255,255,255,0.16);
        }}
        section[data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"],
        section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {{
            background: {ACCENT};
            border-color: {ACCENT};
            box-shadow: 0 2px 8px rgba(245,124,32,0.35);
        }}
        section[data-testid="stSidebar"] div[role="radiogroup"] input {{
            display: none;
        }}

        /* Brand block — logo + wordmark inline, single row */
        .sidebar-brand {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 20px 18px 16px 18px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 16px;
            white-space: nowrap;
        }}
        .sidebar-brand-icon {{
            background: {ACCENT};
            border-radius: 9px;
            width: 38px;
            height: 38px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 19px;
            flex-shrink: 0;
        }}
        .sidebar-brand-text {{
            font-weight: 800;
            font-size: 1.15rem;
            color: #ffffff !important;
            letter-spacing: 0.3px;
            line-height: 1;
        }}

        .sidebar-user {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 18px 20px 18px;
            margin-bottom: 6px;
        }}
        .sidebar-user-avatar {{
            background: {ACCENT};
            color: #1a0d00 !important;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 1.05rem;
            flex-shrink: 0;
        }}
        .sidebar-user-name {{
            font-weight: 700;
            font-size: 0.98rem;
            color: #ffffff !important;
            line-height: 1.15;
        }}
        .sidebar-user-role {{
            font-size: 0.78rem;
            color: {ACCENT} !important;
            font-weight: 700;
        }}

        .sidebar-divider {{
            border-top: 1px solid rgba(255,255,255,0.1);
            margin: 14px 18px 12px 18px;
        }}
        .sidebar-footer-tag {{
            text-align: center;
            font-size: 0.68rem;
            color: {MUTED_LIGHT} !important;
            padding: 6px 0 4px 0;
            letter-spacing: 0.4px;
        }}

        /* ---------- Login page ---------- */
        .login-topbar {{
            background: {PRIMARY};
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 28px;
            margin: -1rem -1rem 2rem -1rem;
            border-bottom: 3px solid {ACCENT};
        }}
        .login-topbar-brand {{
            display: flex;
            align-items: center;
            gap: 10px;
            white-space: nowrap;
        }}
        .login-topbar-icon {{
            background: {ACCENT};
            width: 34px;
            height: 34px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 17px;
            flex-shrink: 0;
        }}
        .login-topbar-text {{
            font-weight: 800;
            font-size: 1.1rem;
            color: #ffffff;
            letter-spacing: 0.3px;
        }}
        .login-topbar-back {{
            color: {MUTED_LIGHT};
            font-size: 0.85rem;
            font-weight: 600;
        }}
        .login-title {{
            text-align: center;
            font-size: 1.8rem;
            font-weight: 800;
            color: {PRIMARY};
            margin-bottom: 2px;
        }}
        .login-subtitle {{
            text-align: center;
            color: #64748b;
            font-size: 1rem;
            margin-bottom: 1.2rem;
        }}

        /* ---------- Top header bar (post-login pages) ---------- */
        .bh-topbar {{
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: 18px;
            background: {CARD_BG};
            border-radius: 12px;
            padding: 10px 18px;
            margin-bottom: 1.1rem;
            border: 1px solid #e9eef4;
            box-shadow: 0 1px 4px rgba(11,61,107,0.05);
        }}
        .bh-topbar-icon {{
            font-size: 1.15rem;
            color: {PRIMARY};
            position: relative;
        }}
        .bh-topbar-dot {{
            position: absolute;
            top: -2px;
            right: -3px;
            width: 7px;
            height: 7px;
            background: {ACCENT};
            border-radius: 50%;
        }}
        .bh-topbar-user {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .bh-topbar-avatar {{
            background: {PRIMARY};
            color: #fff;
            width: 34px;
            height: 34px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 0.95rem;
        }}
        .bh-topbar-name {{
            font-weight: 700;
            font-size: 0.92rem;
            color: {PRIMARY};
            line-height: 1.15;
        }}
        .bh-topbar-role {{
            font-size: 0.72rem;
            color: #64748b;
        }}

        /* ---------- Buttons ---------- */
        div.stButton > button {{
            background-color: {CARD_BG};
            color: {PRIMARY};
            border: 1px solid #dfe6ee;
            border-radius: 10px;
            font-weight: 600;
            font-size: 1rem;
            padding: 0.55rem 1.1rem;
            text-align: left;
            transition: transform 0.05s ease, box-shadow 0.15s ease, border-color 0.15s ease;
        }}
        div.stButton > button:hover {{
            border-color: {PRIMARY};
            box-shadow: 0 2px 8px rgba(11,61,107,0.12);
            color: {PRIMARY};
            transform: translateY(-1px);
        }}
        div.stButton > button[kind="primary"] {{
            background-color: {PRIMARY};
            color: #ffffff;
            border: none;
            text-align: center;
        }}
        div.stButton > button[kind="primary"]:hover {{
            background-color: {PRIMARY_MID};
            color: #ffffff;
        }}
        section[data-testid="stSidebar"] div.stButton > button {{
            background-color: transparent;
            border: 1px solid rgba(255,255,255,0.25);
            color: {TEXT_LIGHT} !important;
            width: 100%;
            font-weight: 600;
            text-align: center;
        }}
        section[data-testid="stSidebar"] div.stButton > button:hover {{
            background-color: rgba(255,255,255,0.1);
            transform: none;
            box-shadow: none;
        }}

        /* ---------- Cards ---------- */
        .bh-card {{
            background: {CARD_BG};
            border-radius: 14px;
            padding: 1.3rem 1.5rem;
            box-shadow: 0 2px 10px rgba(11,61,107,0.07);
            border: 1px solid #e9eef4;
            margin-bottom: 1.1rem;
        }}
        .bh-stat-top {{
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
        }}
        .bh-stat-label {{
            color: #64748b;
            font-size: 0.9rem;
            font-weight: 600;
        }}
        .bh-stat-value {{
            font-size: 2.2rem;
            font-weight: 800;
            color: {PRIMARY};
            margin-top: 4px;
        }}
        .bh-stat-sub {{
            color: {ACCENT_DARK};
            font-size: 0.82rem;
            margin-top: 6px;
            font-weight: 700;
        }}
        .bh-chip {{
            width: 40px;
            height: 40px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.15rem;
            flex-shrink: 0;
        }}
        .chip-blue {{ background: #e5edf9; }}
        .chip-orange {{ background: #fdecdc; }}
        .chip-teal {{ background: #e2f4ee; }}
        .chip-indigo {{ background: #eaeafb; }}

        /* ---------- Workflow flowchart (plain divs, no SVG) ---------- */
        .bh-flow-row {{
            display: flex;
            align-items: center;
            gap: 6px;
            overflow-x: auto;
            padding: 4px 0;
        }}
        .bh-flow-node {{
            flex: 1 0 170px;
            min-width: 150px;
            background: #ffffff;
            border: 1.5px solid {PRIMARY};
            border-radius: 12px;
            padding: 14px 10px 12px 10px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        .bh-flow-topbar {{
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 5px;
            background: {ACCENT};
        }}
        .bh-flow-icon {{
            font-size: 1.4rem;
            margin-top: 4px;
        }}
        .bh-flow-title {{
            font-weight: 700;
            font-size: 0.92rem;
            color: {PRIMARY};
            margin-top: 4px;
        }}
        .bh-flow-sub {{
            font-size: 0.72rem;
            color: #64748b;
            margin-top: 2px;
        }}
        .bh-flow-arrow {{
            font-size: 1.3rem;
            color: {ACCENT};
            font-weight: 800;
            flex: 0 0 auto;
            padding: 0 2px;
        }}

        .bh-badge {{
            display: inline-block;
            background: rgba(245,124,32,0.14);
            color: {ACCENT_DARK};
            border-radius: 20px;
            padding: 5px 14px;
            font-size: 0.8rem;
            font-weight: 700;
        }}

        /* ---------- Headings & tabs ---------- */
        h1 {{ color: {PRIMARY}; font-weight: 800; }}
        h2 {{ color: {PRIMARY}; font-weight: 800; font-size: 1.65rem; }}
        h3, h4 {{ color: {PRIMARY}; font-weight: 700; }}
        p, label, .stMarkdown {{ font-size: 1rem; }}

        .stTabs [data-baseweb="tab"] {{
            font-size: 1.02rem;
            font-weight: 600;
        }}
        .stTabs [aria-selected="true"] {{
            color: {ACCENT_DARK} !important;
        }}

        div[data-testid="stMetricValue"] {{
            font-size: 1.85rem;
            color: {PRIMARY};
        }}

        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header[data-testid="stHeader"] {{background: transparent;}}
        </style>
        """,
        unsafe_allow_html=True,
    )


def login_header():
    st.markdown(
        f"""
        <div class="login-topbar">
            <div class="login-topbar-brand">
                <div class="login-topbar-icon">🌏</div>
                <div class="login-topbar-text">BHUMI-INSIGHT</div>
            </div>
            <div class="login-topbar-back">← Back to Home</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar_brand():
    st.sidebar.markdown(
        f"""
        <div class="sidebar-brand">
            <div class="sidebar-brand-icon">🌏</div>
            <div class="sidebar-brand-text">BHUMI-INSIGHT</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar_user(name: str, role: str):
    initial = name.strip()[0].upper() if name else "U"
    st.sidebar.markdown(
        f"""
        <div class="sidebar-user">
            <div class="sidebar-user-avatar">{initial}</div>
            <div>
                <div class="sidebar-user-name">{name}</div>
                <div class="sidebar-user-role">{role}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar_footer():
    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)


def sidebar_prototype_tag():
    st.sidebar.markdown(
        '<div class="sidebar-footer-tag">SIH 2026 · SIH26019 Prototype</div>',
        unsafe_allow_html=True,
    )


def topbar():
    """Slim header bar shown at the top of every post-login page —
    theme toggle + notification icons (decorative) and the user's avatar."""
    user = st.session_state.get("user") or {"name": "Guest", "email": ""}
    role = st.session_state.get("role", "Guest")
    initial = user["name"].strip()[0].upper() if user["name"] else "U"
    st.markdown(
        f"""
        <div class="bh-topbar">
            <div class="bh-topbar-icon">🌙</div>
            <div class="bh-topbar-icon">🔔<span class="bh-topbar-dot"></span></div>
            <div class="bh-topbar-user">
                <div class="bh-topbar-avatar">{initial}</div>
                <div>
                    <div class="bh-topbar-name">{user['name']}</div>
                    <div class="bh-topbar-role">{role}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def stat_card(label: str, value: str, sub: str = "", icon: str = "", chip: str = "chip-blue"):
    icon_html = f'<div class="bh-chip {chip}">{icon}</div>' if icon else ""
    st.markdown(
        f"""
        <div class="bh-card">
            <div class="bh-stat-top">
                <div class="bh-stat-label">{label}</div>
                {icon_html}
            </div>
            <div class="bh-stat-value">{value}</div>
            <div class="bh-stat-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
