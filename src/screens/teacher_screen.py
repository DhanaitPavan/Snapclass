import streamlit as st
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.ui.base_layout import style_background_dashboard, style_base_layout



def teacher_screen():

    style_background_dashboard()  # Apply the dashboard background style
    style_base_layout()  # Apply the base layout style

    if 'teacher_login_state' not in st.session_state or st.session_state.teacher_login_state == "login":
        teacher_screen_login() 
    elif st.session_state.teacher_login_state == "register":
        teacher_screen_register()

def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go to back home", type="secondary", key="loginbackbtn", shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()  


    st.header("Login using Password", text_alignment='center')
    st.space()
    teacher_username=st.text_input("Enter username", placeholder="eg.abc123")
    teacher_pass=st.text_input("Enter password", placeholder="Enter password", type="password")

    st.divider()  # Add a divider line

    btn_col1, btn_col2 = st.columns(2)

    with btn_col1:
        st.button("Login", key="loginbtn", type="secondary", shortcut="control+enter", icon=":material/passkey:", width='stretch')

    with btn_col2:
        if st.button("Register", key="registerbtn", type="primary", icon=":material/person_add:", width='stretch'):
            st.session_state.teacher_login_state = "register"

    footer_dashboard()  # Call the footer function to display the footer

def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go to back home", type="secondary", key="registerbackbtn", shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()


    st.header("Register your teacher profile", text_alignment='center')

    teacher_name=st.text_input("Enter name", placeholder="eg. John Doe")

    teacher_username=st.text_input("Enter username", placeholder="eg.abc123")

    teacher_pass=st.text_input("Enter password", placeholder="Enter password", type="password")

    teacher_pass_confirm=st.text_input("Confirm Password", placeholder="Confirm Password", type="password")

    st.divider()  # Add a divider line

    btn_col1, btn_col2 = st.columns(2)

    with btn_col1:
        st.button("Register now", shortcut="control+enter", icon=":material/passkey:", width='stretch')

    with btn_col2:
        if st.button("Login Instead", type="primary", icon=":material/passkey:", width='stretch'):
            st.session_state.teacher_login_state = "login"

    footer_dashboard()  # Call the footer function to display the footer