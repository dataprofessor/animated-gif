import streamlit as st
from moviepy.editor import VideoFileClip

st.title('🎈 Animated GIF Maker')

uploaded_file = st.file_uploader("Choose a file", type=['mov', 'mp4'])

if uploaded_file is not None:
  # Save to temp file
  tfile = tempfile.NamedTemporaryFile(delete=False) 
  tfile.write(f.read())
  # Open file
  clip = VideoFileClip(uploaded_file)
  # Display width of video
  st.write(clip.w)
else:
  st.warning('☝️ Upload a video file')
