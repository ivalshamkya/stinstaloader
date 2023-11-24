import streamlit as st
from PIL import Image
from io import BytesIO
import requests
import os
from dotenv import load_dotenv

load_dotenv()

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
    download_type = st.sidebar.selectbox("Select Download Type", ["Post & Reels", "Story", "All Posts"])

    # Input field for Instagram link or username
    if download_type in ["All Posts", "Story"]:
        username = st.text_input("Enter Instagram username:")
    else:
        link = st.text_input("Enter Instagram link:")

    if st.button("Download"):
        try:
            result = None
            base_url =  os.getenv('API_URL') # Update with your Flask API URL

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
                if len(result) == 2:
                    for url in result[0]:
                        print("aa")
                        if url["is_video"]:
                            st.video(BytesIO(requests.get(url["url"]).content))
                        else:
                            image = Image.open(BytesIO(requests.get(url["url"]).content))
                            st.image(image, use_column_width=True)
                    st.text(result[1])
                else:
                    print(result)
                    for url in result:
                        print(url)
                        if url["is_video"]:
                            st.video(BytesIO(requests.get(url["url"]).content))
                        else:
                            image = Image.open(BytesIO(requests.get(url["url"]).content))
                            st.image(image, use_column_width=True)
                st.success("Download successful!")
            else:
                st.error("Download failed. Please check the link or username.")
        except requests.exceptions.RequestException as e:
            st.error(f"Request error: {e}")
