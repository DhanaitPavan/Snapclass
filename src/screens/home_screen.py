import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_background_home , style_base_layout
import time

def home_screen():

    header_home() 

    style_background_home() 
    style_base_layout()


    col1, col2 = st.columns(2, gap="large")

    with col1:

        st.header("I'm Student")
        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=120)
        if st.button("Student Portal", type="primary", icon=":material/arrow_outward:"):
            with st.spinner("Going to Student Portal..."):
                st.session_state['login_type'] = "student"
                time.sleep(2)
                st.rerun()  # Rerun the app to reflect the change in login_type       

    with col2:

        st.header("I'm Teacher")
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=145)
        if st.button("Teacher Portal" ,type="primary", icon=":material/arrow_outward:"):
            with st.spinner("Going to Teacher Portal..."):
                st.session_state['login_type'] = "teacher"
                time.sleep(2)
                st.rerun()  # Rerun the app to reflect the change in login_type
        
    footer_home()  # Call the footer function to display the footer