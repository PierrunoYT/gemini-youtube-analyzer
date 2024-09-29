# Video Summarizer

Video Summarizer is a Python tool that automatically generates concise summaries of video content using advanced AI techniques. It extracts key frames from videos and uses the Groq API to analyze and summarize the content.

## Features

- Extract frames from videos using YouTube URLs
- Convert video frames to base64 format for AI processing
- Utilize Groq's powerful language model for content analysis
- Generate concise summaries of video content
- Easy-to-use command-line interface
- Implements retry mechanism with exponential backoff for API rate limiting

## Requirements

- Python 3.7+
- pip (Python package installer)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/video-summarizer.git
   cd video-summarizer
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
   
   If you encounter any issues, you can install the dependencies individually:
   ```
   pip install yt-dlp opencv-python-headless numpy requests Pillow
   ```

3. Set up your OpenRouter API key and site information:
   - Open a Command Prompt
   - Run the following commands, replacing the placeholders with your actual information:
     ```
     setx OPENROUTER_API_KEY "your_api_key_here"
     setx YOUR_SITE_URL "https://your-site-url.com"
     setx YOUR_SITE_NAME "Your Site Name"
     ```
   - Close and reopen any command prompt windows for the changes to take effect

## Usage

1. Run the script:
   ```
   python VideoSummarizer.py
   ```

2. When prompted, enter the URL of the YouTube video you want to summarize.

3. The tool will extract frames, process them, and generate a summary of the video content.

4. The summary will be saved to a markdown file in the same directory as the script.

## How It Works

1. The tool downloads the video using the provided URL.
2. It extracts a specified number of frames (default is 5) from the video.
3. The frames are converted to base64 format.
4. The Groq API is called with the frame data to analyze the content.
5. A summary is generated based on the AI's analysis of the key frames.
6. The summary is saved to a markdown file with a timestamp in the filename.

## Configuration

You can adjust the number of frames extracted by modifying the `num_frames` parameter when initializing the `VideoSummarizer` class.

## Troubleshooting

- If you encounter an "OPENROUTER_API_KEY environment variable is not set" error, make sure you've correctly set up your API key as described in the installation steps.
- Ensure you have a stable internet connection for downloading videos and accessing the Groq API.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for video downloading capabilities
- [OpenCV](https://opencv.org/) for image processing
- [OpenRouter](https://openrouter.ai/) for providing access to various AI language models
- [Google Gemini](https://deepmind.google/technologies/gemini/) for the powerful language model used in this project

## Disclaimer

This tool is for educational and research purposes only. Ensure you have the right to use and summarize the video content you're processing.
