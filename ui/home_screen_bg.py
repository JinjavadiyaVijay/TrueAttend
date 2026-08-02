import streamlit as st


# home screen
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
                """,
        unsafe_allow_html=True,
    )


# deshboard
def deshboard_screen_bg():
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


def style_home_layout():
    st.markdown(
        """
            <style>
            
            @import url('https://fonts.googleapis.com/css2?family=Sonsie+One&family=Sora:wght@100..800&display=swap');
            
            #MainMenu,
            header,
            footer{
                visibility:hidden;
            }
            
            h1, h2{
                font-family:'Sonsie One',sans-serif !important;
                font-size:3.9rem !important;
                color:#FFF8EC !important;
                line-height:1.1 !important;
                margin-bottom:0 !important;
            }
            
            .header h3,
            .header h4 {
                font-family:'Sora',sans-serif !important;
                color:#FFF8EC !important;
            }
            
            
            /* Primary button */
            button[data-testid="stBaseButton-primary"]{
                background-color:#BA5A5A !important;
                color:#FFF8EC !important;
                border:none !important;
            }

            /* Secondary button */
            button[data-testid="stBaseButton-secondary"]{
                background-color:#4B5694 !important;
                color:white !important;
                border:none !important;
            }
            
            div.stButton > button:hover{
                transform:scale(1.05);
            }
            
            
            /* Remove top padding */
            .block-container{
            padding-top: 0.2rem;
            padding-bottom: 0rem;
            }
                      
            </style>
            """,
        unsafe_allow_html=True,
    )


def style_dashboard_layout():
    st.markdown(
        """
            <style>
            
            @import url('https://fonts.googleapis.com/css2?family=Sonsie+One&family=Sora:wght@100..800&display=swap');
            
            #MainMenu,
            header,
            footer{
                visibility:hidden;
            }

            .header {
                display: flex !important;
                justify-content: flex-start !important;
                flex-direction: row !important;
                align-items: center !important;
                gap: 10px !important;
                width: 80% !important;
            }

            .header img {
                width: 90px !important;
                border-radius: 20px !important;
            }

            .header h1,
            .header h2 {
                font-family:'Sonsie One',sans-serif !important;
                font-size:2rem !important;
                color:#063B00 !important;
                margin-bottom: -5px !important;
            }
            
            .sub-header{
                width:100%;
                display:flex;
                justify-content:center;
                align-items:center;
                margin-top:10px;
            }
            
            .sub-header h3{
                margin:0;
                font-family:'Sora',sans-serif;
                font-size:2.6rem;
                font-weight:700;
                color:#063B00;
            }
            
            
            /* Text input container */
            div[data-testid="stTextInput"]{
                margin-bottom: 1rem;
            }
            /* Input box */
            div[data-testid="stTextInput"] input{
                background:#FFFFFF !important;
                color:#063B00 !important;
                border:2px solid #063B00 !important;
                border-radius:12px !important;
                padding:0.7rem 1rem !important;
                font-size:1rem !important;
                caret-color:#063B00 !important;
            }
            /* Placeholder */
            div[data-testid="stTextInput"] input::placeholder{
                color:#7B7B7B !important;
                opacity:1 !important;
            }
            /* Label */
            div[data-testid="stTextInput"] label{
                color:#063B00 !important;
                font-weight:600 !important;
            }
            /* Focus */
            div[data-testid="stTextInput"] input:focus{
                border:2px solid #4B5694 !important;
                box-shadow:0 0 0 3px rgba(75,86,148,.15) !important;
            }
            div[data-testid="stDivider"] hr {
                border-top: 2px solid #063B00 !important;
                opacity: 1 !important;
            }
            
            /* Primary button */
            button[data-testid="stBaseButton-primary"]{
                background-color:#BA5A5A !important;
                color:#FFF8EC !important;
                border:none !important;
            }

            /* Secondary button */
            button[data-testid="stBaseButton-secondary"]{
                background-color:#4B5694 !important;
                color:white !important;
                border:none !important;
            }
            
            div.stButton > button:hover{
                transform:scale(1.05);
            }
            
            
            /* Remove top padding */
            .block-container{
            padding-top: 0.2rem;
            padding-bottom: 0rem;
            }
                      
            </style>
            """,
        unsafe_allow_html=True,
    )
