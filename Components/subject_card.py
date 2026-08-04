import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None, actions=None):
    """
    Reusable subject card component.
    
    Args:
        name: Subject name
        code: Subject code
        section: Section identifier
        stats: List of (icon, label, value) tuples
        footer_callback: Callable to render footer buttons
        actions: List of (label, key, callback) tuples for action buttons
    """
    html = f"""
        <div style="
            background: white;
            border-left: 6px solid #4B5694;
            padding: 20px 24px;
            border-radius: 16px;
            border: 1px solid rgba(0,0,0,0.1);
            margin-bottom: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        ">
            <h3 style="margin:0 0 8px 0; color:#1e293b; font-size:1.3rem; font-family:'Sora',sans-serif;">
                📘 {name}
            </h3>
            <p style="color:#64748b; margin:4px 0 12px 0; font-size:0.95rem;">
                Code: <span style="
                    background:#E0E3FF;
                    color:#4B5694;
                    padding:2px 10px;
                    border-radius:6px;
                    font-weight:600;
                    font-size:0.85rem;
                ">{code}</span>
                &nbsp;|&nbsp; Section: <strong>{section}</strong>
            </p>
    """

    if stats:
        html += '<div style="display:flex; gap:24px; margin-top:8px;">'
        for icon, label, value in stats:
            html += f"""
                <div style="text-align:center;">
                    <span style="font-size:1.4rem;">{icon}</span>
                    <div style="font-size:1.2rem; font-weight:700; color:#063B00;">{value}</div>
                    <div style="font-size:0.8rem; color:#64748b; text-transform:uppercase;">{label}</div>
                </div>
            """
        html += '</div>'

    html += '</div>'

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()

    if actions:
        cols = st.columns(len(actions))
        for i, (label, key, callback) in enumerate(actions):
            with cols[i]:
                if st.button(label, key=key):
                    callback()
