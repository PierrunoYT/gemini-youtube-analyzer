# Video Summarizer

This project provides a tool to summarize videos by extracting key frames and generating a concise representation.

## Features

- Extract a specified number of frames from a video URL
- Convert extracted frames to base64 format
- Summarize video content based on extracted frames

## Usage

To use the Video Summarizer, create an instance of the `VideoSummarizer` class with a video URL and optionally specify the number of frames to extract:

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
     setx GROQ_API_KEY "your_api_key_here" /M
     ```
   - Close and reopen any command prompt windows for the change to take effect

## License

This project is open-source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.