# 🎬 Video Format Converter

A Python desktop application that converts video files between popular formats **and lets you control the frame rate** — using a GUI file picker and FFmpeg under the hood. No command-line knowledge required.

---

## 📋 Overview

This tool lets you select any video file through a graphical file dialog, analyze its current format and frame rate, choose a target format and FPS, then automatically convert and save the output to a dedicated `Converted Video/` folder. It uses `imageio_ffmpeg` to bundle FFmpeg, so no manual FFmpeg installation is needed.

---

## ✨ Features

- 🖱️ **GUI file picker** — browse and select your video file visually via Tkinter
- 🔍 **File analysis** — displays the selected file's name, format, and **detected frame rate** before converting
- 🎞️ **10 output format options** across MP4, MOV, MKV, AVI, WMV, and FLV groups
- 🔁 **Keep original format** — option `0` lets you re-encode without changing the container
- 🎛️ **Frame rate control** — choose from presets (24, 30, 60, 120 fps) or enter a **custom FPS**
- 🏷️ **Smart file naming** — output files are named as `originalname_FORMAT_FPSfps.ext`
- 📂 **Auto-saves** converted files to a `Converted Video/` folder
- ⚡ **Bundled FFmpeg** via `imageio_ffmpeg` — no external FFmpeg installation required

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
- **Tkinter** — for the GUI file picker dialog
- **imageio_ffmpeg** — for bundled FFmpeg binary
- **subprocess** — to run FFmpeg and detect frame rate from metadata
- **re** — to parse FPS from FFmpeg's stderr output
- **os** — for file path and directory management

---

## 🚀 Getting Started

### Prerequisites

Install the required library:

```bash
pip install imageio_ffmpeg
```

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

1. A file dialog opens — select your video file.
2. The app displays the file's name, detected format, and **current frame rate**.
3. Choose an output format from the menu (0–9), including option `0` to keep the original.
4. Choose a target frame rate (0–5), including a custom FPS option.
5. FFmpeg runs the conversion with the specified format and FPS settings.
6. The converted file is saved to the `Converted Video/` folder, named as:
   - `originalname_FORMAT_FPSfps.ext` (if FPS was changed)
   - `originalname_FORMAT.ext` (if original FPS was kept)

---

## 🗂️ Output Example

```
Converted Video/
├── myvideo_MP4_60fps.mp4
├── myvideo_MKV.mkv
└── clip_AVI_30fps.avi
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

## 📝 Changelog

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

- The `Converted Video/` folder is created automatically if it doesn't exist.
- Conversion time depends on the size, format, and frame rate of the input video.
- Frame rate is detected by parsing FFmpeg's stderr metadata output using regex.
- If `imageio_ffmpeg` is not installed, the program will exit with an installation prompt.

---

## 🔮 Future Improvements

- Add a progress bar during conversion
- Support batch conversion of multiple files at once
- Allow custom output resolution or quality settings
- Add audio-only extraction (MP3, AAC)
- Build a full GUI to replace the CLI menu

---

## 👤 Author

**Seth**
- GitHub: [@SXTH2105](https://github.com/SXTH2105)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
