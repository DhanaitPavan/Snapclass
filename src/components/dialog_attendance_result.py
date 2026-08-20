import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
import time


from src.database.db import create_attendance

def show_attendance_result(df, logs):
    st.write('Please review attendance before confirming.')
    st.dataframe(df, hide_index=True, width='stretch')

    col1, col2 = st.columns(2)

    with col1:
        if st.button('Discard', width='stretch'):
            with st.spinner("Discarding.."):
                st.session_state.voice_attendance_results = None
                st.session_state.attendance_images = []
                time.sleep(0.7)
                st.rerun()

    with col2:
        if st.button('Confirm & Save', width='stretch', type='primary'):
            with st.spinner("Saving records..."):
                success = False
                try:
                    create_attendance(logs)
                    st.toast("Attendance taken")
                    st.session_state.attendance_images = []
                    st.session_state.voice_attendance_results = None
                    time.sleep(0.5) 
                    success = True
                except Exception as e:
                    print(f"Database Error: {e}")
                    st.error(f'Sync failed! Error: {e}')

                if success:
                    time.sleep(0.5) # Optional: gives the toast a moment to display
                    st.rerun()



@st.dialog("Attendance Reports")
def attendance_result_dialog(df, logs):
    show_attendance_result(df, logs)
    

