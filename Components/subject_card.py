import streamlit as st

def subject_card(name, code, section, stats, footer_callback=None):
    with st.container(border=True):
        st.markdown(f"### {name}")
        st.markdown(f"**Code:** {code} | **Section:** {section}")
        
        if stats:
            cols = st.columns(len(stats))
            for i, (icon, label, value) in enumerate(stats):
                with cols[i]:
                    st.markdown(f"**{icon} {value}** {label}")
                    
        if footer_callback:
            st.divider()
            footer_callback()
