```text
Assets folder guidelines (updated for memes and Windows 8.1)

Create these subfolders inside the project assets/ folder:

assets/
  sounds/            <- old system sounds, beeps, error sounds (wav/mp3/ogg)
  meme_sounds/       <- meme-style short sounds and clip loops (wav/mp3)
  memes/             <- meme images/overlays (PNG/JPG/GIF)
  images/            <- generic images used for overlays or memes
  errors/            <- OS error dialog screenshots / stylized images
  adverts/           <- old overlay adverts / banners
  overlays_videos/   <- short overlay videos / animated GIF converted to short mp4

Suggested filenames:
  sounds/os_beep.wav
  meme_sounds/dj_loop.wav
  memes/meme_overlay.png
  images/meme_overlay.png
  errors/error_winxp.png
  adverts/advert_2009.png
  overlays_videos/overlay_loop_2009.mp4

Windows 8.1 tips:
- Use Python 3.6+ for best compatibility on Windows 8.1.
- Place a compatible ffmpeg.exe binary in the project folder or add the ffmpeg folder to PATH.
- Keep assets small (< a few MB) to speed up processing on modest hardware.

Usage:
- If GUI asset fields are empty, engine will auto-pick appropriate items from these folders.
- Do not include copyrighted OS images/sounds in public repos.
```