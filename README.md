```markdown
# YTP Deluxe Generator — Windows Legacy Edition

YTP Deluxe Generator is a lightweight, legacy-friendly YouTube Poop (YTP) generator designed to run on older Windows systems (Windows 7 / 8.1 and legacy-era hardware). This repository contains a Beta series of the generator with a Tkinter GUI, FFmpeg-based effect engine, asset discovery, Auto-Generate batch mode, and an optional concatenation of generated outputs.

This README explains what the project does, how to install and run it on Windows 8.1, how to prepare assets, and how to use the key features (Preview, Preview2, Auto-Generate, and Concat).

---

## Features (summary)

- GUI (Tkinter) for selecting input/output and toggling effects.
- Per-effect toggles plus configurable probability and level.
- Implemented effects (or safe approximations):
  - Random sound overlay (audio mix)
  - Reverse clip (video & audio)
  - Speed up / slow down (setpts + atempo chain)
  - Chorus (aecho approximation)
  - Vibrato / pitch-bend (asetrate + atempo approximation)
  - Stutter loop
  - Earrape (volume boost)
  - Auto-tune placeholder (external tool integration required)
  - Dance / Squidward video transforms
  - Invert colors, Mirror mode, Sus effect
  - Rainbow / Meme overlay, Explosion spam, Frame shuffle
  - Sentence mixing / random clip shuffle / random cuts
- Auto-Generate (batch randomized outputs) — no beta key required.
- Concat generated outputs into a single file (fast concat with fallbacks to reencode).
- Preview (ffplay) and Preview2 (fast low-res sample).
- Asset discovery: assets/, including memes and meme sounds.
- Codec fallbacks for older FFmpeg builds (libx264/aac → mpeg4/libmp3lame).

---

## Requirements

- Windows 8.1 (32-bit or 64-bit)
- Python 3.6+ recommended (works with Python 3.6–3.11)
- FFmpeg Windows build with `ffmpeg.exe` (and optional `ffplay.exe`)
- Disk space for temporary files (working folder `ytp_temp` by default)

Notes:
- Place `ffmpeg.exe` (and `ffplay.exe` if available) in the project root or ensure the FFmpeg binary folder is on PATH.
- For very old or minimal FFmpeg builds, the engine includes codec and filter fallbacks but some effects may be unavailable.

---

## Quick install

1. Clone or extract this repository on the Windows 8.1 machine.
2. Install Python 3.6+ if not already installed. Make sure `python` is on PATH.
3. Download a compatible FFmpeg static build for Windows and copy `ffmpeg.exe` (and optionally `ffplay.exe`) into the project folder.
4. Prepare the assets folder (see next section).
5. Run:
   - double-click `run_windows81.bat` or
   - open a cmd window in the project folder and run:
     ```
     python main.py
     ```

---

## Assets folder layout

Create an `assets/` folder in the project root and add these recommended subfolders:

- assets/sounds/         — old system sounds, beeps (wav/mp3/ogg)
- assets/meme_sounds/    — meme-style short audio clips (wav/mp3)
- assets/memes/          — meme overlay images (png/jpg/gif)
- assets/images/         — generic images for overlays
- assets/errors/         — OS error images (keep license in mind)
- assets/adverts/        — overlay banners
- assets/overlays_videos/— short overlay mp4 loops

Keep assets small (a few MB each) for faster processing.

---

## Usage (GUI)

1. Launch the GUI (`main.py`).
2. Choose Input video and Output file.
3. Toggle effects from the quick list. For fine control click "Configure Effects" to set per-effect probability (0.0–1.0) and numeric level/parts.
4. Optionally set specific asset files (rainbow overlay, random sound, meme image, meme sound). If left blank the engine auto-picks assets from the `assets/` folders.
5. Use Preview 2 (6s low-res sample) for fast checking before a full render.
6. Click Generate to create a single YTP.
7. Use Auto Generate to produce multiple randomized YTPs. If the "Concat auto-generated outputs" option is selected, the app will attempt to join the generated files into a single output.

---

## Auto-Generate + Concat

- Auto-Generate creates N randomized YTPs with jittered probabilities/levels based on your base options.
- Concat option: check the "Concat auto-generated outputs" box and specify a concat filename (defaults to `ytp_concat.mp4` in the output folder). The engine will:
  - Generate each file individually.
  - Create a file list and attempt a fast concat (`ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp4`).
  - If fast concat fails (codec mismatch), it falls back to re-encoding the concatenated sequence (libx264/aac or mpeg4/libmp3lame).

Usage notes:
- Fast concat works best when generated files share identical codecs and parameters.
- Re-encoding is slower but more compatible across varied inputs.

---

## Preview & Preview2

- Preview: plays a generated file using `ffplay` (if present).
- Preview2: quickly creates a 6-second low-resolution, slightly processed sample using `-preset ultrafast` to test look and feel before a full render.

---

## Example manual FFmpeg commands

Reverse video + audio:
```
ffmpeg -y -i input.mp4 -vf reverse -af areverse out_reverse.mp4
```

Speed 2x:
```
ffmpeg -y -i input.mp4 -vf "setpts=0.5*PTS" -af "atempo=2.0" out_fast.mp4
```

Chorus (aecho approx):
```
ffmpeg -y -i input.mp4 -af "aecho=0.8:0.9:120|240:0.6|0.3" out_chorus.mp4
```

Overlay image:
```
ffmpeg -y -i input.mp4 -i overlay.png -filter_complex "overlay=10:10" -c:v libx264 -preset ultrafast -c:a copy out_overlay.mp4
```

Concat files (fast concat demuxer):
```
# create filelist.txt:
# file '/path/to/ytp_auto_001.mp4'
# file '/path/to/ytp_auto_002.mp4'
ffmpeg -y -f concat -safe 0 -i filelist.txt -c copy out_concat.mp4
```

If the concat copy fails, re-encode:
```
ffmpeg -y -f concat -safe 0 -i filelist.txt -c:v libx264 -preset veryfast -c:a aac out_concat_reencoded.mp4
```

---

## Troubleshooting

- "ffmpeg not found": ensure `ffmpeg.exe` is in the project folder or the FFmpeg folder is added to PATH. Run `ffmpeg -version` in a cmd window to verify.
- "Filter not found": your FFmpeg build may be too old. Try a different legacy build, update FFmpeg, or disable the effect.
- Slow performance: use Preview2 for testing, reduce resolution (`-vf "scale=640:-2"`), use `-preset ultrafast` or shorter clips.
- Temporary files: the engine writes temporary files to `ytp_temp` (or the system temp folder). Delete `ytp_temp` after successful runs to free space.

---

## Security & Safety

- Earrape mode is very loud. Test at low headphone/speaker volume.
- Do not redistribute copyrighted OS images/sounds without permission. Use public-domain or self-created assets.

---

## Development notes

- The engine builds FFmpeg commands conservatively (sequential calls) for compatibility with older builds.
- Auto-Generate randomizes options per output; you can tune the base configuration in the GUI before batch runs.
- Auto-tune is a placeholder: integrate an external autotune tool if desired.

---

## Files of interest

- main.py        — Tkinter GUI
- engine.py      — FFmpeg orchestration and effects
- utils.py       — helpers (ffmpeg detection, temp files, asset scanning)
- run_windows81.bat — convenience launcher for Windows 8.1
- assets/        — user-supplied asset folders as described above
- assets/README.txt — more asset usage tips

---

## License

This project skeleton is provided under the MIT license. FFmpeg is a third-party tool; follow FFmpeg licensing when redistributing binaries. Assets are user-supplied — check their licenses.

---

## Contact / Next steps

The repository README is ready and matches the Windows 8.1 update (memes support, removed beta gating, concat feature). The code examples and usage instructions are included above so you can get started quickly. If you want, I can also prepare a small sample assets ZIP, update the release notes to mention the concat feature, or add a minimal CLI-only script for batch operations on headless machines — I will proceed with whichever task you ask next.
```