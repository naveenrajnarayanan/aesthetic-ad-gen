# Link for Privous Video: https://www.youtube.com/watch?v=rtHcsPvE7Uw
# write streamlit application which will remove background from image and replace it with another image
# streamlit.io
# pip install streamlit
# pip install rembg

# run application using command: streamlit run app.py

import streamlit as st
from PIL import Image
import os
import requests
from io import BytesIO
import urllib.request

# set full screen
st.set_page_config(layout="wide")

st.title("MARBLE AI AD ASSIGNMENT using ML and AI")
st.write("This is a simple image background removal and replacement web app using ML and AI")

os.makedirs('original', exist_ok=True)
os.makedirs('masked', exist_ok=True)

use_local_image = st.checkbox("Use Local Image", value=False)
cols = st.columns(2)
if use_local_image:
    subject_file = cols[0].file_uploader("Choose Subject Image...", type=["jpg", 'png', 'jpeg'], key='subject')
    background_file = cols[1].file_uploader("Choose Background Image...", type=["jpg", 'png', 'jpeg'], key='background')

    subject_name = subject_file.name
    subject_file = os.path.join('original', subject_name)
    
    background_name = background_file.name
    background_file = os.path.join('original', background_name)

else:
    subject_url = cols[0].text_input("Enter Subject Image URL", "https://www.barristerandmann.com/cdn/shop/products/SevilleShavingSoap.jpg")
    background_url = cols[1].text_input("Enter Background URL", "https://t3.ftcdn.net/jpg/04/60/44/08/360_F_460440876_a8lkfz8UHz64eDPFzmSJJZ55UQBNiC0a.jpg")

    subject_name = subject_url.split('/')[-1]
    background_name = background_url.split('/')[-1]

    subject_file = os.path.join('original', subject_name)
    background_file = os.path.join('original', background_name)

    #subject_img = Image.open(BytesIO(requests.get(subject_url).content))
    #subject_img.save(subject_file, format='jpeg')
    urllib.request.urlretrieve(subject_url, subject_file) # Save the image

    #background_img = Image.open(BytesIO(requests.get(background_url).content))
    #background_img.save(background_file, format='jpeg')
    urllib.request.urlretrieve(background_url, background_file) # Save the image

subject_img = Image.open(subject_file)
cols[0].image(subject_img, caption='Subject Image', use_column_width=True)

background_img = Image.open(background_file)
cols[1].image(background_img, caption='Background Image', use_column_width=True)

from rembg import remove

st.title("AESTHETIC PLEASING AD OUTPUT")
threshold = st.slider("Background Threshold", 0, 255, value=50, step=5)

cols = st.columns(2)

output_file = "masked/" + subject_name
f = open(output_file, 'wb')
subject_img = open(subject_file, 'rb').read()
subject = remove(subject_img, alpha_matting=True, alpha_matting_foreground_threshold=threshold)
f.write(subject)
f.close()

cols[0].image(output_file, caption="Subject Image without Background. Use Slider to Control Background Removal", use_column_width=True)


background_img = Image.open(background_file)
subject_img = Image.open(output_file)

background_img = background_img.resize(subject_img.size)

background_img.paste(subject_img, (0,0), subject_img)
background_img.save('masked/background.jpg', format='jpeg')

cols[1].image('masked/background.jpg', caption='Merged Image', use_column_width=True)

