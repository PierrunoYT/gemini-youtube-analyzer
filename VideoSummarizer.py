import os
import io
import time
import requests
from PIL import Image
import google.generativeai as genai
from yt_dlp import YoutubeDL

# Get API key from environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Check if API key is available
if not GEMINI_API_KEY:
    raise ValueError("API key not found. Please set GEMINI_API_KEY as an environment variable.")

# Configure Gemini model
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

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

def main():
    video_url = input("Enter the YouTube video URL: ")
    try:
        ydl_opts = {'quiet': True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
        video_id = info['id']
        video_details = {
            'title': info['title'],
            'description': info['description'],
            'view_count': info['view_count'],
            'like_count': info.get('like_count', 'N/A'),
            'thumbnail_url': info['thumbnail']
        }
        
        print("Video found. Fetching thumbnail...")
        thumbnail_data = get_thumbnail_image(video_details['thumbnail_url'])
        thumbnail_path = f"{video_id}_thumbnail.png"
        with open(thumbnail_path, 'wb') as f:
            f.write(thumbnail_data)
        
        print("Downloading video...")
        output_path = f"{video_id}.mp4"
        download_video(video_url, output_path)
        
        print("Analyzing video...")
        analysis = analyze_video(video_details, thumbnail_path, output_path)
        
        print("\nSummary and Analysis:")
        print(analysis)

        # Cleanup
        os.remove(output_path)
        os.remove(thumbnail_path)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
