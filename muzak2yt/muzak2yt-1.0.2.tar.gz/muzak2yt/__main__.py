import os
import argparse
import subprocess
from pathlib import Path
import re
import json
import fleep
from mutagen.easyid3 import *
from youtube_uploader_selenium import YouTubeUploader

album = []
parsearger = argparse.ArgumentParser(prog='muzak2yt',
                                    usage='%(prog)s [options]',
                                    description='Convert to mp4 and upload to YouTube')

parsearger.add_argument("-nu", "--noup", help="Not upload to YouTube, only convert to MP4",  action="store_true")
args = parsearger.parse_args()


dir = Path.cwd()
if os.path.isfile('image.png'):
    for file in os.scandir(dir):
        readfile = open(file, "rb")
        info = fleep.get(readfile.read(128))
        if (info.type_matches('audio')) and file.is_file():
            audio = EasyID3(file.path)
            audio_info = {}

            filtre = {"album", "title", "artist", "tracknumber", "date"}
            for tag in audio:
                if tag in filtre:
                    audio_info[tag] = audio[tag]
                album.append(audio_info)
            video_filename = ""
            video_filename = str(audio["album"]).strip(
                '[\']') + " - " + str(audio["title"]).strip('[\']')
            invalid = '<>:"/\|?*'
            for char in invalid:
                video_filename = video_filename.replace(char, '-')
            video_filename += ".mp4"
            print(video_filename)
            subprocess.call(['ffmpeg', '-n',  '-framerate',  '3', '-loop', '1',  '-i', 'image.png',
                             '-i', file.name, '-shortest', '-movflags', 'faststart', '-c:v', 'libx264', '-profile:v', 'high',
                             '-bf', '2', '-g', '5', '-crf', '18', '-pix_fmt', 'yuv420p', 
                             '-c:a', 'aac', '-ac', '2', '-ar', '48000', '-b:a', '320k', video_filename])
            video_path = video_filename
            title = str(audio["album"]).strip('[\']') + " - " +  str(audio["title"]).strip('[\']')
            metadata = {
                "title":  title,
                "description": "Album: " + str(audio["album"]).strip('[\']') + "\nArtist(s): " + str(audio["artist"]).strip('[\']').replace("\"", "")
            }
            metadata_path = 'metadata.json'
            with open(metadata_path, 'w') as outfile:
                json.dump(metadata, outfile)
            if not args.noup:
                uploader = YouTubeUploader(video_path, metadata_path)
                was_video_uploaded, video_id = uploader.upload()
                assert was_video_uploaded

else:
    print("no image.png file found !")
