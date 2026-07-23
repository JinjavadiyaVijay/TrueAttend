import streamlit as st


# home screen
def home_screen_bg():
    st.markdown(
        """
        <style>
                .stApp {
                    background: #063B00 !important;
                }
        </style>
                """,
        unsafe_allow_html=True,
    )


# deshboard
def deshboard_screen_bg():
    st.markdown(
        """
        <style>
                .stApp {
                    background: #A1BC98 !important;
                }
        </style>
                """,
        unsafe_allow_html=True,
    )


def style_base_layout():
    st.markdown(
        """
            <style>
                 @import url('https://fonts.googleapis.com/css2?family=BBH+Bartle&family=Sonsie+One&family=Sora:wght@100..800&display=swap');;

                    /*Hide default toolbar*/
                    #MainMenu, footer,header{
                        visibility : hidden;
                        }

                    h1,
                    h2 {
                        font-family: 'Sonsie One', sans-serif !important;
                        font-size:3.9rem !important;
                        color: #FFF8EC !important;
                        line-heigth: 1.1 !important;
                        margin-bottom:0rem !important;
                    }

                    h3,
                    h4,
                    p
                    {
                        font-family: 'Sora', sans-serif !important;
                        color: #FFF8EC !important;
                     }
            </style>

    """,
        unsafe_allow_html=True,
    )
