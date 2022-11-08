import streamlit as st
import os
import base64
import tempfile
from PIL import Image
import numpy as np
from moviepy.editor import VideoFileClip
import moviepy.video.fx.all as vfx

## Session state ##
if 'clip_width' not in st.session_state:
    st.session_state.clip_width = 0
if 'clip_height' not in st.session_state:
    st.session_state.clip_height = 0
if 'clip_duration' not in st.session_state:
    st.session_state.clip_duration = 0
if 'clip_fps' not in st.session_state:
    st.session_state.clip_fps = 0
if 'clip_total_frames' not in st.session_state:
    st.session_state.clip_total_frames = 0  
    
st.title('🎈 Animated GIF Maker')

## Upload file ##
st.sidebar.header('Upload file')
uploaded_file = st.sidebar.file_uploader("Choose a file", type=['mov', 'mp4'])
st.sidebar.markdown('''
[Download example file](https://github.com/dataprofessor/animated-gif/raw/master/example/streamlit-app-starter-kit-screencast.mov)

---
Made with ❤️ by Chanin Nantasenamat ([Data Professor](https://youtube.com/dataprofessor))
''')

## Display gif generation parameters once file has been uploaded ##
if uploaded_file is not None:
  ## Save to temp file ##
  tfile = tempfile.NamedTemporaryFile(delete=False) 
  tfile.write(uploaded_file.read())
  
  ## Open file ##
  clip = VideoFileClip(tfile.name)
    
  st.session_state.clip_duration = clip.duration
  
  ## Input widgets ##
  st.sidebar.header('Input parameters')
  selected_resolution_scaling = st.sidebar.slider('Scaling of video resolution', 0.0, 1.0, 0.5 )
  selected_speedx = st.sidebar.slider('Playback speed', 0.1, 10.0, 5.0)
  selected_export_range = st.sidebar.slider('Duration range to export', 0, int(st.session_state.clip_duration), (0, int(st.session_state.clip_duration) ))
    
  ## Resizing of video ##
  clip = clip.resize(selected_resolution_scaling)
     
  st.session_state.clip_width = clip.w
  st.session_state.clip_height = clip.h
  st.session_state.clip_duration = clip.duration
  st.session_state.clip_total_frames = clip.duration * clip.fps
  st.session_state.clip_fps = st.sidebar.slider('FPS', 10, 60, 20)
    
  ## Display output ##
  st.subheader('Metrics')
  col1, col2, col3, col4, col5 = st.columns(5)
  col1.metric('Width', st.session_state.clip_width, 'pixels')
  col2.metric('Height', st.session_state.clip_height, 'pixels')
  col3.metric('Duration', st.session_state.clip_duration, 'seconds')
  col4.metric('FPS', st.session_state.clip_fps, '')
  col5.metric('Total Frames', st.session_state.clip_total_frames, 'frames')

  # Extract video frame as a display image
  st.subheader('Preview')

  with st.expander('Show image'):
    selected_frame = st.slider('Preview a time frame (s)', 0, int(st.session_state.clip_duration), int(np.median(st.session_state.clip_duration)) )
    clip.save_frame('frame.gif', t=selected_frame)
    frame_image = Image.open('frame.gif')
    st.image(frame_image)

  ## Print image parameters ##
  st.subheader('Image parameters')
  with st.expander('Show image parameters'):
    st.write(f'File name: `{uploaded_file.name}`')
    st.write('Image size:', frame_image.size)
    st.write('Video resolution scaling', selected_resolution_scaling)
    st.write('Speed playback:', selected_speedx)
    st.write('Export duration:', selected_export_range)
    st.write('Frames per second (FPS):', st.session_state.clip_fps)
    
  ## Export animated GIF ##
  st.subheader('Generate GIF')
  generate_gif = st.button('Generate Animated GIF')
  
  if generate_gif:
    clip = clip.subclip(selected_export_range[0], selected_export_range[1]).speedx(selected_speedx)
    
    frames = []
    for frame in clip.iter_frames():
        frames.append(np.array(frame))
    
    image_list = []

    for frame in frames:
        im = Image.fromarray(frame)
        image_list.append(im)

    image_list[0].save('export.gif', format = 'GIF', save_all = True, loop = 0, append_images = image_list)
    
    #clip.write_gif('export.gif', fps=st.session_state.clip_fps)
    
    ## Download ##
    st.subheader('Download')
    
    #video_file = open('export.gif', 'rb')
    #video_bytes = video_file.read()
    #st.video(video_bytes)
    
    file_ = open('export.gif', 'rb')
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
        unsafe_allow_html=True,
    )
    
    fsize = round(os.path.getsize('export.gif')/(1024*1024), 1)
    st.info(f'File size of generated GIF: {fsize} MB', icon='💾')
    
    fname = uploaded_file.name.split('.')[0]
    with open('export.gif', 'rb') as file:
      btn = st.download_button(
            label='Download image',
            data=file,
            file_name=f'{fname}_scaling-{selected_resolution_scaling}_fps-{st.session_state.clip_fps}_speed-{selected_speedx}_duration-{selected_export_range[0]}-{selected_export_range[1]}.gif',
            mime='image/gif'
          )

## Default page ##
else:
  st.warning('👈 Upload a video file')
