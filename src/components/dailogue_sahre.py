import streamlit as st
import segno 
import io


@st.dialog('Share Class Link')

def share_subject_dialgue(subject_name,subject_code):
    app_domain='Classsroom-main.streamlit.app'
    join_url = f"https://{app_domain}/?join-code={subject_code}"

    st.markdown(f"### {subject_name}")                             
    st.caption(f"Subject Code: `{subject_code}`")                
    qr=segno.make(join_url)
    out=io.BytesIO()
    qr.save(out,kind='png',scale=10,border=1)
    col1,col2=st.columns(2)


    with col1:
        st.markdown('#### Copy Link')
        st.code(join_url,language='text')
        st.code(subject_code,language='text')
        st.info('Copy this link to share on whatsapp or Email')


    with col2:
        st.markdown('#### Scan to join')
        st.image(out.getvalue(),use_container_width=True,caption='QRCODE for joining Class')

