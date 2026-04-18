import os
import subprocess
import threading
import re
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk

try:
    import imageio_ffmpeg
except ImportError:
    print("Required library 'imageio_ffmpeg' is not installed. Please run: pip install imageio_ffmpeg moviepy")
    exit(1)

def get_ffmpeg_path():
    return imageio_ffmpeg.get_ffmpeg_exe()

def get_video_framerate(input_file, ffmpeg_exe):
    command = [ffmpeg_exe, '-i', input_file]
    try:
        # ffmpeg outputs metadata to stderr
        result = subprocess.run(command, stderr=subprocess.PIPE, text=True, errors='ignore')
        output = result.stderr
        match = re.search(r'(\d+(?:\.\d+)?)\s+fps', output)
        if match:
            return match.group(1)
    except Exception:
        pass
    return "Unknown"

class VideoConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Video Format Converter")
        self.geometry("600x450")
        
        # grid layout
        self.grid_columnconfigure(0, weight=1)
        
        self.ffmpeg_exe = get_ffmpeg_path()
        self.input_file = None
        self.current_fps = "Unknown"
        self.name_without_ext = ""
        self.ext = ""
        self.output_dir = ""
        
        self.create_widgets()

    def create_widgets(self):
        # Header
        self.header_label = ctk.CTkLabel(self, text="Video Format Converter", font=ctk.CTkFont(size=24, weight="bold"))
        self.header_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # --- File Selection Frame ---
        self.file_frame = ctk.CTkFrame(self)
        self.file_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.file_frame.grid_columnconfigure(1, weight=1)

        self.browse_btn = ctk.CTkButton(self.file_frame, text="Browse Video", command=self.browse_file)
        self.browse_btn.grid(row=0, column=0, padx=10, pady=10)

        self.file_info_label = ctk.CTkLabel(self.file_frame, text="No file selected", justify="left")
        self.file_info_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # --- Settings Frame ---
        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.settings_frame.grid_columnconfigure(1, weight=1)

        # Output Format
        self.format_label = ctk.CTkLabel(self.settings_frame, text="Output Format:")
        self.format_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        
        self.formats = {
            "Keep Original": None,
            "MP4 (.mp4)": (".mp4", "MP4"),
            "MOV (.mov)": (".mov", "MOV"),
            "MKV (.mkv)": (".mkv", "MKV"),
            "AVI (.avi)": (".avi", "AVI"),
            "WMV (.wmv)": (".wmv", "WMV"),
            "FLV (.flv)": (".flv", "FLV")
        }
        self.format_var = ctk.StringVar(value="Keep Original")
        self.format_combo = ctk.CTkComboBox(self.settings_frame, values=list(self.formats.keys()), variable=self.format_var)
        self.format_combo.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="ew")

        # Frame Rate
        self.fps_label = ctk.CTkLabel(self.settings_frame, text="Frame Rate:")
        self.fps_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.fps_options = ["Keep Original", "24 fps (Cinematic)", "30 fps (Standard)", "60 fps (Smooth)", "120 fps (High)", "Custom"]
        self.fps_var = ctk.StringVar(value="Keep Original")
        self.fps_combo = ctk.CTkComboBox(self.settings_frame, values=self.fps_options, variable=self.fps_var, command=self.on_fps_change)
        self.fps_combo.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Custom FPS Entry (Hidden by default)
        self.custom_fps_label = ctk.CTkLabel(self.settings_frame, text="Custom FPS:")
        self.custom_fps_entry = ctk.CTkEntry(self.settings_frame, placeholder_text="e.g. 144")

        # --- Output Location Frame ---
        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.output_frame.grid_columnconfigure(1, weight=1)

        self.browse_output_btn = ctk.CTkButton(self.output_frame, text="Select Output Folder", command=self.browse_output_dir)
        self.browse_output_btn.grid(row=0, column=0, padx=10, pady=10)

        self.output_dir_label = ctk.CTkLabel(self.output_frame, text="Defaults to selected video's folder", justify="left")
        self.output_dir_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # --- Conversion Action Frame ---
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.grid(row=4, column=0, padx=20, pady=(10, 20), sticky="ew")
        self.action_frame.grid_columnconfigure(0, weight=1)

        self.convert_btn = ctk.CTkButton(self.action_frame, text="Convert Video", font=ctk.CTkFont(size=16, weight="bold"), height=40, command=self.start_conversion)
        self.convert_btn.grid(row=0, column=0, pady=(0, 10))

        self.progress_bar = ctk.CTkProgressBar(self.action_frame, mode="indeterminate")
        self.progress_bar.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self.progress_bar.set(0) # reset value
        self.progress_bar.grid_remove() # hide initially

        self.status_label = ctk.CTkLabel(self.action_frame, text="", text_color="gray")
        self.status_label.grid(row=2, column=0)

    def on_fps_change(self, choice):
        if choice == "Custom":
            self.custom_fps_label.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="w")
            self.custom_fps_entry.grid(row=2, column=1, padx=10, pady=(5, 10), sticky="w")
        else:
            self.custom_fps_label.grid_forget()
            self.custom_fps_entry.grid_forget()

    def browse_output_dir(self):
        dir_path = filedialog.askdirectory(title="Select Output Directory")
        if dir_path:
            self.output_dir = dir_path
            self.output_dir_label.configure(text=self.output_dir)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a Video File",
            filetypes=[("Video Files", "*.mp4 *.mkv *.avi *.mov *.wmv *.flv *.m4p *.m4v *.qt"), ("All Files", "*.*")]
        )
        if file_path:
            self.input_file = file_path
            filename = os.path.basename(file_path)
            self.name_without_ext, self.ext = os.path.splitext(filename)
            self.status_label.configure(text="Analyzing file...", text_color="gray")
            self.update()
            
            self.current_fps = get_video_framerate(self.input_file, self.ffmpeg_exe)
            
            # Default output dir to input file dir if not already set
            if not self.output_dir:
                self.output_dir = os.path.dirname(self.input_file)
                self.output_dir_label.configure(text=self.output_dir)
            
            info_text = f"File: {filename}\nFormat: {self.ext.upper().replace('.', '')}\nFPS: {self.current_fps}"
            self.file_info_label.configure(text=info_text)
            self.status_label.configure(text="Ready to convert", text_color="green")

    def start_conversion(self):
        if not self.input_file:
            messagebox.showerror("Error", "Please select a video file first.")
            return

        target_ext, format_name = self.ext, self.ext.upper().replace('.', '')
        selected_format = self.formats[self.format_var.get()]
        if selected_format:
            target_ext, format_name = selected_format

        target_fps = None
        fps_choice = self.fps_var.get()
        if fps_choice != "Keep Original":
            if fps_choice == "Custom":
                custom_val = self.custom_fps_entry.get().strip()
                if custom_val.replace('.', '', 1).isdigit():
                    target_fps = custom_val
                else:
                    messagebox.showerror("Error", "Invalid custom FPS format. Please enter a valid number.")
                    return
            else:
                # Extract number from "XX fps (...)"
                target_fps = fps_choice.split()[0]

        # Setup paths
        output_dir = self.output_dir
        if not output_dir: # Fallback just in case
            output_dir = os.path.dirname(self.input_file)
            
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        if target_fps:
            output_filename = f"{self.name_without_ext}_{format_name}_{target_fps}fps{target_ext}"
        else:
            output_filename = f"{self.name_without_ext}_{format_name}{target_ext}"
            
        output_path = os.path.join(output_dir, output_filename)

        # Build FFmpeg command
        command = [
            self.ffmpeg_exe,
            '-y',        
            '-i', self.input_file
        ]
        
        if target_fps:
            command.extend(['-r', target_fps])
            
        command.append(output_path)

        # Disable UI and show progress
        self.convert_btn.configure(state="disabled")
        self.browse_btn.configure(state="disabled")
        self.progress_bar.grid()
        self.progress_bar.start()
        self.status_label.configure(text="Converting... Please wait.", text_color="#1f538d") # theme blue color

        # Run conversion in a separate thread
        threading.Thread(target=self.run_conversion_thread, args=(command, output_path), daemon=True).start()

    def run_conversion_thread(self, command, output_path):
        try:
            subprocess.run(command, check=True)
            self.after(0, self.conversion_success, output_path)
        except subprocess.CalledProcessError as e:
            self.after(0, self.conversion_error, str(e))
        except FileNotFoundError:
            self.after(0, self.conversion_error, "FFmpeg not found.")

    def conversion_success(self, output_path):
        self.progress_bar.stop()
        self.progress_bar.grid_remove()
        self.convert_btn.configure(state="normal")
        self.browse_btn.configure(state="normal")
        self.status_label.configure(text=f"Success! Saved to:\n{output_path}", text_color="green")
        messagebox.showinfo("Success", f"Conversion completed successfully!\n\nSaved at: {output_path}")

    def conversion_error(self, error_msg):
        self.progress_bar.stop()
        self.progress_bar.grid_remove()
        self.convert_btn.configure(state="normal")
        self.browse_btn.configure(state="normal")
        self.status_label.configure(text="Conversion failed.", text_color="red")
        messagebox.showerror("Error", f"An error occurred during conversion:\n{error_msg}")

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("dark-blue")
    
    app = VideoConverterApp()
    app.mainloop()
