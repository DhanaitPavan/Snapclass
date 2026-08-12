import streamlit as st
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.database.db import check_teacher_exist, create_teacher, teacher_login, get_teacher_subjects
from src.components.create_dialog_subject import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.share_dialog_subject import share_dialog_subject

def teacher_screen():

    style_background_dashboard()  # Apply the dashboard background style
    style_base_layout()  # Apply the base layout style

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_state' not in st.session_state or st.session_state.teacher_login_state == "login":
        teacher_screen_login() 
    elif st.session_state.teacher_login_state == "register":
        teacher_screen_register()



 

def teacher_dashboard():
    teacher_data=st.session_state.teacher_data

    
    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f""" Welcome {teacher_data['name']}""")
        if st.button("Logout", type="secondary", key="loginbackbtn", shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data
            st.rerun() 

    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab= 'take_attendence'
    tab1, tab2, tab3=st.columns(3)


    with tab1:
        type1="primary" if st.session_state.current_teacher_tab== 'take_attendence' else "tertiary"
        if st.button('Take Attendence', type=type1 ,width='stretch', icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab= 'take_attendence'
            st.rerun()

    with tab2:
        type2="primary" if st.session_state.current_teacher_tab== 'manage_subjects' else "tertiary"
        if st.button('Manage Subjects',type=type2 ,width='stretch', icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab= 'manage_subjects'
            st.rerun()

    with tab3:
        type3="primary" if st.session_state.current_teacher_tab== 'attendence_records' else "tertiary"
        if st.button('Attendence Records',type=type3 , width='stretch', icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab= 'attendence_records'
            st.rerun()

    if st.session_state.current_teacher_tab=='take_attendence':
        teacher_tab_take_attendence()
    if st.session_state.current_teacher_tab=='manage_subjects':
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab=='attendence_records':
        teacher_tab_attendence_records()

    st.divider()

    footer_dashboard()

def teacher_tab_take_attendence():
    st.header("take attendeces tab")


def teacher_tab_manage_subjects():
    teacher_id=st.session_state.teacher_data['teacher_id']
    col1, col2=st.columns(2)
    with col1:
        st.header("Manage Subjects", width='stretch')

    with col2:
        if st.button('Create New Subject', width='stretch'):
            create_subject_dialog(teacher_id)

    #List all Subjects
    subjects=get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats=[
                ("🫂", "Students", sub['total_students']),
                ("🕰️", "Classes", sub['total_classes']),
            ]
        def share_btn():
            if st.button(f"Share Code: {sub['name']}", key=f"share_{sub['subject_code']}", icon=":material/share:"):
                share_dialog_subject(sub['name'], sub['subject_code'])
                st.space()


        subject_card(
            name=sub['name'],
            code=sub['subject_code'],
            section=sub['section'],
            stats=stats,
            footer_callback=share_btn
        )

    else:
        st.info("NO SUBJECT FOUND. CREATE ONE ABOVE")


def teacher_tab_attendence_records():
    st.header("Attedences record tab")

    

def login_teacher(username, password):
    if not username or not password:
        return False

    teacher = teacher_login(username, password)

    if teacher:
        st.session_state.user_role='teacher'
        st.session_state.teacher_data=teacher
        st.session_state.is_logged_in =True
        return True


    return False

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
        if st.button("Login", key="loginbtn", type="secondary", shortcut="control+enter", icon=":material/passkey:", width='stretch'):
            if login_teacher(teacher_username, teacher_pass):
                st.toast("Welcome back!", icon="👋")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username and password!")

    with btn_col2:
        if st.button("Register", key="registerbtn", type="primary", icon=":material/person_add:", width='stretch'):
            st.session_state.teacher_login_state = "register"

    footer_dashboard()  # Call the footer function to display the footer


def register_teacher(teacher_name, teacher_username, teacher_pass, teacher_pass_confirm):
    if not teacher_name or not teacher_username or not teacher_pass:
        return False, "Please fill in all fields."
    if check_teacher_exist(teacher_username):
        return False, "Username already exists. Please choose a different username."
    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords do not match. Please try again."

    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Teacher registered successfully. You can now log in."
    except Exception as e:
        return False, "Unexpected error!"

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
        if st.button("Register now", shortcut="control+enter", icon=":material/passkey:", width='stretch'):
            success, message = register_teacher(teacher_name, teacher_username, teacher_pass, teacher_pass_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)  # Wait for 2 seconds before switching to login screen
                st.session_state.teacher_login_type = "login"
                st.rerun()  # Rerun the app to switch to the login screen
            else:
                st.error(message) 

    with btn_col2:
        if st.button("Login Instead", type="primary", icon=":material/passkey:", width='stretch'):
            st.session_state.teacher_login_state = "login"

    footer_dashboard()  # Call the footer function to display the footer