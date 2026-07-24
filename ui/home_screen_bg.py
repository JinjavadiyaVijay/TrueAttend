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
                    background: #B2D959 !important;
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
            
            h3,h4,p{
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
                gap: 20px !important;
                width: 80% !important;
            }

            .header img {
                width: 90px !important;
                border-radius: 18px !important;
                padding-left: 5px !important;
            }

            .header h1,
            .header h2 {
                font-family:'Sonsie One',sans-serif !important;
                font-size:2rem !important;
                color:#FFF8EC !important;
                line-height:1.1 !important;
                margin-bottom:0 !important;
            }
            
            h3,h4,p{
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
