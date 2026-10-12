import streamlit as st
from src.pipelines.voice_pipeline import process_bulk_audio
from src.database.config import supabase
from datetime import datetime
from src.components.dailogue_attendence_add import show_attendance_result
import pandas as pd


@st.dialog('Voice Attendence')
def voice_attendece_dialog(selected_subject_id):
    st.write('Record audio of students saying I am present')
    audio_date=None
    audio_date=st.audio_input('Record classroom audio')

    if st.button('Analyze Audio',width='stretch',type='primary'):
        if audio_date is None:
            st.warning("Please record classroom audio first.")
            return
        with st.spinner('Processing audio data'):
            enrolled_res=supabase.table('subject_student').select('*,student(*)').eq('subject_id',selected_subject_id).execute()
            enrolled_students=enrolled_res.data
            if not enrolled_students:
                st.warning('No students enrolled in this Course')
                return
            condidates_dict={
                s['student']['student_id']:s['student']['voice_embed']
                for s in enrolled_students if s['student'].get('voice_embed')
            }

            if not condidates_dict:
                st.error('No enrolled students have voice profiles register')
                return
            audio_bytes=audio_date.read()

            detected_scores=process_bulk_audio(audio_bytes,condidates_dict)


            results,attendece_to_log=[],[]
            current_time=datetime.now().strftime("%Y-%m-%dT%H%M%S")

            for node in enrolled_students:
                student=node['student']
                score=detected_scores.get(student['student_id'],0.0)
                is_present=bool(score>0)
                results.append({
                    'Name':student['name'],
                    'ID':student['student_id'],
                    'Source':score if is_present else'-',
                    'Status':'Present' if is_present else 'Absent'

                })
                attendece_to_log.append({
                    'student_id':student['student_id'],
                    'subject_id':selected_subject_id,
                    'timestamp':current_time,
                    'is_present':bool(is_present)

                })

            st.session_state.voice_attendance_results=(pd.DataFrame(results),attendece_to_log)
            if st.session_state.get('voice_attendance_results'):
                st.divider()
                df_results,logs=st.session_state.voice_attendance_results
                show_attendance_result(df_results,logs)