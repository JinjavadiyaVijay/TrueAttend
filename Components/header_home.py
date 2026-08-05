import base64
import streamlit as st


def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def header_home():
    logo = get_base64("Assets/TrueAttend.png")

    st.markdown(
        f"""
        <style>
        .header {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            width: 100%;
        }}

        .header img {{
            width: 140px;
            border-radius: 25px;
        }}

        .header h1 {{
            margin-bottom: 0;
            color: white;
            text-align: center;
        }}
        </style>

        <div class="header">
            <img src="data:image/png;base64,{logo}">
            <h1>TrueAttend</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )


def header_dashboard():
    logo = get_base64("Assets/TrueAttend.png")

    st.markdown(
        f"""
        <div class="header">
            <img src="data:image/png;base64,{logo}">
            <h2>TrueAttend</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

def sub_header_dashboard(text):
    st.markdown(
        f"""
        <div class="sub-header">
            <h3>{text}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

def custom_text_input(label, placeholder="", key=None):
    st.markdown(
        f"<p style='color:#063B00;font-size:20px;font-weight:600'>{label}</p>",
        unsafe_allow_html=True,
    )

    return st.text_input(
        "",
        placeholder=placeholder,
        key=key,
        label_visibility="collapsed",
    )
