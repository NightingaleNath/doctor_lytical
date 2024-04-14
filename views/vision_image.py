import time
import random
import streamlit as st
from PIL import Image
from utils import SAFETY_SETTINGS, MODEL_VISION
from prompts import diagnosis_image_prompt
import google.generativeai as genai

model = genai.GenerativeModel(MODEL_VISION)


def show_message(prompt, image, loading_str, initial_analysis=False):
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown(loading_str)
        full_response = ""
        try:
            for chunk in model.generate_content([diagnosis_image_prompt(prompt, initial_analysis), image], stream=True,
                                                safety_settings=SAFETY_SETTINGS):
                word_count = 0
                random_int = random.randint(5, 10)
                for word in chunk.text:
                    full_response += word
                    word_count += 1
                    if word_count == random_int:
                        time.sleep(0.05)
                        message_placeholder.markdown(full_response + "_")
                        word_count = 0
                        random_int = random.randint(5, 10)
        except genai.types.generation_types.BlockedPromptException as e:
            st.exception(e)
        except Exception as e:
            st.exception(e)
        message_placeholder.markdown(full_response)
        st.session_state.history_pic.append({"role": "assistant", "text": full_response})


def clear_state():
    st.session_state.history_pic = []
    st.session_state.initial_analysis_done = False


def vision_image_page():
    st.title("🩹💊 Doctor Lytical 👨🏼‍⚕️")
    st.caption('Transforming Healthcare with Visionary Precision ')

    if "history_pic" not in st.session_state:
        st.session_state.history_pic = []
    if "initial_analysis_done" not in st.session_state:
        st.session_state.initial_analysis_done = False

    image = None
    if "app_key" in st.session_state:
        uploaded_file = st.file_uploader("choose a pic...", type=["jpg", "png", "jpeg", "gif"],
                                         label_visibility='collapsed', on_change=clear_state)
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            width, height = image.size
            resized_img = image.resize((128, int(height / (width / 128))), Image.LANCZOS)
            st.image(image)

            if image and not st.session_state.initial_analysis_done:
                show_message("", resized_img, "Lytical diagnosing...", initial_analysis=True)
                st.session_state.initial_analysis_done = True

    if len(st.session_state.history_pic) > 0:
        for item in st.session_state.history_pic:
            with st.chat_message(item["role"]):
                st.markdown(item["text"])

    if "app_key" in st.session_state:
        if prompt := st.chat_input("desc this picture"):
            if image is None:
                st.warning("Please upload an image first", icon="⚠️")
            else:
                prompt = prompt.replace('\n', '  \n')
                with st.chat_message("user"):
                    st.markdown(prompt)
                    st.session_state.history_pic.append({"role": "user", "text": prompt})

                show_message(prompt, resized_img, "Lytical thinking...")

