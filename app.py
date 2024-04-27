import streamlit as st
import os
from streamlit_extras.switch_page_button import switch_page

st.session_state['input_folder'] = "input"
st.session_state['output_folder'] = "output"

def clean_input_folder(input_folder):
    if os.path.exists(input_folder):
        for filename in os.listdir(input_folder):
            file_path = os.path.join(input_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                st.error(f"Failed to delete {file_path}. Reason: {e}")
    else:
        try:
            os.mkdir(input_folder)
        except OSError as e:
            st.error(f"Failed to create {input_folder}. Reason: {e}")

st.set_page_config(page_title="AdSauce", page_icon="🎥")
st.markdown(""" <style> section[data-testid="stSidebar"][aria-expanded="true"]{ display: none; } </style> """, unsafe_allow_html=True)

st.title("AdSauce")
file = st.file_uploader("Choose a File",type=['avi', 'flv', 'mkv', 'mov', 'mp4', 'm4v', 'mpg', 'mpeg', 'm2v', 'webm'])
if file:
    clean_input_folder(st.session_state.input_folder)
    st.session_state['fname'] = file.name
    with open(os.path.join(st.session_state.input_folder, file.name), "wb") as f:
        f.write(file.getbuffer())
    switch_page('select_features')
    