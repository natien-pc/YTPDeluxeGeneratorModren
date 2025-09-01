# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import random
import re
import shutil
import tempfile
from utils import find_ffmpeg, temp_filename_for, run_command, rm_f, find_assets_dir, list_asset_files

class YTPEngine(object):
    def __init__(self, ffmpeg_path=None, ffplay_path=None, work_dir=None):
        ffmpeg, ffplay = find_ffmpeg()
        self.ffmpeg = ffmpeg_path or ffmpeg
        self.ffplay = ffplay_path or ffplay
        if not self.ffmpeg:
            raise EnvironmentError("ffmpeg not found. Place ffmpeg.exe on PATH or next to script.")
        if not work_dir:
            work_dir = os.path.join(os.getcwd(), 'ytp_temp')
        self.work_dir = work_dir
        if not os.path.exists(self.work_dir):
            os.makedirs(self.work_dir)
        self.assets_dir = find_assets_dir()
        self.asset_index = list_asset_files(self.assets_dir) if self.assets_dir else {}

    def cleanup(self):
        rm_f(self.work_dir)

    def _pick_asset(self, exts):
        if not self.asset_index:
            return None
        for e in exts:
            lst = self.asset_index.get(e)
            if lst:
                return random.choice(lst)
        for k, v in self.asset_index.items():
            if v:
                return random.choice(v)
        return None

    def _probe_duration(self, path):
        try:
            cmd = [self.ffmpeg, '-i', path]
            p = __import__('subprocess').Popen(cmd, stdout=__import__('subprocess').PIPE, stderr=__import__('subprocess').PIPE)
            out, err = p.communicate()
            text = (err or b'').decode('utf-8', errors='ignore') + (out or b'').decode('utf-8', errors='ignore')
            m = re.search(r'Duration:\s*(\d+):(\d+):(\d+\.\d+)', text)
            if m:
                h, mm, ss = m.groups()
                return int(h)*3600 + int(mm)*60 + float(ss)
        except Exception:
            pass
        return 0.0

    def generate(self, input_video, output_path, options):
        """
        Generate a single YTP file from input_video -> output_path using options.
        Returns path to the generated file (output_path).
        """
        cur = input_video

        if options.get('sentence_mix', {}).get('enabled'):
            cur = self._sentence_mix(cur, options.get('sentence_mix', {}))

        if options.get('mode_2009'):
            cur = self._mode_2009(cur, options)
        if options.get('mode_2012'):
            cur = self._mode_2012(cur, options)

        order = ['reverse','speed','stutter','earrape','chorus','vibrato','sus','invert','mirror','dance','rainbow','explosion','frame_shuffle','meme','random_sound','meme_sound']
        for eff in order:
            cfg = options.get(eff, {})
            if not cfg:
                continue
            enabled = cfg.get('enabled', False)
            prob = float(cfg.get('prob', 1.0)) if 'prob' in cfg else 1.0
            if enabled and random.random() <= prob:
                try:
                    if eff == 'reverse':
                        cur = self._reverse(cur)
                    elif eff == 'speed':
                        cur = self._change_speed(cur, cfg.get('level', 1.0))
                    elif eff == 'stutter':
                        cur = self._stutter(cur, cfg.get('level', 2))
                    elif eff == 'earrape':
                        cur = self._earrape(cur, cfg.get('level', 16.0))
                    elif eff == 'chorus':
                        cur = self._chorus(cur, cfg.get('level', 0.6))
                    elif eff == 'vibrato':
                        cur = self._vibrato(cur, cfg.get('level', 1.03))
                    elif eff == 'sus':
                        cur = self._sus_effect(cur, cfg.get('level', 1.1))
                    elif eff == 'invert':
                        cur = self._invert_colors(cur)
                    elif eff == 'mirror':
                        cur = self._mirror(cur)
                    elif eff == 'dance':
                        cur = self._dance_mode(cur)
                    elif eff == 'rainbow':
                        asset = cfg.get('asset') or self._pick_asset(['.png','.gif','.jpg'])
                        if asset:
                            cur = self._overlay_image(cur, asset, x=cfg.get('x',0), y=cfg.get('y',0), opacity=cfg.get('opacity',0.9))
                    elif eff == 'explosion':
                        asset = cfg.get('asset') or self._pick_asset(['.png','.gif','.jpg'])
                        if asset:
                            cur = self._explosion_spam(cur, asset, count=cfg.get('count',4))
                    elif eff == 'frame_shuffle':
                        cur = self._frame_shuffle(cur, cfg.get('level',8))
                    elif eff == 'meme':
                        img = cfg.get('image') or self._pick_asset(['.png','.jpg','.gif'])
                        if img:
                            cur = self._overlay_image(cur, img, x='(main_w-overlay_w)/2', y='(main_h-overlay_h)-10')
                    elif eff == 'random_sound':
                        audio = cfg.get('asset') or self._pick_asset(['.wav','.mp3','.ogg','.aac'])
                        if audio:
                            cur = self._add_random_sound(cur, audio, cfg.get('count',3))
                    elif eff == 'meme_sound':
                        audio = cfg.get('asset') or self._pick_asset(['.wav','.mp3'])
                        if audio:
                            cur = self._add_random_sound(cur, audio, cfg.get('count',1))
                except Exception as e:
                    print("Effect", eff, "failed:", e)

        # final encode with fallback. cur may already be a temp file.
        out = output_path
        final_cmd = [self.ffmpeg, '-y', '-i', cur, '-c:v', 'libx264', '-preset', 'veryfast', '-c:a', 'aac', '-b:a', '192k', out]
        if not run_command(final_cmd):
            final_cmd2 = [self.ffmpeg, '-y', '-i', cur, '-c:v', 'mpeg4', '-qscale:v', '5', '-c:a', 'libmp3lame', '-b:a', '192k', out]
            run_command(final_cmd2)
        return out

    def auto_generate(self, input_video, out_dir, base_options, count=3, concat_output=None):
        """
        Generate multiple YTPs. If concat_output is provided (full path), try to concat
        generated files into that single file at the end.
        Returns a list of generated file paths. If concat_output was produced, it is appended to the list.
        """
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        generated = []
        for i in range(1, int(count) + 1):
            opts = self._randomize_options(base_options)
            out_path = os.path.join(out_dir, 'ytp_auto_%03d.mp4' % (i,))
            print("Auto-generate #%d -> %s" % (i, out_path))
            self.generate(input_video, out_path, opts)
            generated.append(out_path)

        # If requested, concatenate generated outputs into a single file
        if concat_output:
            try:
                print("Concatenating %d files into %s" % (len(generated), concat_output))
                ok = self.concat_videos(generated, concat_output)
                if ok:
                    generated.append(concat_output)
                else:
                    print("Concatenation failed; check ffmpeg output.")
            except Exception as e:
                print("Concat step failed:", e)
        return generated

    def concat_videos(self, file_list, out_path):
        """
        Concatenate videos using ffmpeg concat demuxer (fast copy). If that fails,
        fallback to re-encoding a concatenated stream.
        Returns True if output produced.
        """
        if not file_list:
            print("No files to concat.")
            return False

        txtlist = temp_filename_for('.txt')
        try:
            with open(txtlist, 'w') as f:
                for p in file_list:
                    # ffmpeg concat demuxer requires paths possibly escaped; safe=0 allows absolute paths
                    f.write("file '%s'\n" % p.replace("'", "'\\''"))
            # First try fast concat (works when codecs/parameters match)
            cmd = [self.ffmpeg, '-y', '-f', 'concat', '-safe', '0', '-i', txtlist, '-c', 'copy', out_path]
            if run_command(cmd):
                return True
            # Fallback: re-encode concatenated list (more compatible, slower)
            cmd2 = [self.ffmpeg, '-y', '-f', 'concat', '-safe', '0', '-i', txtlist, '-c:v', 'libx264', '-preset', 'veryfast', '-c:a', 'aac', '-b:a', '192k', out_path]
            if run_command(cmd2):
                return True
            # Older ffmpeg builds maybe need mpeg4/mp3 fallback
            cmd3 = [self.ffmpeg, '-y', '-f', 'concat', '-safe', '0', '-i', txtlist, '-c:v', 'mpeg4', '-qscale:v', '5', '-c:a', 'libmp3lame', '-b:a', '192k', out_path]
            if run_command(cmd3):
                return True
            return False
        finally:
            rm_f(txtlist)

    def preview(self, output_file):
        if self.ffplay:
            cmd = [self.ffplay, '-autoexit', output_file]
            run_command(cmd)
        else:
            print("ffplay not found. Open the file manually:", output_file)

    def preview2(self, input_path, seconds=6):
        tmp = temp_filename_for('.mp4')
        try:
            vf = "scale=480:-2,format=yuv420p,eq=contrast=1.05:brightness=0.01:saturation=1.2"
            af = "volume=1.0"
            cmd = [self.ffmpeg, '-y', '-t', str(seconds), '-i', input_path, '-vf', vf, '-af', af, '-c:v', 'libx264', '-preset', 'ultrafast', tmp]
            if not run_command(cmd):
                cmd2 = [self.ffmpeg, '-y', '-t', str(seconds), '-i', input_path, '-vf', vf, '-af', af, '-c:v', 'mpeg4', '-qscale:v', '6', tmp]
                run_command(cmd2)
            self.preview(tmp)
        finally:
            rm_f(tmp)

    # ... remaining effect implementations unchanged ...
    # For brevity the rest of effect methods (_sentence_mix, _reverse, etc.)
    # are assumed unchanged from the prior engine implementation and remain here.