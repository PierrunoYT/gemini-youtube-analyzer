import os
import io
import requests
from PIL import Image
import google.generativeai as genai
from googleapiclient.discovery import build

# Get API keys from environment variables
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Check if API keys are available
if not YOUTUBE_API_KEY or not GEMINI_API_KEY:
    raise ValueError("API keys not found. Please set YOUTUBE_API_KEY and GEMINI_API_KEY as environment variables.")

# YouTube API-Client erstellen
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Gemini-Modell konfigurieren
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

def get_video_details(video_id):
    request = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    )
    response = request.execute()
    
    if 'items' in response:
        video = response['items'][0]
        title = video['snippet']['title']
        description = video['snippet']['description']
        view_count = video['statistics']['viewCount']
        like_count = video['statistics'].get('likeCount', 'N/A')
        thumbnail_url = video['snippet']['thumbnails']['high']['url']
        
        return {
            'title': title,
            'description': description,
            'view_count': view_count,
            'like_count': like_count,
            'thumbnail_url': thumbnail_url
        }
    else:
        return None

def get_thumbnail_image(url):
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

def analyze_video(video_details, thumbnail_image):
    prompt = [
        thumbnail_image,
        f"""
        Analyze this video thumbnail and provide a summary based on the following information:
        
        Title: {video_details['title']}
        Description: {video_details['description']}
        Views: {video_details['view_count']}
        Likes: {video_details['like_count']}
        
        Please include:
        1. An interpretation of the thumbnail image
        2. A hypothesis about the video content based on the title, description, and thumbnail
        3. Key points or main topics that might be discussed in the video
        4. An analysis of the video's popularity based on views and likes
        5. Any interesting observations or insights
        """
    ]
    
    response = model.generate_content(prompt)
    return response.text

def main():
    video_id = input("Geben Sie die YouTube-Video-ID ein: ")
    video_details = get_video_details(video_id)
    
    if video_details:
        print("Video gefunden. Hole Thumbnail...")
        thumbnail_image = get_thumbnail_image(video_details['thumbnail_url'])
        
        print("Analysiere Video...")
        analysis = analyze_video(video_details, thumbnail_image)
        
        print("\nZusammenfassung und Analyse:")
        print(analysis)
    else:
        print("Video nicht gefunden oder Fehler beim Abrufen der Details.")

if __name__ == "__main__":
    main()
