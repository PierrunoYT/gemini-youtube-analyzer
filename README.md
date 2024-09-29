# Video Summarizer

Video Summarizer is a Python tool that automatically generates concise summaries of video content using advanced AI techniques. It extracts key frames from videos and uses the Groq API to analyze and summarize the content.

## Features

- Extract frames from videos using YouTube URLs
- Convert video frames to base64 format for AI processing
- Utilize Groq's powerful language model for content analysis
- Generate concise summaries of video content
- Easy-to-use command-line interface

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

3. Set up your Groq API key:
   - Open a Command Prompt
   - Run the following command, replacing `your_api_key_here` with your actual Groq API key:
     ```
     setx GROQ_API_KEY "your_api_key_here"
     ```
   - Close and reopen any command prompt windows for the change to take effect

## Usage

1. Run the script:
   ```
   python VideoSummarizer.py
   ```

2. When prompted, enter the URL of the YouTube video you want to summarize.

3. The tool will extract frames, process them, and generate a summary of the video content.

## How It Works

1. The tool downloads the video using the provided URL.
2. It extracts a specified number of frames (default is 5) from the video.
3. The frames are converted to base64 format.
4. The Groq API is called with the frame data to analyze the content.
5. A summary is generated based on the AI's analysis of the key frames.

## Configuration

You can adjust the number of frames extracted by modifying the `num_frames` parameter when initializing the `VideoSummarizer` class.

## Troubleshooting

- If you encounter a "GROQ_API_KEY environment variable is not set" error, make sure you've correctly set up your API key as described in the installation steps.
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
- [Groq](https://groq.com/) for providing the AI language model API

## Disclaimer

This tool is for educational and research purposes only. Ensure you have the right to use and summarize the video content you're processing.
