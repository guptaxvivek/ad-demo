import streamlit as st
from main import init, cleanup, zoom_video, flip_video, cleanup_input, copy_video, filter_video
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
    keys = st.text_input("Enter Keywords (Seperated by ','): ")
    if keys:
        keywords = keys.split(",")
    
    zoom = st.toggle("Zoom Video")
    if zoom:
        factor_percent = st.slider("Zoom Factor", 100, 200)
    flip = st.toggle("Flip Video")
    color_filter = st.toggle("Color Filter")
    if color_filter:
        filter = st.radio("Select Filter", ["Sepia","Black-White","Invert"])
        if filter:
            intensity = st.slider("% Opacity",1,100)

    submit = st.button("Submit")


    if submit:
        if zoom or flip or color_filter:
            st.session_state.is_processed = True
            with st.status("Processing Video"):
                video_path = os.path.join(st.session_state.input_folder, st.session_state.fname)
                init()
                cleanup()
                if zoom:
                    st.write("Zooming on videos...")
                    zoom_video(video_path, factor_percent, keywords)
                if flip:
                    st.write("Flipping videos...")
                    if zoom:
                        video_name =os.listdir(st.session_state.output_folder)[0]
                        video_path = os.path.join(st.session_state.output_folder, video_name)
                        flip_video(video_path, keywords)
                        os.remove(video_path)
                    else:
                        flip_video(video_path, keywords)
                if color_filter:
                    st.write("Applying Filter...")
                    if zoom or flip:
                        video_name =os.listdir(st.session_state.output_folder)[0]
                        video_path = os.path.join(st.session_state.output_folder, video_name)
                        filter_video(video_path, filter, keywords, intensity)
                        os.remove(video_path)
                    else:
                        filter_video(video_path, filter, keywords, intensity)
                st.write("Finalizing..")
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