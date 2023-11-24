import instaloader
import re

# my_username = "hydenjkyl"
L = instaloader.Instaloader()
# LWL = instaloader.Instaloader()
# L.load_session_from_file(my_username, "instaloader.session")

# if "ins_session" not in st.session_state:
#     st.session_state.ins_session = L
# Initialization

def download_all_posts(username, quality="low"):
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        media_url = []
        for post in profile.get_posts():
            for node in post.get_sidecar_nodes():
                url = {
                    "url": node.video_url if node.video_url is not None else node.display_url,
                    "is_video": node.is_video
                }
                media_url.append(url)
        print(f"All posts from {username} URLs obtained successfully.")
        return media_url
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Profile with username '{username}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def download_story(username):
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        stories = instaloader.Instaloader().get_stories([profile.userid])
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
            post = instaloader.Post.from_shortcode(L.context, mediaid)
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
            post = instaloader.Post.from_shortcode(L.context, mediaid)
            media_url = []
            for node in post.get_sidecar_nodes():
                url = {
                    "url": node.video_url if node.video_url is not None else node.display_url,
                    "is_video": node.is_video
                }
                media_url.append(url)
            print(f"All slides from {post.owner_username} URL obtained successfully.")
            return media_url, post.caption
        except instaloader.exceptions.InstaloaderException:
            print("Invalid post link or post not found.")
            return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None
    else:
        print("Invalid Instagram post link format.")
        return None