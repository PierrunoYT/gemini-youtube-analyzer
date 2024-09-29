# Video Summarizer

This project provides a tool to summarize videos by extracting key frames and generating a concise representation.

## Features

- Extract a specified number of frames from a video URL
- Convert extracted frames to base64 format
- Summarize video content based on extracted frames

## Usage

Before using the Video Summarizer, make sure you have set your Groq API key as an environment variable:

1. Open a Command Prompt with administrator privileges
2. Run the following command, replacing `your_api_key_here` with your actual Groq API key:
   ```
   setx GROQ_API_KEY "your_api_key_here"
   ```
3. Close and reopen any command prompt windows for the change to take effect

To use the Video Summarizer, you can either:

1. Run the script directly:
   ```
   python VideoSummarizer.py
   ```
   You will be prompted to enter the video URL.

2. Or, use it in your own Python script:
   ```python
   from VideoSummarizer import VideoSummarizer

   summarizer = VideoSummarizer("https://example.com/video.mp4", num_frames=5)
   summary = summarizer.summarize()
   ```

## Requirements

- Python 3.x
- Required libraries (install via pip):
  - opencv-python
  - requests

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install opencv-python requests
   ```
3. Set up your Groq API key:
   - Open a Command Prompt with administrator privileges
   - Run the following command, replacing `your_api_key_here` with your actual Groq API key:
     ```
     setx GROQ_API_KEY "your_api_key_here"
     ```
   - Close and reopen any command prompt windows for the change to take effect

## License

This project is open-source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
