import yt_dlp
import cv2
import numpy as np
from groq import Groq
from PIL import Image
import io
import base64

def extract_frames(video_url, num_frames=5):
    # Download video info
    ydl_opts = {'outtmpl': 'video.%(ext)s'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        duration = info['duration']
        ydl.download([video_url])

    # Extract frames
    video = cv2.VideoCapture('video.mp4')
    frames = []
    for i in range(num_frames):
        video.set(cv2.CAP_PROP_POS_MSEC, (duration * 1000 * i) / num_frames)
        success, image = video.read()
        if success:
            frames.append(image)
    video.release()
    return frames

def frames_to_base64(frames):
    encoded_frames = []
    for frame in frames:
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        encoded_frames.append(base64.b64encode(buffered.getvalue()).decode('utf-8'))
    return encoded_frames

def summarize_video(video_url):
    frames = extract_frames(video_url)
    encoded_frames = frames_to_base64(frames)
    
    client = Groq()
    
    prompt = f"""Analyze the following video frames and provide a concise summary of the video content:

    {' '.join([f'[Frame {i+1}: data:image/jpeg;base64,{frame}]' for i, frame in enumerate(encoded_frames)])}

    Based on these key frames, summarize the main points and content of the video."""

    completion = client.chat.completions.create(
        model="llama-3.2-90b-text-preview",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    summary = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content or ""
        summary += content
        print(content, end="", flush=True)
    
    return summary

# Example usage
video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
summary = summarize_video(video_url)
print("\n\nFinal Summary:", summary)
