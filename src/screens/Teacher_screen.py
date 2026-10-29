
import streamlit as st
from src.components.header import header_dashboard
from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.database.db import teacher_exists,create_teacher,teacher_login,get_teacher_subject,get_attendence_for_teacher
from src.components.dailogue_create import create_subject_dailogue
from src.components.subject_card import subject_card
from src.components.dailogue_sahre import share_subject_dialgue
from src.components.dailogue_add_photos import add_photos_dailogue
from src.pipelines.face_pipeline import predict_attendence
from src.database.config import supabase
import numpy as np
from datetime import datetime
import pandas as pd
from src.components.dailogue_attendence_add import attendance_result_dialogue
from src.components.dailogue_voice_attendence import voice_attendece_dialog
from src.components.dailogue_attendence_add import show_attendance_result



def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if 'teacher_data' in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=='login':
        teacher_screen_login()
    elif st.session_state.teacher_login_type=='register':
        teacher_screen_regiter()


    # c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    # with c1:
    #     header_dashboard()
    # with c2:
    #     st.button('Go back to Home',type='secondary',key='loginbackbtn',shortcut='control+backspace')



    # st.header('Login Using Password')
def teacher_dashboard():
    teacher_data=st.session_state.teacher_data
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f'''Welcome, {teacher_data['name']}''')
        if st.button('Logout',type='secondary',key='loginbackbtn',shortcut='control+backspace'):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data
            st.rerun()
        
    st.space()

    if 'current_teacher_tab' not in st.session_state:
        st.session_state.current_teacher_tab='take_attendence'
    tab1,tab2,tab3=st.columns(3)


    with tab1:
        type1='primary' if st.session_state.current_teacher_tab =='take_attendence' else 'tertiary'
        if st.button('Take Attendence',type=type1,width='stretch',icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab='take_attendence'
            st.rerun()

    with tab2:
        type2='primary' if st.session_state.current_teacher_tab =='manage_subjects' else 'tertiary'
        if st.button('Manage Subjects',type=type2,width='stretch',icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab='manage_subjects'
            st.rerun()

    with tab3:
        type3='primary' if st.session_state.current_teacher_tab =='attendence_records' else 'tertiary'
        if st.button('Attendence Records',type=type3,width='stretch',icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab='attendence_records'
            st.rerun()


    st.divider()

    if st.session_state.current_teacher_tab=='take_attendence':
        teacher_tab_take_attendence()
    if st.session_state.current_teacher_tab=='manage_subjects':
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab=='attendence_records':
        teacher_tab_attendence_records()



def teacher_tab_take_attendence():
    teacher_id=st.session_state.teacher_data['teacher_id']
    st.header('Take AI Attendence')

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images=[]

    subjects=get_teacher_subject(teacher_id)
    if not subjects:
        st.warning('You have not created subjects yet! Please create one to begin')
        return

    subject_options={f'{s["name"]}-{s["subject_code"]}':s['subject_id'] for s in subjects}

    col1,col2=st.columns([3,1],vertical_alignment='bottom')

    with col1:
            selected_subject_label=st.selectbox('Select Subject',options=list(subject_options.keys()))

    with col2:
        if st.button('Add Photos',type='primary',icon=':material/photo_prints:',width='stretch'):
            add_photos_dailogue()

    selected_subject_id=subject_options[selected_subject_label]
    st.divider()

    if st.session_state.attendance_images:
        st.header('Add photos')
        gallery_cols=st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx%4]:
                st.image(img,width='stretch',caption=f'Photo{idx+1}')
    has_photos=bool(st.session_state.attendance_images)
    c1,c2,c3=st.columns(3)
    with c1:
        if st.button('Clear All Photos',width='stretch',type='tertiary',icon=':material/delete:',disabled=not has_photos):
            st.session_state.attendance_images=[]

    with c2:
        
        if st.button('Run face analysis',width='stretch',type='secondary',icon=':material/analytics:',disabled=not has_photos):
            with st.spinner('Deep scanning classroom photos'):
                all_detected_id={}
                for idx,img in enumerate(st.session_state.attendance_images):
                    img_np=np.array(img.convert('RGB'))
                    detected,_,_=predict_attendence(img_np)
                    if detected:
                        for sid in detected.keys():
                            student_id=int(sid)
                            all_detected_id.setdefault(student_id,[]).append(f'Photo{idx+1}')
                enrolled_res=supabase.table('subject_student').select('*,student(*)').eq('subject_id',selected_subject_id).execute()
                # print("selected_subject_id:", selected_subject_id)
                # print("enrolled rows:", enrolled_res.data)
                enrolled_students=enrolled_res.data
                if not enrolled_students:
                    st.warning('No students enrolled in this Course')
                else:
                    results,attendece_to_log=[],[]
                    current_time = datetime.now().isoformat(timespec="seconds")

                    for node in enrolled_students:
                        student=node['student']
                        source=all_detected_id.get(int(student['student_id']),[])
                        is_present=len(source)>0
                        results.append({
                            'Name':student['name'],
                            'ID':student['student_id'],
                            'Source':", ".join(source) if is_present else'-',
                            'Status':'Present' if is_present else 'Absent'

                        })
                        attendece_to_log.append({
                            'student_id':student['student_id'],
                            'subject_id':selected_subject_id,
                            'timestamp':current_time,
                            'is_present':bool(is_present)

                        })
                    st.session_state.face_results=(pd.DataFrame(results),attendece_to_log)

    with c3:
        if st.button('Use Voice attendence ',type='primary',width='stretch',icon=':material/mic:'):
            voice_attendece_dialog(selected_subject_id)
    if st.session_state.get('face_results'):
        df_res,logs=st.session_state.face_results
        show_attendance_result(df_res,logs)

def teacher_tab_manage_subjects():
    teacher_id=st.session_state.teacher_data['teacher_id']
    col1,col2=st.columns(2)
    with col1:
        st.header('Manage Subjects',width='stretch')
    with col2:
        if st.button('Create new Subject',width='stretch'): 
            create_subject_dailogue(teacher_id)

    subjects=get_teacher_subject(teacher_id)
    if subjects:
        for sub in subjects:
            stats=[
                ('👥','Students',sub['total_students']),
                ('🏫','Classes',sub['total_classes']),
            ]
            def share_btn():
                if st.button(f"Share Code:{sub['name']}",key=f"share_{sub['subject_code']}",icon=':material/share:'):
                    share_subject_dialgue(sub['name'],sub['subject_code'])
                st.space()
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_btn
            )
    else:
        st.info('No subject found.Create one Above')        



def teacher_tab_attendence_records():
    st.header('Attendence Record')

    teacher_id=st.session_state.teacher_data['teacher_id']
    records=get_attendence_for_teacher(teacher_id)
    if not records:
        st.info("No attendance records found yet.")
        st.caption("Take attendance in a class and the records will appear here.")
        return
    data=[]
    for r in records:
        ts=r.get('timestamp')
        data.append({
            'ts_group':ts.split(".")[0] if ts else None,
            'Time':datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N'A",
            'subject':r['subject']['name'],
            'Subject_code':r['subject']['subject_code'],
            'is_present':bool(r.get('is_present',False))
        })
    df=pd.DataFrame(data)
    summary=(
        df.groupby(['ts_group','Time','subject','Subject_code'])
        .agg(
            present_count=('is_present','sum'),
            total_count=('is_present','count')
            ).reset_index()
    )

    summary['Attendence Stats']=(
        summary['present_count'].astype(str)+'/'+summary['total_count'].astype(str)+'students'
    )
    display_df=(summary.sort_values(by='ts_group',ascending=False)
                [['Time','subject','Subject_code','Attendence Stats']]
                )
    st.dataframe(display_df,width='stretch',hide_index=True)

def login_teacher(username,passward):
    if not username or not passward:
        return False
    teacher=teacher_login(username,passward)

    if teacher:
        st.session_state.user_role='teacher'
        st.session_state.teacher_data=teacher
        st.session_state.is_logged_in=True
        return True
    return False

def teacher_screen_login():
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button('Go back to Home',type='secondary',key='loginbackbtn',shortcut='control+backspace'):
            st.session_state['login_type'] = None
            st.rerun()
    
    st.header('Login Using Password')
    st.space()
    st.space()

    teacher_username=st.text_input('Enter UserName',placeholder='Farhan')
    teacher_pass=st.text_input('Enter passward',type='password',placeholder='Enter passward')
    st.divider()
    btnc1,btnc2=st.columns(2)
    
    with btnc1:
        if st.button('Login',icon=':material/passkey:',shortcut='control+enter',width='stretch'):
            if login_teacher(teacher_username,teacher_pass):
                st.toast("welcome back")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error('Invalid username and passward')
    with btnc2:
            if st.button('Register Instead',icon=':material/passkey:',type='primary',width='stretch'):
                st.session_state.teacher_login_type="register"
            

def register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm):
    if not teacher_name or not teacher_pass or not teacher_username:
        return False,"All fields are required"
    if teacher_exists(teacher_username):
        return False,"Username already taken"
    if teacher_pass != teacher_pass_confirm:
        return False,"passward does not match"
    try:
        create_teacher(teacher_username,teacher_name,teacher_pass)
        return True,"Succesfully Created,Login now"
    except Exception as e:
        return False,f"Unexpected Error{e}"


def teacher_screen_regiter():
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button('Go back to Home',type='secondary',key='registerbackbtn',shortcut='control+backspace'):
            st.session_state['login_type']=None
            st.rerun()


    st.header('Register your teacher profile')
    st.space()
    st.space()

    teacher_username=st.text_input("Enter username",placeholder='Farhankhan12345')
    teacher_name=st.text_input("Enter Name",placeholder='Farhan')
    teacher_pass=st.text_input("Enter Passward",placeholder='Enter passward',type='password')
    teacher_pass_confirm=st.text_input("Confirm passward",placeholder='Enter passward',type='password')

    st.divider()

    btnc1,btnc2=st.columns(2)

    with btnc1:
        if st.button('Register now',icon=':material/passkey:',shortcut='control+enter',width='stretch'):
            succes,message=register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm)
            if succes:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type="login"
                st.rerun()
            else:
                st.error(message)

    with btnc2:
            if st.button('Login Instead',icon=':material/passkey:',type='primary',width='stretch'):
                st.session_state.teacher_login_type='login'
                st.rerun()




    

