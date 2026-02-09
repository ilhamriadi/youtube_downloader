# YouTube Video Downloader

A Python script to download YouTube videos and playlists with ease. Supports video downloads, audio extraction (MP3), manual quality selection, and playlist downloads.

## Features

- **Download Video (Best Quality)** - Download video with the best available quality
- **Download Audio Only (MP3)** - Extract audio as MP3 with 192kbps bitrate
- **Manual Quality Selection** - Choose video quality manually from available formats
- **Playlist Support** - Download entire playlists with auto-skip for existing files

## Prerequisites

1. **Python 3.7+**
2. **yt-dlp** - Python library for downloading YouTube videos
3. **FFmpeg** - Required for merging video and audio streams

### Installing Prerequisites

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install FFmpeg
# Windows: Download from https://ffmpeg.org/download.html and add to PATH
# macOS: brew install ffmpeg
# Linux: sudo apt-get install ffmpeg
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/ilhamriadi/youtube-downloader.git
cd youtube-downloader
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure FFmpeg is installed and available in your system PATH.

## Usage

Run the script:

```bash
python youtube_downloader.py
```

### Menu Options

1. **Download Video (Best Quality)** - Downloads video with best video+audio quality merged as MP4
2. **Download Audio Only (MP3)** - Downloads and converts to MP3 format (192kbps)
3. **Download with Quality Selection** - Shows all available formats and lets you choose
4. **Download Playlist** - Downloads entire playlist with automatic folder creation

### Example

```
$ python youtube_downloader.py

YouTube Video Downloader
Checking prerequisites...
✓ FFmpeg found

==================================================
     YOUTUBE VIDEO DOWNLOADER
==================================================
1. Download Video (Best Quality)
2. Download Audio Only (MP3)
3. Download with Quality Selection
4. Download Playlist
0. Exit
==================================================
Select option (0-4): 1

Enter YouTube URL: https://youtube.com/watch?v=...
```

## File Structure

```
youtube-downloader/
├── youtube_downloader.py    # Main script
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── downloads/              # Downloaded files (auto-created)
```

## Requirements

- Python 3.7 or higher
- yt-dlp >= 2023.12.30
- FFmpeg (must be in system PATH)

## Notes

- Downloaded files are saved to the `downloads/` folder
- Playlist downloads create a subfolder with the playlist name
- The script skips already downloaded files (tracked in `downloads/downloaded.txt`)
- FFmpeg is required for merging separate video and audio streams

## License

This project is open source. Feel free to use and modify.

## Author

**Ilham Riadi**
- Website: [ilham.co.id](https://ilham.co.id)
- GitHub: [@ilhamriadi](https://github.com/ilhamriadi)

---

Copyright © 2025 Ilham Riadi. All rights reserved.
# youtube_downloader
