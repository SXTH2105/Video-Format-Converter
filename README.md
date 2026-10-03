# 🎬 Video Format Converter

A Python desktop application that converts video files between popular formats **and lets you control the frame rate** — using a full graphical user interface (GUI) and FFmpeg under the hood. No command-line knowledge required.

Available both as a Python script and as a **standalone Windows `.exe`** with zero external dependencies.

---

## 📋 Overview

This tool lets you select any video file and convert it seamlessly via an interactive GUI built with CustomTkinter. The interface allows you to view the selected file's format and frame rate, choose a target format and FPS, then automatically convert and save the output.

The project is fully configured for standalone distribution via **PyInstaller**: FFmpeg, CustomTkinter themes, and required dependencies are bundled directly into a single `.exe` file. Users can double-click and run the application without needing Python or FFmpeg installed.

---

## ✨ Features

- 🖥️ **Full Modern GUI** — dark-mode ready graphical interface using CustomTkinter
- 📦 **Standalone Windows Executable** — portable single-file `.exe` build with no Python or FFmpeg setup required
- 🖱️ **File picker** — browse and select your video file visually
- 🔍 **File analysis** — displays the selected file's name, format, and **detected frame rate** before converting
- 🎞️ **Multiple output format options** across MP4, MOV, MKV, AVI, WMV, and FLV groups
- 🔁 **Keep original format** — option to re-encode without changing the container
- 🎛️ **Frame rate control** — choose from presets (24, 30, 60, 120 fps) or enter a **custom FPS**
- 🏷️ **Smart file naming** — output files are named as `originalname_FORMAT_FPSfps.ext`
- ⏳ **Background processing** — UI remains fully responsive during video conversion with active progress feedback
- 🔇 **Zero Console Popups** — FFmpeg operations run completely silently in the background
- ⚡ **Fail-Safe FFmpeg Resolution** — automatically finds FFmpeg in PyInstaller bundles (`_MEIPASS`), local folder, `imageio_ffmpeg`, or system `PATH`
- 🎨 **Custom Icon Support** — seamlessly applies `.ico` icons to both the executable and window title bar

---

## 🎞️ Supported Output Formats

| Group | Extensions |
|-------|------------|
| MP4   | `.mp4`, `.m4p`, `.m4v` |
| MOV   | `.mov`, `.qt` |
| Other | `.mkv`, `.avi`, `.wmv`, `.flv` |

---

## 🎛️ Frame Rate Presets

| Option | FPS | Use Case |
|--------|-----|----------|
| 0 | Keep original | No change |
| 1 | 24 fps | Cinematic look |
| 2 | 30 fps | Standard video |
| 3 | 60 fps | Smooth motion |
| 4 | 120 fps | High frame rate |
| 5 | Custom | Enter any value (e.g. 144) |

---

## 🛠️ Tech Stack

- **Python 3**
- **CustomTkinter** — modern GUI and dark-blue theme components
- **Tkinter** — file dialogs and alert dialogs
- **FFmpeg** — high-performance media transcoding and metadata probe
- **imageio_ffmpeg** — automated FFmpeg binary distribution for Python environments
- **PyInstaller** — standalone Windows `.exe` packaging
- **threading** — background conversion worker preventing UI freeze
- **subprocess** — hidden background FFmpeg process management (`CREATE_NO_WINDOW`)

---

## 🚀 Getting Started (Run from Source)

### 1. Prerequisites

Install the required Python packages:

```bash
pip install customtkinter imageio_ffmpeg
```

### 2. Clone the Repository

```bash
git clone https://github.com/SXTH2105/Video-Format-Converter.git
cd Video-Format-Converter
```

### 3. Run the Application

```bash
python main.py
```

---

## 📦 Building Standalone Windows Executable (.exe)

You can package the application into a single `.exe` file that users can run by simply double-clicking—no Python or manual setup required.

### 1. Install PyInstaller

```powershell
pip install pyinstaller
```

### 2. Prepare `ffmpeg.exe`

Ensure `ffmpeg.exe` is in your project directory. If you have `imageio_ffmpeg` installed, copy the binary to your project folder with this one-liner:

```powershell
python -c "import imageio_ffmpeg, shutil; shutil.copy(imageio_ffmpeg.get_ffmpeg_exe(), 'ffmpeg.exe')"
```

### 3. Build the Executable

