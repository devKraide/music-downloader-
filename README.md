# 🎵 YouTube Music Downloader

![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.6+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

A beautiful, user-friendly desktop application to download and convert YouTube videos to MP3 files. Get your favorite music with just a few clicks!

## ✨ Features

- 🔍 Simple and intuitive graphical user interface
- 🎧 High-quality MP3 conversion (192kbps)
- 📁 Smart default download location (local 'downloads' folder)
- 📊 Detailed download progress tracking (speed, ETA, percentage)
- ⚠️ Enhanced error handling with detailed feedback
- 🔄 Multi-threading for responsive UI during downloads
- 🛠️ Automatic retry mechanism for reliable downloads
- 📝 Clear status updates throughout the download process

## 📋 Requirements

- Python 3.6+
- yt-dlp
- FFmpeg (for audio conversion)
- Tkinter (included with standard Python)

## 🚀 Installation

1. Clone this repository or download the `youtube_music_downloader.py` file.

2. Install the required dependencies:

```bash
pip install yt-dlp
```

3. Install FFmpeg:
   - **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - **macOS:** `brew install ffmpeg`
   - **Linux:** `sudo apt install ffmpeg`

## 💻 Usage

1. Run the application:

```bash
python youtube_music_downloader.py
```

2. Paste a YouTube URL into the input field
3. (Optional) Click "Select folder" to choose a custom download location, or use the default 'downloads' folder
4. Click "Download" button
5. Monitor the progress with real-time status updates
6. Use the "Clear" button to reset the interface for your next download

## 📷 Screenshots

![Application Screenshot](assets/appWorking.png)

_Main application window showing download in progress_

## 🛠️ How It Works

The application uses yt-dlp (an improved fork of youtube-dl) to download videos from YouTube and extract their audio. It includes smart error handling with automatic retries and detailed error messages. The download process runs in a separate thread to keep the UI responsive, and provides real-time feedback including download speed, estimated time remaining, and progress percentage.

## ⚙️ Customization

You can modify these settings in the code:

- Audio quality (currently set to 192kbps)
- Number of download retries (currently set to 5)
- Socket timeout (currently set to 30 seconds)
- Default download directory
- Output file naming format

## 🤝 Contributing

Contributions are welcome! Feel free to submit pull requests or open issues to improve the application.

## 📜 License

This project is released under the MIT License.

---

Created with ❤️ by Nicolas Kraide
