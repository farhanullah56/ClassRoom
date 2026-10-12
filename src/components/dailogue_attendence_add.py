import streamlit as st
from src.database.db import create_attendence


def show_attendance_result(df,logs):
    st.write('Please review attendence before conferming')
    st.dataframe(df,hide_index=True,width='stretch')
    col1,col2=st.columns(2)
    with col1:
        if st.button('Discard',width='stretch'):
            st.session_state.voice_attendance_results=None
            st.session_state.attendance_images=[]
            
            st.rerun()

    with col2:
        if st.button('Confirm and save',width='stretch'):
            try:
                create_attendence(logs)
                st.toast('Attendence taken')
                st.session_state.attendance_images=[]
                st.session_state.voice_attendance_results=None
                st.rerun()
            except Exception as e:
                st.error('Sync failed')

def attendance_result_dialogue(df,logs):
    show_attendance_result(df,logs)
    

