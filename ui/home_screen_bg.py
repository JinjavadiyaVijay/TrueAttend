import streamlit as st

def home_screen_bg():
    st.markdown(
        """
        <style>
                .stApp {
                    background: #063B00 !important;
                }
                div[data-testid="stColumn"] > div{
                    background: rgba(255,255,255,0.15);
                    backdrop-filter: blur(12px);
                    border: 1px solid rgba(255,255,255,0.2);
                    border-radius: 30px;
                    padding: 30px;
                }
        </style>
        """,
        unsafe_allow_html=True,
    )

def dashboard_screen_bg():
    st.markdown(
        """
        <style>
                .stApp {
                    background: #F0FFC3 !important;
                }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ─── Design System ────────────────────────────────────────────────
COMMON_STYLE = """
    @import url('https://fonts.googleapis.com/css2?family=Sonsie+One&family=Sora:wght@100..800&display=swap');

    /* ── Primary button ── */
    button[data-testid="stBaseButton-primary"] {
        background-color: #BA5A5A !important;
        color: #FFF8EC !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.55rem 1.4rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 6px rgba(186,90,90,0.2) !important;
    }
    button[data-testid="stBaseButton-primary"]:hover {
        background-color: #a34d4d !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(186,90,90,0.3) !important;
    }
    button[data-testid="stBaseButton-primary"]:active {
        transform: translateY(0) !important;
    }

    /* ── Secondary button ── */
    button[data-testid="stBaseButton-secondary"] {
        background-color: #4B5694 !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.55rem 1.4rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 6px rgba(75,86,148,0.2) !important;
    }
    button[data-testid="stBaseButton-secondary"]:hover {
        background-color: #3d4778 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(75,86,148,0.3) !important;
    }

    /* ── Tertiary button ── */
    button[kind="tertiary"] {
        background-color: transparent !important;
        color: #1f2937 !important;
        border: 2px solid #94a3b8 !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 0.55rem 1.4rem !important;
        transition: all 0.2s ease;
    }
    button[kind="tertiary"]:hover {
        background-color: #e2e8f0 !important;
        color: black !important;
        border-color: #64748b !important;
    }
    button[kind="tertiary"]:active {
        background-color: #cbd5e1 !important;
    }
    button[kind="tertiary"] svg { color: inherit !important; }
    button[kind="tertiary"] p { color: inherit !important; font-weight: 600 !important; }

    /* ── General hover ── */
    div.stButton > button:hover {
        transform: translateY(-2px);
    }

    /* ── Centered container ── */
    .block-container {
        max-width: 1200px !important;
        margin: 0 auto !important;
        padding-top: 0.2rem;
        padding-bottom: 0rem;
    }

    /* ── Text input ── */
    div[data-testid="stTextInput"] {
        margin-bottom: 0.75rem;
    }
    div[data-testid="stTextInput"] input {
        background: #FFFFFF !important;
        color: #063B00 !important;
        border: 2px solid #063B00 !important;
        border-radius: 12px !important;
        padding: 0.7rem 1rem !important;
        font-size: 1rem !important;
        caret-color: #063B00 !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
    }
    div[data-testid="stTextInput"] input::placeholder {
        color: #7B7B7B !important;
        opacity: 1 !important;
    }
    div[data-testid="stTextInput"] label {
        color: #063B00 !important;
        font-weight: 600 !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border: 2px solid #4B5694 !important;
        box-shadow: 0 0 0 3px rgba(75,86,148,.15) !important;
    }

    /* ── Divider ── */
    div[data-testid="stDivider"] hr {
        border-top: 2px solid #063B00 !important;
        opacity: 1 !important;
    }

    /* ── Spinner ── */
    .stSpinner > div p {
        color: #063B00 !important;
        font-size: 18px;
        font-weight: 600;
    }
    .stSpinner svg {
        stroke: #ff9800 !important;
    }

    /* ── Metric cards ── */
    div[data-testid="stMetric"] {
        background: white;
        border-radius: 14px;
        padding: 18px 22px;
        border: 1px solid rgba(0,0,0,0.06);
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: box-shadow 0.2s, transform 0.2s;
    }
    div[data-testid="stMetric"]:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        transform: translateY(-1px);
    }
    div[data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }
    div[data-testid="stMetricValue"] {
        color: #063B00 !important;
        font-weight: 700 !important;
        font-size: 1.6rem !important;
    }

    /* ── Data table ── */
    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(0,0,0,0.08);
    }

    /* ── Select box ── */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        background: white !important;
        border: 2px solid #063B00 !important;
        border-radius: 12px !important;
    }
    div[data-testid="stSelectbox"] label {
        color: #063B00 !important;
        font-weight: 600 !important;
    }

    /* ── Download button ── */
    div[data-testid="stDownloadButton"] button {
        background-color: #063B00 !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
    }

    /* ── File uploader ── */
    div[data-testid="stFileUploader"] {
        border: 2px dashed #4B5694 !important;
        border-radius: 12px !important;
        padding: 10px !important;
    }

    /* ── Radio buttons ── */
    div[data-testid="stRadio"] label {
        color: #063B00 !important;
        font-weight: 600 !important;
    }

    /* ── Alert boxes ── */
    div[data-testid="stAlert"] {
        border-radius: 12px !important;
    }
"""


def style_home_layout():
    st.markdown(
        f"""
            <style>
            {COMMON_STYLE}

            h1, h2{{
                font-family:'Sonsie One',sans-serif !important;
                font-size:3.9rem !important;
                color:#FFF8EC !important;
                line-height:1.1 !important;
                margin-bottom:0 !important;
            }}

            .header h3,
            .header h4 {{
                font-family:'Sora',sans-serif !important;
                color:#FFF8EC !important;
            }}
            </style>
        """,
        unsafe_allow_html=True,
    )


def style_dashboard_layout():
    st.markdown(
        f"""
            <style>
            {COMMON_STYLE}

            /* ── Dashboard header ── */
            .header {{
                display: flex !important;
                justify-content: flex-start !important;
                flex-direction: row !important;
                align-items: center !important;
                gap: 10px !important;
                width: 80% !important;
            }}

            .header img {{
                width: 90px !important;
                border-radius: 20px !important;
            }}

            .header h1,
            .header h2 {{
                font-family:'Sonsie One',sans-serif !important;
                font-size:2rem !important;
                color:#063B00 !important;
                margin-bottom: -5px !important;
            }}

            /* ── Sub header ── */
            .sub-header{{
                width:100%;
                display:flex;
                justify-content:center;
                align-items:center;
                margin-top:10px;
            }}

            .sub-header h3{{
                margin:0;
                font-family:'Sora',sans-serif;
                font-size:2.6rem;
                font-weight:700;
                color:#063B00;
            }}

            </style>
        """,
        unsafe_allow_html=True,
    )
