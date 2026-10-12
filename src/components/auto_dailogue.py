import streamlit as st
import time
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
@st.dialog('Quick Enrollment')

def auto_enroll_dailogue(subject_code):
    student_id=st.session_state.student_data['student_id']

    res=supabase.table('subject').select('subject_id,name').eq('subject_code',subject_code).execute()
    if not res.data:
        st.error('Subject code not found')
        if st.button('Close'):
            st.query_params.clear()
            st.rerun()

    subject=res.data[0]

    check=supabase.table('student_subject').select('*').eq('subject',subject['subject_id']).eq('student_id',student_id).execute()
    if check.data:
        st.info('You are already enrolled')
        if st.button('Got it'):
            st.query_params.clear()
            st.rerun()
        return
    st.markdown(f'Would you like to enroll in **{subject["name"]}**')

    col1,col2=st.columns(2)
    with col1:
        if st.button('No thanks'):
            st.query_params.clear()
            st.rerun()
        return
    with col2:
        if st.button('Yes enroll now',type='primary',width='stretch'):
            enroll_student_to_subject(subject_id,subject['subject_id'])
            st.success('joined successfully')
            st.query_params.clear()
            time.sleep(2)
            st.rerun()
