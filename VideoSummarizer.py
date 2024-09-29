import yt_dlp
import cv2
import numpy as np
from groq import Groq
from PIL import Image
import io
import base64
import os
from datetime import datetime

class VideoSummarizer:
    def __init__(self, video_url, num_frames=5):
        self.video_url = video_url
        self.num_frames = num_frames
        api_key = os.environ.get('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set. Use 'setx GROQ_API_KEY your_api_key_here' to set it.")
        self.client = Groq(api_key=api_key)

    def extract_frames(self):
        ydl_opts = {'outtmpl': 'video.%(ext)s'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.video_url, download=False)
            duration = info['duration']
            ydl.download([self.video_url])

        video = cv2.VideoCapture('video.mp4')
        frames = []
        for i in range(self.num_frames):
            video.set(cv2.CAP_PROP_POS_MSEC, (duration * 1000 * i) / self.num_frames)
            success, image = video.read()
            if success:
                frames.append(image)
        video.release()
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
        
        prompt = f"""Analyze the following video frames and provide a concise summary of the video content:

        {' '.join([f'[Frame {i+1}: data:image/jpeg;base64,{frame}]' for i, frame in enumerate(encoded_frames)])}

        Based on these key frames, summarize the main points and content of the video."""

        completion = self.client.chat.completions.create(
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
    summarizer = VideoSummarizer(video_url)
    print("Summarizing video...")
    summary = summarizer.summarize()
    filename = summarizer.save_summary_to_markdown(summary)
    print(f"\n\nSummary saved to: {filename}")
