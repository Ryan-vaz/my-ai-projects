import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import whisper
import os

# Global model cache
current_model = None
current_model_name = None

def load_model(model_name):
    global current_model, current_model_name
    if current_model is None or current_model_name != model_name:
        current_model_name = model_name
        current_model = whisper.load_model(model_name)
    return current_model

def transcribe_single(file_path, model_name, language, text_widget, progress_bar, save_automatically=True):
    try:
        text_widget.insert(tk.END, f"\nTranscribing: {os.path.basename(file_path)}...\n")
        text_widget.update()

        model = load_model(model_name)
        result = model.transcribe(file_path, language=language if language != "Auto" else None)

        text_widget.insert(tk.END, result["text"] + "\n\n")
        text_widget.update()

        if save_automatically:
            save_path = os.path.splitext(file_path)[0] + "_transcription.txt"
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(result["text"])

    except Exception as e:
        messagebox.showerror("Error", f"Error transcribing {file_path}:\n{e}")

def transcribe_batch(file_paths, model_name, language, text_widget, progress_bar):
    try:
        progress_bar.start()
        text_widget.delete(1.0, tk.END)

        for file_path in file_paths:
            transcribe_single(file_path, model_name, language, text_widget, progress_bar, save_automatically=True)

        progress_bar.stop()
        messagebox.showinfo("Success", "Batch transcription completed!")
    except Exception as e:
        progress_bar.stop()
        messagebox.showerror("Error", f"An error occurred during batch transcription: {e}")

def browse_files(entry):
    file_paths = filedialog.askopenfilenames(
        title="Select Audio/Video Files",
        filetypes=(("Audio/Video Files", "*.mp3 *.mp4 *.m4a *.wav *.webm *.mkv *.mov *.avi"), ("All Files", "*.*"))
    )
    if file_paths:
        entry.delete(0, tk.END)
        entry.insert(0, ";".join(file_paths))  # Separate files by semicolon

def start_transcription(entry, model_var, language_var, text_widget, progress_bar):
    files = entry.get().strip()
    if not files:
        messagebox.showerror("Error", "No file selected.")
        return

    file_paths = files.split(";")
    if any(not os.path.isfile(fp) for fp in file_paths):
        messagebox.showerror("Error", "One or more selected files are invalid.")
        return

    model_name = model_var.get()
    language = language_var.get()

    threading.Thread(target=transcribe_batch, args=(file_paths, model_name, language, text_widget, progress_bar), daemon=True).start()

def save_transcription(text_widget):
    text = text_widget.get(1.0, tk.END).strip()
    if not text:
        messagebox.showwarning("Warning", "No transcription to save.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        messagebox.showinfo("Success", f"Transcription saved to {file_path}")

def main():
    global current_model_name
    current_model_name = "base"  # Default model

    root = tk.Tk()
    root.title("Whisper Transcriber (Batch Enabled)")
    root.geometry("800x600")
    root.resizable(False, False)

    # File selection
    frame = tk.Frame(root)
    frame.pack(pady=10)

    entry = tk.Entry(frame, width=70)
    entry.pack(side=tk.LEFT, padx=(10, 5))

    browse_button = tk.Button(frame, text="Browse Files", command=lambda: browse_files(entry))
    browse_button.pack(side=tk.LEFT)

    # Model selection
    model_frame = tk.Frame(root)
    model_frame.pack(pady=5)

    tk.Label(model_frame, text="Model:").pack(side=tk.LEFT, padx=5)
    model_var = tk.StringVar(value="base")
    model_dropdown = ttk.Combobox(model_frame, textvariable=model_var, state="readonly")
    model_dropdown["values"] = ("tiny", "base", "small", "medium", "large")
    model_dropdown.pack(side=tk.LEFT)

    # Language selection
    tk.Label(model_frame, text="Language:").pack(side=tk.LEFT, padx=5)
    language_var = tk.StringVar(value="Auto")
    language_dropdown = ttk.Combobox(model_frame, textvariable=language_var, state="readonly")
    language_dropdown["values"] = (
        "Auto", "English", "Hindi", "Spanish", "French", "German", "Chinese", "Japanese", "Korean", "Russian", "Arabic"
    )
    language_dropdown.pack(side=tk.LEFT)

    # Start transcription button
    start_button = tk.Button(root, text="Start Transcription", command=lambda: start_transcription(entry, model_var, language_var, text_widget, progress_bar))
    start_button.pack(pady=10)

    # Progress bar
    progress_bar = ttk.Progressbar(root, mode='indeterminate', length=400)
    progress_bar.pack(pady=5)

    # Text widget to show transcription
    text_widget = tk.Text(root, wrap=tk.WORD)
    text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Save transcription button
    save_button = tk.Button(root, text="Save All Shown Transcription", command=lambda: save_transcription(text_widget))
    save_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
