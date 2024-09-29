import yt_dlp
import cv2
import numpy as np
import requests
from PIL import Image
import io
import base64
import os
from datetime import datetime
import logging
import time
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def exponential_backoff(attempt, max_attempts=5, base_delay=1, max_delay=60):
    if attempt >= max_attempts:
        raise Exception("Max retry attempts reached")
    delay = min(base_delay * (2 ** attempt) + random.uniform(0, 1), max_delay)
    time.sleep(delay)

class VideoSummarizer:
    def __init__(self, video_url, num_frames=5):
        self.video_url = video_url
        self.num_frames = num_frames
        self.api_key = os.environ.get('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is not set. Use 'setx OPENROUTER_API_KEY your_api_key_here' to set it.")
        self.site_url = os.environ.get('YOUR_SITE_URL', 'http://localhost')
        self.site_name = os.environ.get('YOUR_SITE_NAME', 'VideoSummarizer')

    def extract_frames(self):
        ydl_opts = {'outtmpl': 'video.%(ext)s'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.video_url, download=True)
            duration = info['duration']
            filename = ydl.prepare_filename(info)
            logger.info(f"Downloaded video: {filename}")

        video = cv2.VideoCapture(filename)
        if not video.isOpened():
            raise ValueError(f"Unable to open video file: {filename}")

        frames = []
        for i in range(self.num_frames):
            video.set(cv2.CAP_PROP_POS_MSEC, (duration * 1000 * i) / self.num_frames)
            success, image = video.read()
            if success:
                frames.append(image)
            else:
                logger.warning(f"Failed to read frame {i+1}")
        video.release()

        if not frames:
            raise ValueError("No frames were extracted from the video")

        logger.info(f"Extracted {len(frames)} frames from the video")
        return frames

    @staticmethod
    def frames_to_base64(frames):
        encoded_frames = []
        for frame in frames:
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG")
            encoded_frames.append(base64.b64encode(buffered.getvalue()).decode('utf-8'))
        return encoded_frames

    def summarize(self):
        frames = self.extract_frames()
        encoded_frames = self.frames_to_base64(frames)
        
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analyze the following video frames and provide a concise summary of the video content:"
                    }
                ]
            }
        ]

        for i, frame in enumerate(encoded_frames):
            messages[0]["content"].append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{frame}"
                }
            })

        messages[0]["content"].append({
            "type": "text",
            "text": "Based on these key frames, summarize the main points and content of the video."
        })

        for attempt in range(5):
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "HTTP-Referer": self.site_url,
                        "X-Title": self.site_name,
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "google/gemini-pro-1.5",
                        "messages": messages
                    }
                )
                response.raise_for_status()
                summary = response.json()['choices'][0]['message']['content']
                print(summary)
                return summary
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if "rate_limit_exceeded" in str(e):
                    exponential_backoff(attempt)
                else:
                    raise e
        
        raise Exception("Failed to summarize after multiple attempts")

    def save_summary_to_markdown(self, summary):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"video_summary_{timestamp}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# Video Summary\n\n")
            f.write(f"Video URL: {self.video_url}\n\n")
            f.write(f"## Summary\n\n{summary}\n")
        return filename

if __name__ == "__main__":
    video_url = input("Please enter the video URL: ")
    try:
        summarizer = VideoSummarizer(video_url)
        print("Summarizing video...")
        summary = summarizer.summarize()
        filename = summarizer.save_summary_to_markdown(summary)
        print(f"\n\nSummary saved to: {filename}")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        print(f"An error occurred: {str(e)}")
