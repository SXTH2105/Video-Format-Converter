"""
Video Format Converter
A desktop GUI tool to convert video containers and adjust framerates using FFmpeg.
Built with CustomTkinter and packaged for standalone distribution via PyInstaller.
"""

import os
import sys
import shutil
import subprocess
import threading
import re
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk

# Windows-specific flag to prevent black command prompt windows from popping up
# when spawning background FFmpeg subprocesses from a GUI application.
CREATE_NO_WINDOW = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0


def get_resource_path(relative_path: str) -> str:
    """
    Get the absolute path to a resource file.
    
    Why this is needed for PyInstaller:
    When bundled into a single-file executable (--onefile), PyInstaller extracts all
    bundled data files and binaries into a temporary directory at runtime, which is
    pointed to by `sys._MEIPASS`. During normal Python development, files are located
    relative to the script's actual directory.
    """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Running inside PyInstaller onefile temporary bundle
        return os.path.join(sys._MEIPASS, relative_path)
    
    # Running normally in Python development mode
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


def get_ffmpeg_path() -> str:
    """
    Finds the FFmpeg binary in a fail-safe, hierarchical order:
    1. PyInstaller bundled temp directory (sys._MEIPASS) -> when bundled into .exe
    2. Alongside the executable or main script -> for portable folder distribution
    3. imageio_ffmpeg library -> used automatically during Python development
    4. System PATH -> if the user has FFmpeg installed globally
    """
    # 1. Check if packaged with PyInstaller (_MEIPASS)
    if getattr(sys, 'frozen', False):
        base_meipass = getattr(sys, '_MEIPASS', None)
        if base_meipass:
            bundled_candidate = os.path.join(base_meipass, "ffmpeg.exe")
            if os.path.isfile(bundled_candidate):
                return bundled_candidate

        # Also check directly next to the running .exe (e.g. portable build folder)
        exe_dir = os.path.dirname(sys.executable)
        alongside_exe = os.path.join(exe_dir, "ffmpeg.exe")
        if os.path.isfile(alongside_exe):
            return alongside_exe

    # 2. Check in the local project directory (next to main.py)
    local_candidate = get_resource_path("ffmpeg.exe")
    if os.path.isfile(local_candidate):
        return local_candidate

    # 3. Fallback to imageio_ffmpeg (useful during local development)
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        pass

    # 4. Fallback to system-wide PATH
    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        return system_ffmpeg

    # Return None if not found anywhere so caller can handle gracefully
    return None


def get_video_framerate(input_file: str, ffmpeg_exe: str) -> str:
    """
    Extracts the video framerate by running a lightweight FFmpeg probe command
    and parsing the FPS from stderr metadata using regex.
    """
    if not ffmpeg_exe or not os.path.isfile(ffmpeg_exe):
        return "Unknown"

    command = [ffmpeg_exe, '-i', input_file]
    try:
        # FFmpeg outputs metadata to stderr. We suppress stdout and hide console popup window.
        result = subprocess.run(
            command,
            stderr=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            text=True,
            errors='ignore',
            creationflags=CREATE_NO_WINDOW
        )
        output = result.stderr
        match = re.search(r'(\d+(?:\.\d+)?)\s+fps', output)
        if match:
            return match.group(1)
    except Exception:
        pass
    return "Unknown"


