import streamlit as st
import tempfile
from moviepy.editor import VideoFileClip

st.title('🎈 Animated GIF Maker')

with st.form('my_form'):
  st.sidebar.header('Upload file')
  uploaded_file = st.sidebar.file_uploader("Choose a file", type=['mov', 'mp4'])
  
  submitted = st.sidebar.form_submit_button('Submit')

  if submitted:
    # Save to temp file
    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(uploaded_file.read())

    # Open file
    clip = VideoFileClip(tfile.name)

    # Display output
    col1, col2, col3 = st.columns(3)
    col1.metric('Width', clip.w, 'pixels')
    col2.metric('Height', clip.h, 'pixels')
    col3.metric('Duration', clip.duration, 'seconds')
  
  else:
    st.warning('☝️ Upload a video file')
