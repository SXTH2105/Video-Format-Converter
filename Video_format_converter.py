import os
import subprocess
import tkinter as tk
from tkinter import filedialog

try:
    import imageio_ffmpeg
except ImportError:
    print("Required library 'imageio_ffmpeg' is not installed. Please run: pip install imageio_ffmpeg moviepy")
    exit(1)

def get_ffmpeg_path():
    return imageio_ffmpeg.get_ffmpeg_exe()
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
    
    print("\n--- File Analysis ---")
    print(f"Selected File: {filename}")
    print(f"File Type/Format: {ext.upper().replace('.', '')} ({ext})")
    
    # options for format conversion
    formats = {
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
    
    choice = input("\nEnter the number of your choice (1-9): ").strip()
    
    if choice not in formats:
        print("Invalid choice. Exiting program.")
        return
        
    target_ext, format_name = formats[choice]
    
    # save to Converted Video Folder with converted format name
    # requirement: "save the converted file into Converted Video Folder"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, "Converted Video")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"\nCreated directory: {output_dir}")
        
    # name convention: name of the file before converted + name of format that converted to
    output_filename = f"{name_without_ext}_{format_name}{target_ext}"
    output_path = os.path.join(output_dir, output_filename)
    
    print(f"\nInitializing conversion...")
    print(f"From: {input_file}")
    print(f"To:   {output_path}")
    print("This might take a while depending on the video size and format...")
    
    ffmpeg_exe = get_ffmpeg_path()
    
    # Build ffmpeg command 
    command = [
        ffmpeg_exe,
        '-y',        
        '-i', input_file,
        output_path
    ]
    
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
