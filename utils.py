# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import tempfile
import shutil
import subprocess

def which(exe_name):
    paths = os.environ.get('PATH', '').split(os.pathsep)
    exts = ['']
    if os.name == 'nt':
        pathext = os.environ.get('PATHEXT', '.EXE;.BAT;.CMD')
        exts = pathext.split(';')
    for p in paths:
        candidate = os.path.join(p, exe_name)
        for e in exts:
            full = candidate + e
            if os.path.exists(full) and os.path.isfile(full):
                return full
    return None

def find_ffmpeg():
    ffmpeg = which('ffmpeg') or which('ffmpeg.exe')
    ffplay = which('ffplay') or which('ffplay.exe')
    cur = os.getcwd()
    # Accept ffmpeg.exe in current dir (common on Windows)
    if not ffmpeg and os.path.exists(os.path.join(cur, 'ffmpeg.exe')):
        ffmpeg = os.path.join(cur, 'ffmpeg.exe')
    if not ffplay and os.path.exists(os.path.join(cur, 'ffplay.exe')):
        ffplay = os.path.join(cur, 'ffplay.exe')
    return ffmpeg, ffplay

def safe_tempfile(suffix='', prefix='ytp_', dir=None):
    fd, path = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=dir)
    try:
        os.close(fd)
    except Exception:
        pass
    return path

def temp_filename_for(ext):
    if not ext.startswith('.'):
        ext = '.' + ext
    return safe_tempfile(suffix=ext)

def rm_f(path):
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.exists(path):
            os.remove(path)
    except Exception:
        pass

def run_command(cmd, shell=False):
    try:
        if isinstance(cmd, (list, tuple)):
            print("Running:", " ".join(cmd))
        else:
            print("Running:", cmd)
        p = subprocess.Popen(cmd, shell=shell)
        p.communicate()
        return p.returncode == 0
    except Exception as e:
        print("Command failed:", e)
        return False

# Assets helpers (now includes memes and meme_sounds)
def find_assets_dir(default='assets'):
    if os.path.isdir(default):
        return default
    return None

def list_asset_files(assets_dir):
    files = {}
    if not assets_dir:
        return files
    try:
        for root, _, filenames in os.walk(assets_dir):
            for fn in filenames:
                path = os.path.join(root, fn)
                ext = os.path.splitext(fn)[1].lower()
                files.setdefault(ext, []).append(path)
    except Exception:
        pass
    return files