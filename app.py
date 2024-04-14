import os
import streamlit as str
from dotenv import load_dotenv
import google.generativeai as genai

from views.vision_image import vision_image_page
from views.vision_text import vision_text_page


load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")


def configure_genai():
    str.session_state.app_key = google_api_key

    try:
        genai.configure(api_key=str.session_state.app_key)
    except AttributeError as e:
        str.warning(e)


def main():
    configure_genai()
    # Set up the page configuration
    page_icon_path = "img/logo.png"
    if os.path.exists(page_icon_path):
        str.set_page_config(
            page_title="Doctor Lytical Agent",
            page_icon=page_icon_path,
        )

    # Define the pages dictionary
    pages = {
        "Doctor Lytical": vision_text_page,
        "Doctor Lytical Vision": vision_image_page
    }

    # Create the sidebar navigation

    str.sidebar.image("img/doc_robot.jpeg")
    str.sidebar.write("---")

    selection = str.sidebar.radio("Switch Screens", list(pages.keys()))
    # Call the function corresponding to the selected page
    pages[selection]()

    if str.sidebar.button("Clear Chat Window", use_container_width=True, type="primary"):
        str.rerun()

    str.sidebar.write("---")
    str.sidebar.image("img/doc_think.jpeg")
    str.sidebar.write("Doctor Lytical was created by @CodeLytical")


if __name__ == "__main__":
    main()
