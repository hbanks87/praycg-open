#!/usr/bin/env python3
"""
Download a CC-BY Sintel source file from Wikimedia Commons and create a 4-minute PRAYCG source excerpt.

Requires ffmpeg on PATH.

The direct source URL may change. If the download fails, manually download Sintel from:
  https://commons.wikimedia.org/wiki/File:Sintel_movie_-_Blender_Fondation.ogv
or
  https://durian.blender.org/download/

Then run this script with --source-file.
"""
from __future__ import annotations
import argparse, subprocess, urllib.request
from pathlib import Path

DEFAULT_URL = 'https://upload.wikimedia.org/wikipedia/commons/7/79/Sintel_movie_-_Blender_Fondation.ogv'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out-dir', default='sintel_praycg_source')
    ap.add_argument('--source-file', default='')
    ap.add_argument('--url', default=DEFAULT_URL)
    ap.add_argument('--start', default='00:05:10', help='excerpt start time in source film')
    ap.add_argument('--duration', default='00:04:00')
    ap.add_argument('--width', default='854')
    args = ap.parse_args()
    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    source = Path(args.source_file) if args.source_file else out / 'Sintel_source.ogv'
    if not source.exists():
        print('Downloading:', args.url)
        urllib.request.urlretrieve(args.url, source)
    dest = out / 'sintel_praycg_source_excerpt_4min.mp4'
    cmd = [
        'ffmpeg','-y','-ss',args.start,'-i',str(source),'-t',args.duration,
        '-vf',f'scale={args.width}:-2', '-c:v','libx264','-preset','veryfast','-crf','23',
        '-c:a','aac','-b:a','128k', str(dest)
    ]
    print('Running:', ' '.join(cmd))
    subprocess.check_call(cmd)
    (out/'ATTRIBUTION_SINTEL_CC_BY_3_0.txt').write_text(
        'Sintel © copyright Blender Foundation | www.sintel.org / durian.blender.org\n'
        'Licensed under Creative Commons Attribution 3.0 Unported.\n'
        'This file is a transformed PRAYCG source excerpt for protocol testing.\n', encoding='utf-8')
    print('Wrote', dest)

if __name__ == '__main__':
    main()
