# Video Summarizer

Video Summarizer is a Python tool that automatically generates concise summaries of YouTube video content using advanced AI techniques. It utilizes the Google Gemini API to analyze both visual and audio content of the video.

## Features

- Download YouTube videos
- Analyze video thumbnails and content
- Utilize Google's Gemini AI for comprehensive content analysis
- Generate detailed summaries of video content
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

3. Set up your API key:
   - Open a Command Prompt
   - Run the following command, replacing the placeholder with your actual API key:
     ```
     setx GEMINI_API_KEY "your_gemini_api_key_here"
     ```
   - Close and reopen any command prompt windows for the changes to take effect

## Usage

1. Run the script:
   ```
   python VideoSummarizer.py
   ```

2. When prompted, enter the URL of the YouTube video you want to summarize.

3. The tool will download the video, analyze the content, and generate a summary.

4. The summary will be displayed in the console.

## How It Works

1. The tool uses yt-dlp to fetch video details and download the video.
2. The thumbnail image and video file are uploaded to the Google Gemini API.
3. The Gemini AI model analyzes both the visual and audio content.
4. A comprehensive summary is generated based on the AI's analysis.

## Troubleshooting

- If you encounter API key errors, make sure you've correctly set up your Gemini API key as described in the installation steps.
- Ensure you have a stable internet connection for downloading videos and accessing the API.

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
- [Google Gemini API](https://deepmind.google/technologies/gemini/) for the powerful AI model used in this project

## Disclaimer

This tool is for educational and research purposes only. Ensure you have the right to use and summarize the video content you're processing. Respect YouTube's terms of service and the video creators' rights when using this tool.