**Without a custom icon:**

```powershell
pyinstaller --noconsole --onefile --collect-all customtkinter --add-binary "ffmpeg.exe;." --name "VideoConverter" main.py
```

**With a custom icon (`icon.ico`):**

```powershell
pyinstaller --noconsole --onefile --collect-all customtkinter --add-binary "ffmpeg.exe;." --add-data "icon.ico;." --icon="icon.ico" --name "VideoConverter" main.py
```

#### What these flags do:
- `--noconsole`: Hides the background terminal window.
- `--onefile`: Packages everything into a single standalone `.exe`.
- `--collect-all customtkinter`: Includes all CustomTkinter theme JSON files, fonts, and assets.
- `--add-binary "ffmpeg.exe;."`: Bundles FFmpeg into the application's runtime temporary directory (`sys._MEIPASS`).
- `--icon="icon.ico"`: Embeds the icon into the executable for Windows File Explorer.
- `--add-data "icon.ico;."`: Bundles the icon file so the GUI titlebar can display it.

The resulting executable will be in the **`dist/`** directory (`dist/VideoConverter.exe`).

---

## 📖 How It Works

1. Launch the application or double-click `VideoConverter.exe`.
2. Click **Browse Video** and select your video file.
3. The app displays the file name, container format, and **detected frame rate**.
4. Choose an output format from the dropdown menu, or select to keep the original.
5. Choose a target frame rate from presets or choose **Custom** to enter any numeric value.
6. (Optional) Click **Select Output Folder** to specify where the converted file should be saved (defaults to the source video folder).
7. Click **Convert Video**. An animated progress bar indicates active processing in a background worker thread.
8. A success popup appears upon completion with the saved file path!

---

## 🗂️ Output Example

```
Selected Folder/
├── myvideo_MP4_60fps.mp4
├── myvideo_MKV.mkv
└── clip_AVI_30fps.avi
```

---

## 📁 Project Structure

```
Video-Format-Converter/
│
├── main.py                     # Main application source code
├── ffmpeg.exe                  # Standalone FFmpeg binary for packaging
├── icon.ico                    # Application icon (optional)
├── dist/
│   └── VideoConverter.exe      # Compiled standalone Windows executable
├── build/                      # PyInstaller build artifacts
├── README.md                   # Documentation
└── .gitignore                  # Git ignore rules
```

---

## 📝 Changelog

### v3.1.0
- 📦 **Standalone Windows Executable**: Added full PyInstaller support with single-file bundling (`--onefile`, `--noconsole`).
- ⚡ **Bundled FFmpeg Integration**: Added `sys._MEIPASS` runtime extraction and hierarchical binary lookup (bundle -> local -> imageio_ffmpeg -> system PATH).
- 🔇 **Silent FFmpeg Execution**: Added `CREATE_NO_WINDOW` flag for subprocess calls to eliminate command prompt window popups on Windows.
- 🎨 **Custom Icon Support**: Added automatic window titlebar and file icon embedding.
- 🛡️ **Graceful Error Handling**: Improved error popups for missing dependencies and invalid custom framerates.
- 💬 **Code Documentation**: Humanized codebase with thorough developer comments and docstrings.

### v3.0.0
- 🚀 Complete overhaul from CLI to a full **Modern GUI** using CustomTkinter
- ⏳ Integrated background threading to prevent UI freezing during conversion
- 🔄 Added an indeterminate progress bar mechanism
- 📥 Replaced all CLI number prompts with dropdown menus and interactive buttons

### v2.0.0
- ➕ Added real-time **frame rate detection** from video metadata
- ➕ Added **frame rate selection menu** with presets (24, 30, 60, 120 fps)
- ➕ Added **custom FPS input** option
- ➕ Added **option 0** to keep the original format without re-encoding to a new container
- ✏️ Updated output filename convention to include FPS when changed
- ✏️ Updated format menu numbering from (1–9) to (0–9)

### v1.0.0
- 🎉 Initial release with format conversion and GUI file picker

---

## ⚠️ Notes

- The target output folder is created automatically if it doesn't exist.
- Conversion speed depends on hardware specifications, input video resolution, and chosen codecs.
- Frame rate is probed non-destructively by parsing FFmpeg stderr output.

---

## 👤 Author

**Seth**
- GitHub: [@SXTH2105](https://github.com/SXTH2105)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
