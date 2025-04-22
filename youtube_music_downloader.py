import os
import re
import tkinter as tk
from tkinter import filedialog, StringVar, messagebox
import threading
import time

# Using yt-dlp instead of pytube for greater reliability
# pip install yt-dlp
import yt_dlp

class YoutubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Downloader")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        # Variables
        self.url_var = StringVar()
        self.status_var = StringVar()
        self.status_var.set("Ready to download")
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        
        # Interface
        self._create_widgets()
        
    def _create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(main_frame, text="Music Downloader", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        # URL field
        url_frame = tk.Frame(main_frame)
        url_frame.pack(fill="x", pady=20)
        
        tk.Label(url_frame, text="YouTube URL:", font=("Helvetica", 12)).pack(side="left")
        tk.Entry(url_frame, textvariable=self.url_var, width=40, font=("Helvetica", 12)).pack(side="left", padx=10, fill="x", expand=True)
        
        # Buttons
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(fill="x", pady=20)
        
        tk.Button(buttons_frame, text="Select folder", command=self.select_directory, font=("Helvetica", 12)).pack(side="left", padx=5)
        tk.Button(buttons_frame, text="Download", command=self.start_download_thread, font=("Helvetica", 12), bg="#4CAF50", fg="white").pack(side="left", padx=5)
        tk.Button(buttons_frame, text="Clear", command=self.clear_fields, font=("Helvetica", 12)).pack(side="left", padx=5)
        
        # Display selected folder
        self.path_label = tk.Label(main_frame, text=f"Folder: {self.download_path}", font=("Helvetica", 10))
        self.path_label.pack(anchor="w", pady=10)
        
        # Status bar
        status_frame = tk.Frame(main_frame, relief=tk.SUNKEN, bd=1)
        status_frame.pack(fill="x", side="bottom", pady=10)
        
        self.status_label = tk.Label(status_frame, textvariable=self.status_var, font=("Helvetica", 10))
        self.status_label.pack(anchor="w", padx=10, pady=5)
    
    def select_directory(self):
        path = filedialog.askdirectory()
        if path:
            self.download_path = path
            self.path_label.config(text=f"Folder: {self.download_path}")
    
    def start_download_thread(self):
        # Start download in a separate thread to avoid freezing the interface
        download_thread = threading.Thread(target=self.download_music)
        download_thread.daemon = True
        download_thread.start()
    
    def download_music(self):
        url = self.url_var.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL.")
            return
        
        try:
            self.status_var.set("Connecting to YouTube...")
            
            # Options for yt-dlp
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'progress_hooks': [self.progress_hook],
                'verbose': True,
                'ignoreerrors': True,
                'retries': 5,  # Increase the number of attempts
                'socket_timeout': 30  # Increase socket timeout
            }
            
            # Get video information first to display the title
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                try:
                    info = ydl.extract_info(url, download=False)
                    if info:
                        title = info.get('title', 'Unknown file')
                        self.status_var.set(f"Downloading: {title}")
                    else:
                        self.status_var.set("Could not retrieve video information, but attempting to download anyway...")
                except Exception as e:
                    self.status_var.set(f"Warning: Could not retrieve preliminary information: {str(e)}")
            
            # Start the download
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            self.status_var.set("Download completed successfully!")
            messagebox.showinfo("Success", f"Download completed!\nSaved in: {self.download_path}")
            
        except Exception as e:
            error_message = str(e)
            self.status_var.set(f"Error: {error_message}")
            
            # More descriptive error messages based on the type of error
            if "HTTP Error 400: Bad Request" in error_message:
                messagebox.showerror("Error", "Bad Request (Error 400). The URL may be incorrect or the video may not be available.")
            elif "HTTP Error 403" in error_message:
                messagebox.showerror("Error", "Forbidden access (Error 403). YouTube is blocking access.")
            elif "HTTP Error 429" in error_message:
                messagebox.showerror("Error", "Too many requests (Error 429). Try again later.")
            elif "socket" in error_message.lower() or "timeout" in error_message.lower():
                messagebox.showerror("Error", "Connection timeout exceeded. Check your internet connection.")
            else:
                messagebox.showerror("Error", f"An error occurred during the download:\n{error_message}")
    
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            # Update the progress bar if available
            percent = d.get('_percent_str', 'unknown')
            speed = d.get('_speed_str', 'unknown')
            eta = d.get('_eta_str', 'unknown')
            self.status_var.set(f"Downloading: {percent} | Speed: {speed} | Remaining time: {eta}")
        elif d['status'] == 'finished':
            self.status_var.set("Download completed. Converting to MP3...")
        elif d['status'] == 'error':
            self.status_var.set(f"Error during download: {d.get('error', 'Unknown error')}")
    
    def clear_fields(self):
        self.url_var.set("")
        self.status_var.set("Ready to download")

def main():
    root = tk.Tk()
    app = YoutubeDownloader(root)
    root.mainloop()

if __name__ == "__main__":
    main()