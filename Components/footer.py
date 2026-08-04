import base64
import streamlit as st


def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def footer():
    st.markdown("""
        <hr style="
            border: none;
            height: 1px;
            background: rgba(0, 0, 0, 0.18);
            margin: 24px 0;
        ">
        """, unsafe_allow_html=True)
    footer_img = get_base64("Assets/Seminar-pana.svg")

    st.markdown(f"""
        <div style="display:flex;justify-content:center;padding:20px 0;">
            <img src="data:image/svg+xml;base64,{footer_img}" style="width:400px;opacity:0.7;">
        </div>
        """, unsafe_allow_html=True)