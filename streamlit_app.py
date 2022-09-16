import streamlit as st
from moviepy.editor import VideoFileClip

st.title('🎈 Animated GIF Maker')

uploaded_file = st.file_uploader("Choose a file", type=['mov', 'mp4'])

if uploaded_file is not None:
  clip = VideoFileClip(uploaded_file)
  st.write(clip.w)
