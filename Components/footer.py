import base64
import streamlit as st


def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def footer():
    st.divider()
    footer_img = get_base64("Assets/Seminar-pana.svg")

    st.markdown(f"""
        <div style="display:flex;justify-content:center;padding:20px 0;">
            <img src="data:image/svg+xml;base64,{footer_img}" style="width:200px;opacity:0.7;">
        </div>
        """, unsafe_allow_html=True)