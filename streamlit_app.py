import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import os
import time
from dotenv import load_dotenv

load_dotenv()

def run_app():
    title = "Instagram Downloader"
    title_el = st.empty()
    hide_st_style = """
    <style>
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    # header {visibility: hidden;}
    </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    # Menu for selecting download type
    download_type = st.sidebar.selectbox("Select Download Type", ["Post & Reels", "Story - Currently not available", "All Posts"])
    button_submit_text = "Download"
    # Input field for Instagram link or username
    title += " " + download_type
    input_field = st.empty()
    if download_type in ["All Posts", "Story - Currently not available"]:
        if download_type == "Story - Currently not available":
            title = "Not Available"
            username = input_field.text_input("Enter Instagram username:", value="", disabled=True)
        else:
            username = input_field.text_input("Enter Instagram username:", value="", placeholder="Username")
    else:
        link = input_field.text_input("Enter Instagram link:", value="", placeholder="https://www.instagram.com/p/example")

    title_el.title(title)

    submit_button = st.button("Run", use_container_width=False)

    if submit_button:
        try:
            progress_bar = st.empty()
            progress_bar.progress(0, text="Please wait(0%)...")

            dividerEl = st.empty()
            result = None
            
            base_url = os.getenv('API_URL')  # Update with your Flask API URL

            if download_type == "All Posts" and username:
                endpoint = "/download_all_posts"
                params = {"username": username}
                result = requests.get(f"{base_url}{endpoint}", params=params).json()

            elif download_type in "Story" and username:
                endpoint = "/download_story"
                params = {"username": username}
                result = requests.get(f"{base_url}{endpoint}", params=params).json()

            elif download_type == "Post & Reels" and link.startswith("https://www.instagram.com/"):
                if link.startswith("https://www.instagram.com/reel/"):
                    endpoint = "/download_reels"
                    params = {"post_link": link}
                elif link.startswith("https://www.instagram.com/p/"):
                    endpoint = "/download_all_post_slides"
                    params = {"post_link": link}
                    
                result = requests.get(f"{base_url}{endpoint}", params=params).json()

            if result is not None:
                dividerEl.divider()
                total_progress = 100
                increment = total_progress // len(result)
                current_progress = 0
                if len(result) == 2:
                    for url in result[0]:
                        if url["is_video"]:
                            st.video(BytesIO(requests.get(url["url"]).content))
                        else:
                            image = Image.open(BytesIO(requests.get(url["url"]).content))
                            st.image(image, use_column_width=True)
                        current_progress += increment
                        progress_bar.progress(current_progress, text=f"Please wait({current_progress}%)...")
                    st.text(result[1])
                else:
                    for url in result:
                        if url["is_video"]:
                            st.video(BytesIO(requests.get(url["url"]).content))
                        else:
                            image = Image.open(BytesIO(requests.get(url["url"]).content))
                            st.image(image, use_column_width=True)
                        current_progress += increment
                        progress_bar.progress(current_progress, text=f"Please wait({current_progress}%)...")
                progress_bar.progress(100, text=f"Finished({100}%).")
                st.success("Download successful!")
            else:
                progress_bar.progress(0, text="error occurred while downloading")
                st.error("Download failed. Please check the link or username.")
        except requests.exceptions.RequestException as e:
            st.error(f"Request error: {e}")

