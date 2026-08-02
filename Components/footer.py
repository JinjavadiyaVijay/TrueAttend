import base64
import streamlit as st

def footer():
    st.divider()
    st.space()
    footer_img = get_base64("Assets/Seminar-pana.svg")
    
    st.markdown(f"""
                <div class="footer">
                    <img src="data:image/svg;base64,{footer_img}">
                </div>
                """,unsafe_allow_html=True
                )    