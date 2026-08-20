import streamlit as st
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.database.db import check_teacher_exist, create_teacher, teacher_login, get_teacher_subjects, get_attendance_for_teacher
from src.components.create_dialog_subject import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.share_dialog_subject import share_dialog_subject
from src.components.dialog_add_photos import add_photos_dialog
import numpy as np
from PIL import Image
from src.database.config import supabase
from src.pipelines.face_pipeline import predict_attendance
from datetime import datetime
import pandas as pd
from src.components.dialog_attendance_result import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
import time


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
        st.subheader(f"👋 Welcome, {teacher_data['name']}")
        if st.button("Logout", type="secondary", key="loginbackbtn", shortcut="control+backspace"):
            with st.spinner("Teacher Logout..."):
                st.session_state['is_logged_in'] = False
                del st.session_state.teacher_data
                time.sleep(1.5)
                st.rerun() 

    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab= 'take_attendence'
    tab1, tab2, tab3=st.columns(3)


    with tab1:
        type1="primary" if st.session_state.current_teacher_tab== 'take_attendence' else "tertiary"
        if st.button('Take Attendence', type=type1 ,width='stretch', icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab= 'take_attendence'
            time.sleep(1)
            st.rerun()

    with tab2:
        type2="primary" if st.session_state.current_teacher_tab== 'manage_subjects' else "tertiary"
        if st.button('Manage Subjects',type=type2 ,width='stretch', icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab= 'manage_subjects'
            time.sleep(1)
            st.rerun()

    with tab3:
        type3="primary" if st.session_state.current_teacher_tab== 'attendence_records' else "tertiary"
        if st.button('Attendence Records',type=type3 , width='stretch', icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab= 'attendence_records'
            time.sleep(1)
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
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header('Take AI Attendance')


    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning('You havent created any subjects yet! Please create one to begin!')
        return
    
    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3,1], vertical_alignment='bottom')

    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))

    with col2:
        if st.button('Add Photos', type='primary', icon=':material/photo_prints:', width='stretch'):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.header('Added Photos')
        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4 ]:
                st.image(img, width='stretch', caption=f'Photo {idx+1}')
    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button('Clear all photos', width='stretch', type='tertiary', icon=':material/delete:', disabled=not has_photos):
            with st.spinner("Clearing photos.."):
                st.session_state.attendance_images = []
                time.sleep(1)
                st.rerun()


    with c2:
        
        if st.button('Run Face Analysis', width='stretch', type='secondary', icon=':material/analytics:', disabled=not has_photos):
            with st.spinner('Deep scanning classroom photos...'):
                all_detected_ids = {}

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected, _, _ = predict_attendance(img_np)


                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)

                            all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}")

                enrolled_res = supabase.table('subject_students').select("*, students(*)").eq('subject_id',selected_subject_id ).execute()
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning('No students enrolled in this course')
                else:

                    results, attendance_to_log  = [], []

                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


                    for node in enrolled_students:
                        student = node['students']
                        sources = all_detected_ids.get(int(student['student_id']), [])
                        is_present= len(sources) > 0

                        results.append({
                            "Name": student['name'],
                            "ID": student['student_id'],
                            "Source": ", ".join(sources) if is_present else "-",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })

                        attendance_to_log.append({
                            'student_id': student['student_id'],
                            'subject_id': selected_subject_id,
                            'timestamps': current_timestamp,
                            'is_present': bool(is_present)
                        })

                    attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

    with c3:
        if st.button('Use Voice Attendance', type='primary', width='stretch', icon=':material/mic:'):
            voice_attendance_dialog(selected_subject_id)







def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    
    # Grid layout for the header actions
    col1, col2 = st.columns([3, 1])  # 3:1 ratio handles sizing better than 'width'
    with col1:
        st.header("Manage Subjects")

    with col2:
        # Streamlit buttons automatically stretch to container width inside columns
        if st.button('Create New Subject', use_container_width=True):
            create_subject_dialog(teacher_id)

    # Fetch and list all Subjects
    subjects = get_teacher_subjects(teacher_id)
    
    if subjects:
        for sub in subjects:
            # Stats dynamically built for the current subject
            stats = [
                ("🫂", "Students", sub['total_students']),
                ("🕰️", "Classes", sub['total_classes']),
            ]
            
            # Use unique keys by embedding the subject code
            button_key = f"share_{sub['subject_code']}"
            
            # Inline callback layout using a lambda to pass correct arguments safely
            def make_footer_callback(s_name=sub['name'], s_code=sub['subject_code']):
                def callback():
                    if st.button(f"Share Code: {s_name}", key=button_key, icon=":material/share:",width='content'):
                        share_dialog_subject(s_name, s_code)
                return callback

            # Render the card inside the loop so all subjects appear
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=make_footer_callback()
            )
            st.divider()
    else:
        st.info("NO SUBJECT FOUND. CREATE ONE ABOVE")



def teacher_tab_attendence_records():
    st.header("Attedences Records")

    teacher_id=st.session_state.teacher_data['teacher_id']

    records=get_attendance_for_teacher(teacher_id)

    if not records:
        return
    data=[]

    for r in records:
        ts= r.get('timestamps')

        data.append({
            'ts_group':ts.split(".")[0] if ts else None,
            'Time':datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
            'Subject':r['subjects']['name'],
            'Subject Code':r['subjects']['subject_code'],
            'is_present':(r.get('is_present', False))
        })

    df=pd.DataFrame(data)


    summary=(
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code']).agg(
            Present_Count=('is_present', 'sum'),
            Total_Count=('is_present', 'count')
        ).reset_index()
    )
    
    summary['Attendance_stats']=(
        "✅" + summary['Present_Count'].astype(str) + " /"
        + summary['Total_Count'].astype(str) + ' Students'
    )

    display_df= (summary.sort_values(by='ts_group' ,ascending=False)
                [['Time', 'Subject', 'Subject Code', 'Attendance_stats']])

    st.dataframe(display_df, width='stretch', hide_index=True)

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
            with st.spinner("Loging..."):
                if login_teacher(teacher_username, teacher_pass):
                    st.toast("Welcome back!", icon="👋")
                    import time
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid username and password!")

    with btn_col2:
        if st.button("Register", key="registerbtn", type="primary", icon=":material/person_add:", width='stretch'):
            with st.spinner("Going to Register..."):
                st.session_state.teacher_login_state = "register"
                import time
                time.sleep(1)

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
            with st.spinner("Going to Home..."):
                st.session_state['login_type'] = None
                import time
                time.sleep(0.8)
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
            with st.spinner("Creating Profile..."):
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
            with st.spinner("Loging..."):
                st.session_state.teacher_login_state = "login"
                import time
                time.sleep(1)
                

    footer_dashboard()  # Call the footer function to display the footer