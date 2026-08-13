import streamlit as st

def style_background_home():
    st.markdown("""
    <style>
        .stApp {

            background : #5865F2 !important;
            
            }

        .stApp [data-testid="stColumn"] {
            background-color: #E0E3FF !important;
            padding: 2.5rem !important;
            border-radius: 5rem !important;

        }
    </style>
    """, unsafe_allow_html=True)



def style_background_dashboard():
    st.markdown("""
    <style>
    
        .stApp {

            background: #E0E3FF !important;
            
            }
    </style>
    """, unsafe_allow_html=True)


def style_base_layout():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap'); 
    @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Outfit:wght@100..900&display=swap');

        /* Hide Top bar of Streamlit */

            #MainMenu, header, footer {
                visibility: hidden;
            }
            
            .block-container {
                padding-top:1.5rem; !important;
            }

            h1{
            
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 3.5rem !important;
                line-height: 1.1 !important;
                margin-bottom: 0 !important;
            }

            h2{
            
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 2 rem !important;
                line-height: 0.9 !important;
                margin-bottom: 0 !important;
            }

            h3, p, h4{
            
                font-family: 'Outfit', sans-serif !important;
            }

            button{ 
                border-radius: 1.5rem !important;
                background-color: #5865F2 !important;
                color: white !important; 
                padding: 10px 20px !important;
                border: none !important;
                transition: all 0.3s ease-in-out !important;

            }

            div.stButton > button:hover {
                background-color: #d43f3f !important;
                transform: translateY(-2px);
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.15);
            }

            /* Active / Click state */
            div.stButton > button:active {
                transform: translateY(0px);
            }  
            

            button[kind="secondary"]{ 
                border-radius: 1.5rem !important;
                background-color: #EB459E !important;
                color: white !important; 
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;           
            }
            
            button[kind="tertiary"]{ 
                border-radius: 1.5rem !important;
                background-color: black !important;
                color: white !important; 
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;           
            }
    </style>
    """, unsafe_allow_html=True)