class VideoConverterApp(ctk.CTk):
    """
    Main application GUI window.
    Provides options to select video files, pick output formats and framerates,
    and runs conversion tasks asynchronously on background threads.
    """
    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        self.title("Video Format Converter")
        self.geometry("600x470")
        self.resizable(False, False)

        # Make the main layout column expand to fill the window
        self.grid_columnconfigure(0, weight=1)

        # --- Load Window Icon if present ---
        icon_path = get_resource_path("icon.ico")
        if os.path.isfile(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass  # Fall back to default window icon if file is incompatible

        # --- State Variables ---
        self.ffmpeg_exe = get_ffmpeg_path()
        self.input_file = None
        self.current_fps = "Unknown"
        self.name_without_ext = ""
        self.ext = ""
        self.output_dir = ""

        # Build UI layout
        self.create_widgets()

        # Check FFmpeg availability and warn user immediately if missing
        if not self.ffmpeg_exe:
            messagebox.showwarning(
                "FFmpeg Not Found",
                "Could not find 'ffmpeg.exe'.\n\n"
                "Please make sure ffmpeg is placed alongside this program, "
                "bundled inside the build, or installed on your system PATH."
            )

    def create_widgets(self):
        """Constructs all UI frames, buttons, dropdowns, and status labels."""

        # --- Header Title ---
        self.header_label = ctk.CTkLabel(
            self,
            text="Video Format Converter",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.header_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # --- File Selection Frame ---
        self.file_frame = ctk.CTkFrame(self)
        self.file_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.file_frame.grid_columnconfigure(1, weight=1)

        self.browse_btn = ctk.CTkButton(
            self.file_frame,
            text="Browse Video",
            command=self.browse_file
        )
        self.browse_btn.grid(row=0, column=0, padx=10, pady=10)

        self.file_info_label = ctk.CTkLabel(
            self.file_frame,
            text="No file selected",
            justify="left"
        )
        self.file_info_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # --- Settings Frame (Format & Framerate) ---
        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.settings_frame.grid_columnconfigure(1, weight=1)

        # Output format dropdown
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
        self.format_combo = ctk.CTkComboBox(
            self.settings_frame,
            values=list(self.formats.keys()),
            variable=self.format_var
        )
        self.format_combo.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="ew")

        # Frame rate dropdown
        self.fps_label = ctk.CTkLabel(self.settings_frame, text="Frame Rate:")
        self.fps_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.fps_options = [
            "Keep Original",
            "24 fps (Cinematic)",
            "30 fps (Standard)",
            "60 fps (Smooth)",
            "120 fps (High)",
            "Custom"
        ]
        self.fps_var = ctk.StringVar(value="Keep Original")
        self.fps_combo = ctk.CTkComboBox(
            self.settings_frame,
            values=self.fps_options,
            variable=self.fps_var,
            command=self.on_fps_change
        )
        self.fps_combo.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Custom FPS Entry (Initially hidden, revealed when "Custom" is selected)
        self.custom_fps_label = ctk.CTkLabel(self.settings_frame, text="Custom FPS:")
        self.custom_fps_entry = ctk.CTkEntry(self.settings_frame, placeholder_text="e.g. 144")

        # --- Output Location Frame ---
        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.output_frame.grid_columnconfigure(1, weight=1)

        self.browse_output_btn = ctk.CTkButton(
            self.output_frame,
            text="Select Output Folder",
            command=self.browse_output_dir
        )
        self.browse_output_btn.grid(row=0, column=0, padx=10, pady=10)

        self.output_dir_label = ctk.CTkLabel(
            self.output_frame,
            text="Defaults to selected video's folder",
            justify="left"
        )
        self.output_dir_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # --- Conversion Action Frame ---
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.grid(row=4, column=0, padx=20, pady=(10, 20), sticky="ew")
        self.action_frame.grid_columnconfigure(0, weight=1)

        self.convert_btn = ctk.CTkButton(
            self.action_frame,
            text="Convert Video",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40,
            command=self.start_conversion
        )
        self.convert_btn.grid(row=0, column=0, pady=(0, 10))

        # Progress bar (Indeterminate animation during processing)
        self.progress_bar = ctk.CTkProgressBar(self.action_frame, mode="indeterminate")
        self.progress_bar.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self.progress_bar.set(0)
        self.progress_bar.grid_remove()  # Hide until conversion starts

        # Informational / status message label
        self.status_label = ctk.CTkLabel(self.action_frame, text="", text_color="gray")
        self.status_label.grid(row=2, column=0)

    def on_fps_change(self, choice: str):
        """Dynamically displays or hides the custom FPS input box."""
        if choice == "Custom":
            self.custom_fps_label.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="w")
            self.custom_fps_entry.grid(row=2, column=1, padx=10, pady=(5, 10), sticky="w")
        else:
            self.custom_fps_label.grid_forget()
            self.custom_fps_entry.grid_forget()

    def browse_output_dir(self):
        """Opens a folder picker for the user to choose custom output folder."""
        dir_path = filedialog.askdirectory(title="Select Output Directory")
        if dir_path:
            self.output_dir = dir_path
            self.output_dir_label.configure(text=self.output_dir)

    def browse_file(self):
        """Opens a file dialog to pick an input video and analyzes its metadata."""
        file_path = filedialog.askopenfilename(
            title="Select a Video File",
            filetypes=[
                ("Video Files", "*.mp4 *.mkv *.avi *.mov *.wmv *.flv *.m4p *.m4v *.qt"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            self.input_file = file_path
            filename = os.path.basename(file_path)
            self.name_without_ext, self.ext = os.path.splitext(filename)

            self.status_label.configure(text="Analyzing file metadata...", text_color="gray")
            self.update()

            # Detect current video framerate using FFmpeg
            self.current_fps = get_video_framerate(self.input_file, self.ffmpeg_exe)

            # Default output directory to the source file's directory if not set
            if not self.output_dir:
                self.output_dir = os.path.dirname(self.input_file)
                self.output_dir_label.configure(text=self.output_dir)

            info_text = f"File: {filename}\nFormat: {self.ext.upper().replace('.', '')}\nDetected FPS: {self.current_fps}"
            self.file_info_label.configure(text=info_text)
            self.status_label.configure(text="Ready to convert", text_color="green")

    def start_conversion(self):
        """Validates settings and launches conversion in a background worker thread."""
        if not self.input_file:
            messagebox.showerror("Error", "Please select a video file first.")
            return

        if not self.ffmpeg_exe or not os.path.isfile(self.ffmpeg_exe):
            messagebox.showerror(
                "FFmpeg Error",
                "FFmpeg binary not found. Cannot proceed with video conversion."
            )
            return

        # Determine target container format
        target_ext = self.ext
        format_name = self.ext.upper().replace('.', '')
        selected_format = self.formats[self.format_var.get()]
        if selected_format:
            target_ext, format_name = selected_format

        # Determine target framerate
        target_fps = None
        fps_choice = self.fps_var.get()
        if fps_choice != "Keep Original":
            if fps_choice == "Custom":
                custom_val = self.custom_fps_entry.get().strip()
                # Basic validation for positive float/integer FPS values
                if custom_val.replace('.', '', 1).isdigit() and float(custom_val) > 0:
                    target_fps = custom_val
                else:
                    messagebox.showerror("Error", "Invalid custom FPS format. Please enter a valid positive number.")
                    return
            else:
                # Extract numeric value from preset like "60 fps (Smooth)"
                target_fps = fps_choice.split()[0]

        # Prepare output directory and destination filename
        output_dir = self.output_dir if self.output_dir else os.path.dirname(self.input_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        if target_fps:
            output_filename = f"{self.name_without_ext}_{format_name}_{target_fps}fps{target_ext}"
        else:
            output_filename = f"{self.name_without_ext}_{format_name}{target_ext}"

        output_path = os.path.join(output_dir, output_filename)

        # Build FFmpeg command arguments
        # -y: automatically overwrite output if it exists
        command = [
            self.ffmpeg_exe,
            '-y',
            '-i', self.input_file
        ]

        if target_fps:
            command.extend(['-r', target_fps])

        command.append(output_path)

        # Lock controls and start progress bar animation
        self.convert_btn.configure(state="disabled")
        self.browse_btn.configure(state="disabled")
        self.progress_bar.grid()
        self.progress_bar.start()
        self.status_label.configure(text="Converting... Please wait.", text_color="#1f538d")

        # Run conversion inside a daemon thread so GUI stays responsive
        worker = threading.Thread(
            target=self.run_conversion_thread,
            args=(command, output_path),
            daemon=True
        )
        worker.start()

    def run_conversion_thread(self, command: list, output_path: str):
        """Background thread worker that invokes FFmpeg."""
        try:
            # We hide console popups on Windows and capture stderr for error diagnostics
            subprocess.run(
                command,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                creationflags=CREATE_NO_WINDOW
            )
            # Safely trigger UI update on Tkinter's main thread
            self.after(0, self.conversion_success, output_path)
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.decode('utf-8', errors='ignore') if e.stderr else str(e)
            # Truncate very long FFmpeg tracebacks for the message dialog
            snippet = err_msg.strip().splitlines()[-5:] if err_msg else ["Unknown FFmpeg failure"]
            self.after(0, self.conversion_error, "\n".join(snippet))
        except FileNotFoundError:
            self.after(0, self.conversion_error, "FFmpeg binary not found on disk.")
        except Exception as ex:
            self.after(0, self.conversion_error, str(ex))

    def conversion_success(self, output_path: str):
        """Called on main thread when conversion finishes successfully."""
        self.progress_bar.stop()
        self.progress_bar.grid_remove()
        self.convert_btn.configure(state="normal")
        self.browse_btn.configure(state="normal")
        self.status_label.configure(text="Conversion complete!", text_color="green")
        messagebox.showinfo("Success", f"Conversion completed successfully!\n\nSaved at:\n{output_path}")

    def conversion_error(self, error_msg: str):
        """Called on main thread if conversion encounters an error."""
        self.progress_bar.stop()
        self.progress_bar.grid_remove()
        self.convert_btn.configure(state="normal")
        self.browse_btn.configure(state="normal")
        self.status_label.configure(text="Conversion failed.", text_color="red")
        messagebox.showerror("Error", f"An error occurred during conversion:\n\n{error_msg}")


if __name__ == "__main__":
    # Configure CustomTkinter design theme
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("dark-blue")

    app = VideoConverterApp()
    app.mainloop()
