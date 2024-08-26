from flask import Flask, jsonify, request,Response
from googleapiclient.discovery import build
import json
import time
app = Flask(__name__)

# YouTube Data API configuration
API_KEY = "AIzaSyBlGwIATxgUZNgEh_P7lwUIVszl6TaXYKk"
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(query):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

    # Call the search.list method to retrieve search results excluding live videos
    search_response = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=6,  # Number of search results to return
        type='video',  # Ensure we are only getting video results
        eventType='completed'  # Ensure we are only getting non-live video results
    ).execute()

    thumbnails = []
    for item in search_response.get('items', []):
        video_title = item['snippet']['title']
        thumbnail_url = item['snippet']['thumbnails']['high']['url']
        video_id = item['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        thumbnails.append({
            'title': video_title,
            'thumbnail_url': thumbnail_url,
            'video_url': video_url
        })

    return thumbnails

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400

    thumbnails = youtube_search(query)
    return jsonify({"thumbnails": thumbnails})
def generate_data():
    while True:
        value=input("a")
        yield f"{json.dumps(value)}\n\n"


@app.route('/stream')
def stream():
    return Response(generate_data(), mimetype='text/event-stream')
   
if __name__ == '__main__':
    app.run(debug=True)
