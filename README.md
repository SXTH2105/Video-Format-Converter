# 🎬 Video Format Converter

A Python desktop application that converts video files between popular formats using a file picker GUI and FFmpeg under the hood — no command-line knowledge required.

---

## 📋 Overview

This tool lets you select any video file through a graphical file dialog, choose a target format from a menu of 9 options, and automatically convert and save the output to a dedicated `Converted Video/` folder. It uses `imageio_ffmpeg` to bundle FFmpeg, so no manual FFmpeg installation is needed.

---

## ✨ Features

- 🖱️ **GUI file picker** — browse and select your video file visually via Tkinter
- 🎞️ **9 output format options** across MP4, MOV, MKV, AVI, WMV, and FLV groups
- 📂 **Auto-saves** converted files to a `Converted Video/` folder
- 🏷️ **Smart file naming** — output files are named as `originalname_FORMAT.ext`
- ⚡ **Bundled FFmpeg** via `imageio_ffmpeg` — no external FFmpeg installation required
- 🔍 **File analysis** — displays the selected file's name and current format before conversion

---

## 🎞️ Supported Formats

| Group | Extensions |
|---|---|
| MP4 | `.mp4`, `.m4p`, `.m4v` |
| MOV | `.mov`, `.qt` |
| Other | `.mkv`, `.avi`, `.wmv`, `.flv` |

---

## 🛠️ Tech Stack

- **Python 3**
- **Tkinter** — for the file picker dialog
- **imageio_ffmpeg** — for bundled FFmpeg binary
- **subprocess** — to run the FFmpeg conversion command
- **os** — for file path and directory management

---

## 🚀 Getting Started

### Prerequisites

Install the required library:

```bash
pip install imageio_ffmpeg
```

> `moviepy` is also listed as a companion install but is not required for core functionality.

### Installation

1. Clone the repository:

```bash
git clone https://github.com/SXTH2105/Video-Format-Converter.git
cd Video-Format-Converter
```

2. Run the script:

```bash
python Video_format_converter.py
```

---

## 📖 How It Works

1. A file dialog window opens — select your video file (supports `.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`, `.m4p`, `.m4v`, `.qt`).
2. The app displays the selected file's name and detected format.
3. A numbered menu presents 9 output format options to choose from.
4. FFmpeg performs the conversion in the background.
5. The converted file is saved to the `Converted Video/` folder in the project directory, named as `originalname_FORMAT.ext`.

---

## 🗂️ Output Example

```
Converted Video/
├── myvideo_MP4.mp4
├── myvideo_MKV.mkv
└── clip_AVI.avi
```

---

## 📁 Project Structure

```
Video-Format-Converter/
│
├── Video_format_converter.py    # Main application file
└── Converted Video/             # Output folder (auto-created)
```

---

## ⚠️ Notes

- The `Converted Video/` folder is created automatically if it doesn't exist.
- Conversion time depends on the size and format of the input video.
- If `imageio_ffmpeg` is not installed, the program will exit with an installation prompt.

---

## 🔮 Future Improvements

- Add a progress bar during conversion
- Support batch conversion of multiple files at once
- Allow users to set custom output quality or resolution
- Add audio-only extraction (MP3, AAC)
- Build a full GUI to replace the CLI menu

---

## 👤 Author

**Seth**
- GitHub: [@SXTH2105](https://github.com/SXTH2105)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
