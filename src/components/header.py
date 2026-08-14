import streamlit as st

def header_home():
    
    logo_url = "https://i.ibb.co/1Jj94M07/dc8bc56f-16ca-424f-ab25-dfad5d9b967f.png"   

    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: center; flex-direction: column; margin-bottom: 30px; margin-top: 30px;">
        <img src="{logo_url}" style="height: 100px;" />
        <h1 style="text-align: center; color: #E0E3FF;" >CAPT<br/> CLASS</h1>
    </div>
    
    """, unsafe_allow_html=True)

def header_dashboard():
    
    logo_url = "https://i.ibb.co/1Jj94M07/dc8bc56f-16ca-424f-ab25-dfad5d9b967f.png"   

    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
        <img src="{logo_url}" style="height: 85px;" />
        <h2 style="text-align: center; color: #5865F2;" >CAPT<br/> CLASS</h2>
    </div>
    
    """, unsafe_allow_html=True)