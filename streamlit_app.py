import streamlit as st
import tempfile
from PIL import Image
import numpy as np
from moviepy.editor import VideoFileClip

st.title('🎈 Animated GIF Maker')


st.sidebar.header('Upload file')
uploaded_file = st.sidebar.file_uploader("Choose a file", type=['mov', 'mp4'])

if uploaded_file is not None:
  # Save to temp file
  tfile = tempfile.NamedTemporaryFile(delete=False) 
  tfile.write(uploaded_file.read())
  
  # Open file
  clip = VideoFileClip(tfile.name)
  
  # Display output
  col1, col2, col3, col4, col5 = st.columns(5)
  col1.metric('Width', clip.w, 'pixels')
  col2.metric('Height', clip.h, 'pixels')
  col3.metric('Duration', clip.duration, 'seconds')
  col4.metric('FPS', clip.fps, '')
  col5.metric('Frames', clip.duration * clip.fps, 'frames')
  
  selected_frame = st.sidebar.slider('Select a time frame (s)', 0, int(clip.duration), int(np.median(clip.duration)) )
  selected_resolution_scaling = st.sidebar.slider('Scaling of video resolution', 0.0, 1.0, 0.5 )
  
  # Resizing of video
  clip = clip.resize(selected_resolution_scaling)
  
  # Extract video frame as a display image
  clip.save_frame('frame.jpg', t=selected_frame)
  frame_image = Image.open("frame.jpg")
  st.image(frame_image)
  st.write(frame_image.size)
  
else:
  st.warning('👈 Upload a video file')
