import streamlit as st
from main import init, cleanup, zoom_video, flip_video, cleanup_input
import os
import subprocess
from streamlit_extras.switch_page_button import switch_page

st.markdown(""" <style> section[data-testid="stSidebar"][aria-expanded="true"]{ display: none; } </style> """, unsafe_allow_html=True)

st.title("AdSauce")
st.header("Select Processing")
# st.write('#')

if "is_processed" not in st.session_state:
    st.session_state.is_processed = False


if 'fname' and 'input_folder' in st.session_state:
    zoom = st.toggle("Zoom Video")
    if zoom:
        factor_percent = st.slider("Zoom Factor", 100, 200)
    flip = st.toggle("Flip Video")

    submit = st.button("Submit")

    if submit:
        if zoom or flip:
            st.session_state.is_processed = True
            with st.status("Processing Video"):
                video_path = os.path.join(st.session_state.input_folder, st.session_state.fname)
                init()
                cleanup()
                if zoom:
                    st.write("Zooming on videos...")
                    zoom_video(video_path, factor_percent)
                if flip:
                    st.write("Flipping videos...")
                    if zoom:
                        video_name =os.listdir(st.session_state.output_folder)[0]
                        video_path = os.path.join(st.session_state.output_folder, video_name)
                        flip_video(video_path)
                        os.remove(video_name)
                    else:
                        flip_video(video_path)
                st.write("Finalizing..")
                # cleanup_input()
        else:
            st.error("Please Select atleast one Processing")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Original Video")
        st.video(st.session_state.input_folder+'/'+st.session_state.fname)
    if st.session_state.is_processed:
        with c2:
            st.subheader("Final Video")
            outputFname = os.listdir(st.session_state.output_folder)[0]
            st.video(st.session_state.output_folder+'/'+outputFname)
            st.download_button("Download", open(st.session_state.output_folder+'/'+outputFname, 'rb'), file_name=outputFname)          

else:
    st.error("There is some error! Please go to home page")
    if st.button('Home'):
        switch_page('app')