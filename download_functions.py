import instaloader
import requests
import streamlit as st
from PIL import Image
from io import BytesIO
import re

my_username = "hydenjkyl"
L = instaloader.Instaloader()
L.context.log("Login...")
L.load_session_from_file(my_username, "instaloader.session")
# Initialization

def download_all_posts(username):
    try:
        loader = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(loader.context, username)
        image_urls = [post.url for post in profile.get_posts()]
        print(f"All posts from {username} URLs obtained successfully.")
        return image_urls
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Profile with username '{username}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def download_story(username):
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        stories = L.get_stories([profile.userid])
        story_links = []
        for story in stories:
            for item in story.get_items():
                url = {
                    "url": item.video_url if item.video_url is not None else item.url,
                    "is_video": item.is_video
                }
                story_links.append(url)
        print(story_links)
        print(f"Stories from {username} URLs obtained successfully.")
        return story_links
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Profile with username '{username}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def download_post(post_link):
    match = re.search(r'instagram\.com/p/([^/]+)/', post_link)
    if match:
        mediaid = match.group(1)
        try:
            loader = instaloader.Instaloader()
            post = instaloader.Post.from_shortcode(loader.context, mediaid)
            full_image_url = post.graph_target.shortcode_media.image_versions2.candidates[0].url
            image_urls = [post.url]
            print(image_urls)
            print(f"Post from {post.owner_username} URL obtained successfully.")
            return image_urls
        except instaloader.exceptions.InstaloaderException:
            print("Invalid post link or post not found.")
            return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None
    else:
        print("Invalid Instagram post link format.")
        return None

def download_all_post_slides(post_link, quality="low"):
    match = re.search(r'instagram\.com/p/([^/]+)/', post_link)
    if match:
        mediaid = match.group(1)
        try:
            loader = instaloader.Instaloader()
            post = instaloader.Post.from_shortcode(loader.context, mediaid)
            pictures = [node.display_url + f"?quality={quality}" for node in post.get_sidecar_nodes()]
            print(f"All slides from {post.owner_username} URL obtained successfully.")
            return pictures, post.caption
        except instaloader.exceptions.InstaloaderException:
            print("Invalid post link or post not found.")
            return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None
    else:
        print("Invalid Instagram post link format.")
        return None
