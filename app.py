from tensorflow.keras.models import model_from_json
import cv2
import numpy as np
from PIL import Image
import streamlit as st

#directory="C:/Users/USER/Desktop/deploy_fr/"
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
label_map = ['Anger', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']


# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from Kaggle server")

def about():
	st.write(
		'''
		**Haar Cascade** is an object detection algorithm.
		It can be used to detect objects in images or videos. 

		The algorithm has four stages:

			1. Haar Feature Selection 
			2. Creating  Integral Images
			3. Adaboost Training
			4. Cascading Classifiers



View Dev-k web :point_right: http://dev-k-copyright.herokuapp.com/
		''')


# Defining a function that will do the detections
def detect(color,gray):
    faces = face_cascade.detectMultiScale(image=gray, scaleFactor=1.3, minNeighbors=5)
    for (x, y, w, h) in faces:
        cv2.rectangle(color, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = color[y:y+h, x:x+w]
      
    return color,faces,roi_gray

def prediction(roi_gray):
    roi=cv2.resize(roi_gray,(48,48))
    prediction = loaded_model.predict(roi[np.newaxis, :, :, np.newaxis])
    # Custom Symbols to print with text of emotion.
    # Symbols = {"Happy": ":)", "Sad": ":}", "Surprise": "!!","Angry": "?", "Disgust": "#", "Neutral": ".", "Fear": "~"}

    # Defining the Parameters for putting Text on Image
    #Text = str(prediction) + Symbols[str(prediction)]
    return label_map[np.argmax(prediction[0])]


def main():
    st.set_page_config(layout="wide")
    st.markdown("<h1 style='text-align: center; color: white;'>Detection And Facial Expression recognition</h1>", unsafe_allow_html=True)
    banner=Image.open("img3.jpg")
    st.image(banner,use_column_width=True)
    with st.beta_expander("Configuration Option"):

        st.write("**Haarcascade classifier** for face detection ")
        st.write("**CNN** The model is the implementation of the paper Convolutional Neural Networks for Facial Expression Recognition")
        st.write("**Input shape(48,48,1)**The data consists of 48x48 pixel grayscale images of faces")
        st.write("**Expressions** (0=Angry, 1=Disgust, 2=Fear, 3=Happy, 4=Sad, 5=Surprise, 6=Neutral).")

    activities = ["Home", "About"]
    choice = st.sidebar.selectbox("Pick something fun", activities)
    sidebar_image=Image.open('face-detection.jpg')
    st.sidebar.image(sidebar_image,use_column_width=True)
    st.sidebar.info('?? 2021 Copyright: Dev-k')
    if choice == "Home":
        st.write("Go to the About section from the sidebar to learn more about it.")
        image_file = st.file_uploader("Upload image", type=['jpeg', 'png', 'jpg', 'webp'])

        if image_file is not None:
            img = Image.open(image_file)
            #if st.button("Process"):
            color_img=np.array(img.convert('RGB'))
            gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
            result_img, result_faces ,roi_gray= detect(color_img,gray_img)
            roi=cv2.resize(roi_gray,(48,48))
            prediction = loaded_model.predict(roi[np.newaxis, :, :, np.newaxis])
            Text=label_map[np.argmax(prediction[0])]
            #st.image(result_img, use_column_width = True)
            col1, col2 = st.beta_columns(2)
            col1.header("Original")
            col1.image(img, use_column_width=True)
            col2.header("Detected Expression")
            col2.image(result_img, use_column_width=True)
            st.success("Expression: {} ".format(Text))
    elif choice == "About":
    	about()

if __name__ == "__main__":
    main()

