def subject_card(name, code, section, stats=None, footer_callback=None):
    import streamlit as st
    html = f'''
    <div style="
        background: white;
        border-left: 8px solid #EB459E;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid black;
        margin-bottom: 20px;
        color: black;                 /* force black on the whole card */
    ">
        <h3 style="margin:0; color:black; font-size:1.5rem;">{name}</h3>
        <p style="color:black; margin:10px 0;">
            Code: <span style="background:#E0E3FF; color:black; padding:2px 6px; border-radius:6px;">{code}</span>
            | Section: {section}
        </p>
    '''

    if stats:
        html += '<div style="display:flex; gap:20px; flex-wrap:wrap; margin-top:12px;">'
        for icon, label, value in stats:
            html += f'''
            <div style="
                background:#E0E3FF;
                color:black !important;
                padding:5px 12px;
                border-radius:12px;
                font-size:0.9rem;
            ">
                {icon} <b>{value}</b> {label}
            </div>'''
        html += '</div>'

    html += '</div>'          # close the main card div
    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()