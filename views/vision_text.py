import time
import random
import streamlit as st
from utils import SAFETY_SETTINGS, MODEL
from prompts import diagnosis_text_prompt
import google.generativeai as genai


def vision_text_page():
    st.title("🩹💊 Doctor Lytical 👨🏼‍⚕️")
    st.caption(
        "Unveiling the Symphony of Healing with Comprehensive Drug Knowledge, Side Effect Insights, and Precision Dosage Guidance.")

    model = genai.GenerativeModel(MODEL)
    chat = model.start_chat()

    for message in chat.history:
        role = "assistant" if message.role == "model" else message.role
        with st.chat_message(role):
            st.markdown(message.parts[0].text)

    if prompt := st.chat_input(""):
        prompt = prompt.replace('\n', '  \n')
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            st.spinner("Lytical diagnosing...")
            try:
                full_response = ""
                for chunk in chat.send_message(diagnosis_text_prompt(prompt), stream=True,
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
                message_placeholder.markdown(full_response)
            except genai.types.generation_types.BlockedPromptException as e:
                st.exception(e)
            except Exception as e:
                st.exception(e)
