## 🎥 YouTube Downloader

**YouTube Downloader** is a lightweight Python script that lets you **download videos or audio** from YouTube using just a link. It's great for saving tutorials, music, or offline videos for study and entertainment.

---

### ✨ Features

* 🔗 Paste a YouTube URL and download in seconds
* 🎵 Download video **or** audio-only (MP3)
* 📁 Files are saved locally in a selected folder
* ✅ Simple and beginner-friendly interface (command line)

---

### 🧰 Built With

* [Python](https://www.python.org/)
* [pytube](https://github.com/pytube/pytube) — library for YouTube downloads

---

### ▶️ How to Use

1. **Clone or Download the script**

2. **Install requirements**

   ```bash
   pip install pytube
   ```

3. **Run the script**

   ```bash
   python youtube_downloader.py
   ```

4. **Paste the YouTube link** when prompted
   Choose if you want to download **video** or **audio only**

---

### 📁 Output

* Video files will be saved as `.mp4`
* Audio-only files will be saved as `.mp3` or `.webm` (depending on format)

---

### 💡 Example

```bash
Enter YouTube URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ  
Download as: [1] Video  [2] Audio  
-> 2  
Downloading audio...
Saved as: rickroll.mp3
```

---

### 🛠️ To-Do / Ideas

* Add progress bar or download status
* GUI version (with tkinter or PyQt)
* Batch downloads from a playlist or text file
* Format and resolution selection

---

### 📜 License

Feel free to use, edit, and share this script. Attribution not required — but appreciated!
