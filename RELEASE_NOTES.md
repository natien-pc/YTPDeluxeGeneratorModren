# YTP Deluxe Generator — Windows 8.1 Update (feature changes)

Release title:
YTP Deluxe Generator — Windows 8.1 Update

What changed
- Removed legacy beta key gating: Auto-Generate and batch features are now available without a beta key.
- Added explicit support for meme assets:
  - assets/memes/ (images)
  - assets/meme_sounds/ (audio)
- Improved FFmpeg discovery and notes for Windows 8.1.
- Updated GUI to remove beta-key UI and add meme asset/sound fields.
- Updated assets README to show the new folders and recommended small file sizes.
- Kept all legacy-friendly fallbacks (mpeg4 / libmp3lame) to help compatibility with older FFmpeg builds that still run on Windows 8.1.

Compatibility
- Target: Windows 8.1 with Python 3.x (recommended 3.6+), and a Windows FFmpeg build with ffmpeg.exe (ffplay.exe optional).
- Works with older / simpler FFmpeg builds by using sequential commands and codec fallbacks.

Files updated in this release
- main.py — GUI: removed beta key entry; added meme asset & meme sound fields; Auto-Generate unlocked.
- engine.py — removed beta-key check in auto_generate; added meme asset picking and meme_sound support.
- utils.py — removed beta-key helpers; improved asset scanning for memes and meme sounds.
- assets/README.txt — added meme folder guidelines and Windows 8.1 tips.
- run_windows81.bat — small launcher for Windows 8.1

Notes
- If you previously used beta_key.txt, you may remove it — it is no longer required.
- Auto-Generate can now be used directly from the GUI.
```
