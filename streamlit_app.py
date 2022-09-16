import streamlit as st
import tempfile
from moviepy.editor import VideoFileClip

st.title('🎈 Animated GIF Maker')

uploaded_file = st.file_uploader("Choose a file", type=['mov', 'mp4'])

if uploaded_file is not None:
  # Save to temp file
  tfile = tempfile.NamedTemporaryFile(delete=False) 
  tfile.write(uploaded_file.read())
  
  # Open file
  clip = VideoFileClip(tfile.name)
  
  # Display output
  col1, col2, col3 = st.columns(3)
  col1.metric('Width', clip.w, '')
  col2.metric('Height', clip.h, '')
  col3.metric('Duration', clip.duration, '')
  
else:
  st.warning('☝️ Upload a video file')
