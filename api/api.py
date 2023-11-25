from flask import Flask, request, jsonify
import instaloader
from PIL import Image
from io import BytesIO
import re
from repository import download_all_post_slides, download_all_posts, download_story, download_post, download_reels

app = Flask(__name__)
L = instaloader.Instaloader()

@app.route('/download_all_posts', methods=['GET'])
def download_all_posts_api():
    username = request.args.get('username')
    if username:
        result = download_all_posts(username)
        if result:
            return jsonify(result)
    return jsonify({"error": "Invalid request or username not provided"})

@app.route('/download_story', methods=['GET'])
def download_story_api():
    username = request.args.get('username')
    if username:
        result = download_story(username)
        if result:
            return jsonify(result)
    return jsonify({"error": "Invalid request or username not provided"})

@app.route('/download_post', methods=['GET'])
def download_post_api():
    post_link = request.args.get('post_link')
    if post_link:
        result = download_post(post_link)
        if result:
            return jsonify(result)
    return jsonify({"error": "Invalid request or post link not provided"})

@app.route('/download_all_post_slides', methods=['GET'])
def download_all_post_slides_api():
    post_link = request.args.get('post_link')
    if post_link:
        print(post_link)
        result = download_all_post_slides(post_link)
        if result:
            return jsonify(result)
    return jsonify({"error": "Invalid request or post link not provided"})

@app.route('/download_reels', methods=['GET'])
def download_reels_api():
    post_link = request.args.get('post_link')
    if post_link:
        result = download_reels(post_link)
        if result:
            return jsonify(result)
    return jsonify({"error": "Invalid request or post link not provided"})

if __name__ == '__main__':
    app.run(debug=True)