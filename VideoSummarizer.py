import os
import io
import time
import requests
from PIL import Image
import google.generativeai as genai
from googleapiclient.discovery import build
from yt_dlp import YoutubeDL

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

def download_video(video_url, output_path):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': output_path,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

def analyze_video(video_details, thumbnail_path, video_file_path):
    try:
        # Upload thumbnail image
        thumbnail_file = genai.upload_file(thumbnail_path)

        # Upload video file
        video_file = genai.upload_file(video_file_path)

        # Wait for video processing
        while video_file.state.name == "PROCESSING":
            print("Processing video...")
            time.sleep(5)
            video_file = genai.get_file(video_file.name)
    except FileNotFoundError as e:
        print(f"Error: File not found. Please check if the file exists: {e.filename}")
        return "Unable to analyze video due to missing file."
    except Exception as e:
        print(f"An error occurred while processing the files: {str(e)}")
        return "Unable to analyze video due to an unexpected error."

    prompt = f"""
    Analyze this video and provide a summary based on the following information:
    
    Title: {video_details['title']}
    Description: {video_details['description']}
    Views: {video_details['view_count']}
    Likes: {video_details['like_count']}
    
    Please include:
    1. An interpretation of the thumbnail image
    2. A hypothesis about the video content based on the title, description, and thumbnail
    3. Key points or main topics discussed in the video
    4. An analysis of the video's popularity based on views and likes
    5. Any interesting observations or insights from the video content
    """

    response = model.generate_content([thumbnail_file, video_file, prompt])
    return response.text

def extract_video_id(url):
    # Handle various YouTube URL formats
    if 'youtu.be' in url:
        return url.split('/')[-1]
    elif 'youtube.com/watch' in url:
        return url.split('v=')[-1].split('&')[0]
    elif 'youtube.com/shorts' in url:
        return url.split('/')[-1]
    elif url.startswith('v='):
        return url.split('v=')[-1].split('&')[0]
    else:
        raise ValueError("Ungültige YouTube-URL")

def main():
    video_url = input("Geben Sie die YouTube-Video-URL ein: ")
    try:
        video_id = extract_video_id(video_url)
        print(f"Extrahierte Video-ID: {video_id}")
        video_details = get_video_details(video_id)
        
        if video_details:
            print("Video gefunden. Hole Thumbnail...")
            thumbnail_data = get_thumbnail_image(video_details['thumbnail_url'])
            thumbnail_path = f"{video_id}_thumbnail.png"
            with open(thumbnail_path, 'wb') as f:
                f.write(thumbnail_data)
            
            print("Lade Video herunter...")
            output_path = f"{video_id}.mp4"
            download_video(f"https://www.youtube.com/watch?v={video_id}", output_path)
            
            print("Analysiere Video...")
            analysis = analyze_video(video_details, thumbnail_path, output_path)
            
            print("\nZusammenfassung und Analyse:")
            print(analysis)

            # Cleanup
            os.remove(output_path)
            os.remove(thumbnail_path)
        else:
            print("Video nicht gefunden oder Fehler beim Abrufen der Details.")
    except ValueError as e:
        print(f"Fehler beim Extrahieren der Video-ID: {str(e)}")
        print(f"Eingegebene URL: {video_url}")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {str(e)}")

if __name__ == "__main__":
    main()
