#!/usr/bin/env python3
"""
YouTube Video Downloader Script
Supports: video download, audio only, quality selection, playlist download
"""

import os
import sys
import shutil
import yt_dlp


# Configuration
DOWNLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")


def ensure_download_dir():
    """Create downloads directory if it doesn't exist."""
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
        print(f"Created download directory: {DOWNLOAD_DIR}")


def check_ffmpeg():
    """Check if FFmpeg is installed and in PATH."""
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        return True
    return False


def download_video(url):
    """Download video with best quality."""
    ensure_download_dir()

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'quiet': False,
        'no_warnings': False,
    }

    print(f"\nDownloading video (best quality): {url}")
    print("-" * 50)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'Unknown')
            print(f"\n✓ Successfully downloaded: {title}")
            return True
    except Exception as e:
        print(f"\n✗ Error downloading video: {e}")
        return False


def download_audio(url):
    """Download audio only as MP3."""
    ensure_download_dir()

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'no_warnings': False,
    }

    print(f"\nDownloading audio (MP3): {url}")
    print("-" * 50)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'Unknown')
            print(f"\n✓ Successfully downloaded audio: {title}")
            return True
    except Exception as e:
        print(f"\n✗ Error downloading audio: {e}")
        return False


def download_with_quality_selection(url):
    """Download video with manual quality selection."""
    ensure_download_dir()

    print(f"\nFetching available formats for: {url}")
    print("-" * 50)

    try:
        # First, get available formats
        ydl_opts_info = {
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            title = info.get('title', 'Unknown')

        # Filter video formats (with video codec)
        video_formats = []
        for i, f in enumerate(formats):
            if f.get('vcodec') != 'none' and f.get('height'):
                video_formats.append({
                    'index': i,
                    'format_id': f['format_id'],
                    'ext': f['ext'],
                    'resolution': f.get('resolution', 'unknown'),
                    'height': f.get('height', 0),
                    'fps': f.get('fps', 'unknown'),
                    'filesize': f.get('filesize') or f.get('filesize_approx', 0),
                })

        # Sort by height (quality)
        video_formats.sort(key=lambda x: x['height'], reverse=True)

        if not video_formats:
            print("No video formats found!")
            return False

        # Display formats
        print(f"\nAvailable video formats for: {title}")
        print("-" * 70)
        print(f"{'No.':<5} {'Resolution':<12} {'FPS':<8} {'Format':<8} {'Size':<15}")
        print("-" * 70)

        for i, f in enumerate(video_formats[:20], 1):  # Show top 20 formats
            size_str = "Unknown"
            if f['filesize']:
                size_mb = f['filesize'] / (1024 * 1024)
                size_str = f"{size_mb:.1f} MB"
            print(f"{i:<5} {f['resolution']:<12} {str(f['fps']):<8} {f['ext']:<8} {size_str:<15}")

        print("-" * 70)

        # Get user selection
        while True:
            try:
                choice = input(f"\nSelect quality (1-{min(len(video_formats), 20)}), or 0 to cancel: ")
                choice = int(choice)
                if choice == 0:
                    print("Download cancelled.")
                    return False
                if 1 <= choice <= min(len(video_formats), 20):
                    selected = video_formats[choice - 1]
                    break
                else:
                    print(f"Please enter a number between 1 and {min(len(video_formats), 20)}")
            except ValueError:
                print("Please enter a valid number.")

        # Download with selected format
        format_spec = f"{selected['format_id']}+bestaudio/best"

        ydl_opts = {
            'format': format_spec,
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'quiet': False,
            'no_warnings': False,
        }

        print(f"\nDownloading with {selected['resolution']} quality...")
        print("-" * 50)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print(f"\n✓ Successfully downloaded: {title}")
            return True

    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


def download_playlist(url):
    """Download entire playlist."""
    ensure_download_dir()

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(playlist_title)s', '%(playlist_index)s - %(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'quiet': False,
        'no_warnings': False,
        'ignoreerrors': True,  # Skip videos that fail
        'download_archive': os.path.join(DOWNLOAD_DIR, 'downloaded.txt'),  # Skip already downloaded
    }

    print(f"\nDownloading playlist: {url}")
    print("-" * 50)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            playlist_title = info.get('title', 'Unknown') if info else 'Unknown'
            print(f"\n✓ Playlist download completed: {playlist_title}")
            return True
    except Exception as e:
        print(f"\n✗ Error downloading playlist: {e}")
        return False


def show_menu():
    """Display main menu."""
    print("\n" + "=" * 50)
    print("     YOUTUBE VIDEO DOWNLOADER")
    print("=" * 50)
    print("1. Download Video (Best Quality)")
    print("2. Download Audio Only (MP3)")
    print("3. Download with Quality Selection")
    print("4. Download Playlist")
    print("0. Exit")
    print("=" * 50)


def main():
    """Main function."""
    print("\nYouTube Video Downloader")
    print("Checking prerequisites...")

    # Check FFmpeg
    if not check_ffmpeg():
        print("\n⚠ Warning: FFmpeg not found in PATH!")
        print("Some features may not work properly.")
        print("Please install FFmpeg and add it to your PATH.")
        print("Download from: https://ffmpeg.org/download.html")
    else:
        print("✓ FFmpeg found")

    # Ensure download directory exists
    ensure_download_dir()

    while True:
        show_menu()
        choice = input("Select option (0-4): ").strip()

        if choice == '0':
            print("\nGoodbye!")
            sys.exit(0)

        if choice not in ['1', '2', '3', '4']:
            print("\nInvalid option. Please try again.")
            continue

        url = input("\nEnter YouTube URL: ").strip()

        if not url:
            print("URL cannot be empty!")
            continue

        if choice == '1':
            download_video(url)
        elif choice == '2':
            download_audio(url)
        elif choice == '3':
            download_with_quality_selection(url)
        elif choice == '4':
            download_playlist(url)

        print("\n" + "-" * 50)
        input("Press Enter to continue...")


if __name__ == "__main__":
    main()
