import os
from yt_dlp import YoutubeDL

DOWNLOAD_FOLDER = "downloads"

def fix_youtube_url(url):
    if '/shorts/' in url:
        video_id = url.split('/shorts/')[-1].split('?')[0]
        return f"https://www.youtube.com/watch?v={video_id}"
    return url

def download_video(video_url):
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': False,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        filename = ydl.prepare_filename(info)
        return filename

def main():
    video_url = input("Enter YouTube URL: ").strip()
    video_url = fix_youtube_url(video_url)

    print(f"Downloading from: {video_url}")

    try:
        downloaded_file = download_video(video_url)
        print(f"Downloaded to: {downloaded_file}")
    except Exception as e:
        print(f"Download error: {e}")

if __name__ == "__main__":
    main()
