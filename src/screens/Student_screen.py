import streamlit as st
from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.components.header import header_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendence,train_classifier,get_face_embeddings
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students,create_student,get_student_attendence,get_student_subject,unenroll_student_to_subject,enroll_student_to_subject
import time
from src.components.dailogue_enroll import enroll_dialogue
from src.components.subject_card import subject_card




def student_dashboard():
    student_data=st.session_state.student_data
    student_id=student_data['student_id']
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f'''Welcome, {student_data['name']}''')
        if st.button('Logout',type='secondary',key='loginbackbtn',shortcut='control+backspace'):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data
            st.rerun()
        
    st.space()

    col1,col2=st.columns(2)
    with col1:
        st.header('Your enrolled Subjects')

    with col2:
        if st.button('Enroll in subject',type='primary',width='stretch'):
            enroll_dialogue()

    st.divider()

    with st.spinner('Loading your enrolled subjects'):
        subjects=get_student_subject(student_id)
        logs=get_student_attendence(student_id)

    stats_map={}
    for log in (logs or []):
        sid=log['subject_id']
        if sid not in stats_map:
            stats_map[sid]={'total':0,'attended':0}
            stats_map[sid]['total']+=1
            if log.get('is_present'):
                stats_map[sid]['attended']+=1

    cols=st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub=sub_node['subject']
        sid=sub['subject_id']

        stats=stats_map.get(sid,{'total':0,'attended':0})
        def unenroll_button():
            if st.button('Unenroll from this course',type='primary',width='stretch',icon=':material/delete:'):
                unenroll_student_to_subject(student_id,sid)
                st.toast(f"Unenrolled from {sub['name']}successfully!")
                st.rerun()


        with cols[i%2]:
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    ('','Total',stats['total']),
                    ('','Attended',stats['attended']),
                ],
                footer_callback=unenroll_button
            )



def student_screen():
    
    style_background_dashboard()
    style_base_layout()


    if 'student_data' in st.session_state:
        student_dashboard()
        return 
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button('Go back to Home',type='secondary',key='studentbackbtn',shortcut='control+backspace'):
            st.session_state['login_type'] = None
            st.rerun()
    st.header('Login using FaceID',text_alignment='center')
    st.space()
    st.space()
    show_register = False 
    photo_source=st.camera_input('Position your face in center')
    if photo_source:
        img=np.array(Image.open(photo_source))

        with st.spinner('AI is scanning..'):
            detected,all_ids,num_faces=predict_attendence(img)

            if num_faces==0:
                st.warning('Face not found')
            elif num_faces>1:
                st.warning('Multiple faces found')
            else:
                if detected:
                    student_id=list(detected.keys())[0]
                    all_students=get_all_students()
                    student=next((s for s in all_students if s['student_id']==student_id),None)

                    if student:
                        st.session_state.is_logged_in=True
                        st.session_state.user_role='student'
                        st.session_state.student_data=student
                        st.toast(f"Welcome back {student['name']}")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info('Face not recognized! You might be new student')
                    show_register=True
    if show_register:
        with st.container(border=True):
            st.header('Register new profile')
            new_name=st.text_input('Enter your name ',placeholder='E.g Farhan Ullah')

            st.subheader('Optional : Voice Enrolment')
            st.info('Enroll for voice only attendence')

            audio_data=None
            try:
                audio_data=st.audio_input('Record a short phrase like i am present,My name is farhan')
            except Exception:
                st.error('Audio data failed')

            if st.button('Create Account',type='primary'):
                if new_name:
                    with st.spinner('Creating New Profile..'):
                        img=np.array(Image.open(photo_source))
                        encodings=get_face_embeddings(img)
                        if encodings:
                            face_emb=encodings[0].tolist()
                            voice_emb=None
                            if audio_data:
                                voice_emb=get_voice_embedding(audio_data.read())
                            response_data=create_student(new_name,face_embedding=face_emb,voice_embedding=voice_emb)
                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in=True
                                st.session_state.user_role='student'
                                st.session_state.student_data=response_data[0]
                                st.toast(f'Profile Created! Hi {new_name}')
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error('Could not Capture your facial feature for registration')
                else:
                    st.warning('Please enter your name')



