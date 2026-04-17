import os
import subprocess
import tkinter as tk
from tkinter import filedialog
import re

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

#Selected file window popup
def select_file():
    print("Opening file dialog... Please select a video file.")
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    
    file_path = filedialog.askopenfilename(
        title="Select a Video File",
        filetypes=[("Video Files", "*.mp4 *.mkv *.avi *.mov *.wmv *.flv *.m4p *.m4v *.qt"), ("All Files", "*.*")]
    )
    return file_path

def main():
    print("=" * 40)
    print("       VIDEO FORMAT CONVERTER       ")
    print("=" * 40)
    
    # ask user for the file and analyze file type
    input_file = select_file()
    
    if not input_file:
        print("No file was selected. Exiting program.")
        return
        
    filename = os.path.basename(input_file)
    name_without_ext, ext = os.path.splitext(filename)
    
    ffmpeg_exe = get_ffmpeg_path()
    current_fps = get_video_framerate(input_file, ffmpeg_exe)
    
    print("\n--- File Analysis ---")
    print(f"Selected File: {filename}")
    print(f"File Type/Format: {ext.upper().replace('.', '')} ({ext})")
    print(f"Current Frame Rate: {current_fps} fps")
    
    # options for format conversion
    formats = {
        '0': (ext, ext.upper().replace('.', '')),
        '1': ('.mp4', 'MP4'),
        '2': ('.m4p', 'MP4'),
        '3': ('.m4v', 'MP4'),
        '4': ('.mov', 'MOV'),
        '5': ('.qt', 'MOV'),
        '6': ('.mkv', 'MKV'),
        '7': ('.avi', 'AVI'),
        '8': ('.wmv', 'WMV'),
        '9': ('.flv', 'FLV'),
    }
    
    print("\n--- Select Output Format ---")
    print("  0. Keep original format")
    print("MP4 Group:")
    print("  1. .mp4")
    print("  2. .m4p")
    print("  3. .m4v")
    print("MOV Group:")
    print("  4. .mov")
    print("  5. .qt")
    print("Other Formats:")
    print("  6. .mkv (MKV)")
    print("  7. .avi (AVI)")
    print("  8. .wmv (Windows Media Video)")
    print("  9. .flv (Flash Video)")
    
    choice = input("\nEnter the number of your choice (0-9): ").strip()
    
    if choice not in formats:
        print("Invalid choice. Exiting program.")
        return
        
    target_ext, format_name = formats[choice]
    
    print("\n--- Select Frame Rate ---")
    print(f"  0. Keep original frame rate ({current_fps} fps)")
    print("  1. 24 fps (Cinematic)")
    print("  2. 30 fps (Standard)")
    print("  3. 60 fps (Smooth)")
    print("  4. 120 fps (High)")
    print("  5. Custom frame rate")
    
    fps_choice = input("\nEnter the number of your choice (0-5): ").strip()
    target_fps = None
    
    fps_options = {
        '1': '24',
        '2': '30',
        '3': '60',
        '4': '120'
    }
    
    if fps_choice == '5':
        custom_fps = input("Enter custom frame rate (e.g. 144): ").strip()
        if custom_fps.replace('.', '', 1).isdigit():
            target_fps = custom_fps
        else:
            print("Invalid fps format. Keeping original frame rate.")
    elif fps_choice in fps_options:
        target_fps = fps_options[fps_choice]
    
    # save to Converted Video Folder with converted format name
    # requirement: "save the converted file into Converted Video Folder"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, "Converted Video")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"\nCreated directory: {output_dir}")
        
    # name convention: name of the file before converted + name of format that converted to
    if target_fps:
        output_filename = f"{name_without_ext}_{format_name}_{target_fps}fps{target_ext}"
    else:
        output_filename = f"{name_without_ext}_{format_name}{target_ext}"
        
    output_path = os.path.join(output_dir, output_filename)
    
    print(f"\nInitializing conversion...")
    print(f"From: {input_file}")
    print(f"To:   {output_path}")
    print("This might take a while depending on the video size and format...")
    
    # Build ffmpeg command 
    command = [
        ffmpeg_exe,
        '-y',        
        '-i', input_file
    ]
    
    if target_fps:
        command.extend(['-r', target_fps])
        
    command.append(output_path)
    
    try:
        # Run ffmpeg, wait for completion
        subprocess.run(command, check=True)
        print(f"\n[SUCCESS] Conversion completed successfully!")
        print(f"File saved at: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] An error occurred during conversion:")
        print(e)
    except FileNotFoundError:
        print(f"\n[ERROR] FFmpeg not found at {ffmpeg_exe}. Make sure imageio_ffmpeg is correctly installed.")

if __name__ == "__main__":
    main()
