import streamlit as st

def style_background_home():

    st.markdown('''
            <style>
                    .stApp{
                        background:#5865F2 !important
                    
                    .stApp div[data-testid='stColumn']{
                        background-color:#E0E#3FF; !important;
                        padding:2.5rem !important;
                        border-radius:5rem !important;
                    }
                    }
            </style>
                    ''',unsafe_allow_html=True
                )


def style_background_dashboard():
    st.markdown(
        '''
        <style>
            .stApp {
                background-color: #E0E3FF !important;
            }

            [data-testid="stAppViewContainer"] {
                background-color: #E0E3FF !important;
            }
        </style>
        ''',
        unsafe_allow_html=True
    )
def style_base_layout():

    st.markdown('''
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Outfit:wght@100..900&display=swap');
            .stApp {
                background-color: #5865F2 !important;
            }
                #MainMenu,footer,header{
                    visibility:hidden;
                }
                .block-container{
                    padding-top:1.5rem !important
                }

                h1{
                    font-family:'Climate Crisis',sans-serif !important;
                    font-size:2rem !important;
                    line-height:1.1 !important;
                    margin-bottom:0rem !important;
                    color:black !important;
                }

                h2{
                    font-family:'Climate Crisis',sans-serif !important;
                    font-size:2rem !important;
                    line-height:0.9 !important;
                    margin-bottom:0rem !important;
                    color:black !important;
                }

                h3,h4,h5,h6,p{
                    font-family:'Outfit',sans-serif;
                    color:black !important;
                }
                div[data-testid="stAlert"],
                div[data-testid="stAlert"] > div,
                div[data-testid="stAlert"] [role="alert"],
                div[data-testid="stAlertContainer"] {
                    background: white !important;
                    background-color: white !important;
                    border-radius: 1rem !important;
                }

                div[data-testid="stAlert"] p,
                div[data-testid="stAlert"] svg {
                    color: black !important;
                    fill: black !important;
                }
                section[role="dialog"] {
                    background: white !important;
                    background-color: white !important;
                    border-radius: 1.5rem !important;
                }

                section[role="dialog"] h2,
                section[role="dialog"] h3,
                section[role="dialog"] h4,
                section[role="dialog"] p,
                section[role="dialog"] span {
                    color: black !important;
                }

                section[role="dialog"] button[aria-label="Close"] {
                    color: black !important;
                }

                section[role="dialog"] [data-testid="stCode"],
                section[role="dialog"] [data-testid="stCode"] pre {
                    background: #F0F2F6 !important;
                    background-color: #F0F2F6 !important;
                }

                section[role="dialog"] [data-testid="stCode"] code,
                section[role="dialog"] [data-testid="stCode"] code span,
                section[role="dialog"] code {
                    color: black !important;
                    background-color: #F0F2F6 !important;
                }
                                [data-testid="stToastContainer"] {
                    width: auto !important;
                    max-width: 90vw !important;
                }

                [data-testid="stToast"] {
                    width: fit-content !important;
                    min-width: 0 !important;
                    max-width: 90vw !important;
                }

                [data-testid="stToast"],
                [data-testid="stToast"] > div,
                [data-testid="stToastContainer"] > div {
                    background-color: black !important;
                    border-radius: 1rem !important;
                }

                [data-testid="stToast"] > div {
                    width: auto !important;
                    min-width: 0 !important;
                }

                [data-testid="stToast"] p,
                [data-testid="stToast"] span,
                [data-testid="stToast"] div {
                    color: white !important;
                }

                [data-testid="stToast"] button,
                [data-testid="stToast"] svg {
                    color: white !important;
                    fill: white !important;
                }
                button[kind='secondary'],
                button[kind='secondary'] p,
                button[kind='secondary'] span {
                    border-radius: 1.5rem !important;
                    background-color: #EB459E !important;
                    color: white !important;
                    # padding: 10px 10px !important;
                    border: none !important;
                    transition: transform 0.25s ease-in-out !important;
                    font-size: 14px !important;
                }

                button[kind='tertiary'],
                button[kind='tertiary'] p,
                button[kind='tertiary'] span {
                    border-radius: 1.5rem !important;
                    background-color: black !important;
                    color: white !important;
                    # padding: 10px 20px !important;
                    border: none !important;
                    transition: transform 0.25s ease-in-out !important;
                    font-size: 14px !important;
                }

                button[kind='primary'],
                button[kind='primary'] p,
                button[kind='primary'] span {
                    border-radius: 1.5rem !important;
                    background-color: #5865F2 !important;
                    color: white !important;
                    # padding: 10px 20px !important;
                    border: none !important;
                    transition: transform 0.25s ease-in-out !important;
                    font-size: 14px !important;
                }

                button:hover {
                    transform: scale(1.05);
                }

            </style>
                    '''
                ,unsafe_allow_html=True
                )