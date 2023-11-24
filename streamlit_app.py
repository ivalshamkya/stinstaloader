import streamlit as st
import instaloader
from download_functions import download_all_posts, download_story, download_all_post_slides, login
from PIL import Image
from io import BytesIO
import requests

def run_app():
    st.title("Instagram Downloader")

    hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    # header {visibility: hidden;}
    </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    # Menu for selecting download type
    download_type = st.sidebar.selectbox("Select Download Type", ["Post Slides", "Story", "All Posts"])

    # Input field for Instagram link or username
    if download_type in ["All Posts", "Story"]:
        username = st.text_input("Enter Instagram username:")
    else:
        link = st.text_input("Enter Instagram link:")

    if st.button("Download"):
        result = None
        retry_login = False
        try:
            if download_type == "All Posts" and username:
                with st.spinner("Downloading..."):
                    result = download_all_posts(username)
            elif download_type == "Story" and username:
                with st.spinner("Downloading..."):
                    result = download_story(username)
            elif download_type == "Post Slides" and link.startswith("https://www.instagram.com/"):
                with st.spinner("Downloading..."):
                    result = download_all_post_slides(link)

        except instaloader.exceptions.QueryReturnedNotFoundException:
            # Handle the case where the session is not valid
            retry_login = True

        if retry_login:
            st.warning("Session expired. Logging in again...")
            login()
            # Retry the download after logging in again

        if result is not None:
            if len(result) == 2:
                for url in result[0]:
                    if download_type == "Story" and username:
                        st.video(BytesIO(requests.get(url).content))
                        print(url)
                    else:
                        image = Image.open(BytesIO(requests.get(url).content))
                        st.image(image, use_column_width=True)
                st.text(result[1])
            else:
                for url in result:
                    if download_type == "Story" and username:
                        if url["is_video"] == True:
                            st.video(url["url"])
                        else:
                            image = Image.open(BytesIO(requests.get(url["url"]).content))
                            st.image(image, use_column_width=True)
                    else:
                        image = Image.open(BytesIO(requests.get(url).content))
                        st.image(image, use_column_width=True)
            st.success("Download successful!")
        else:
            st.error("Download failed. Please check the link or username.")
