from youtubesearchpython import VideosSearch
from pytube import YouTube
import subprocess
import requests
import eyed3
import os
import yt_dlp
import io

class Download():
    def find_song(self, song_name, song_artists, use_lyrics = True, index = 0):
        song_string = song_name + ' by ' + ' '.join(song_artists)

        if use_lyrics:
            song_string = song_string + ' lyrics'

        search_results = VideosSearch(song_string, limit = 1)
        song_url = search_results.result()['result'][index]['id']
        return 'https://www.youtube.com/watch?v='+song_url

    # def download_song(self, song_url, download_path, song_name):
    #     # youtube = YouTube(song_url, use_oauth=True, allow_oauth_cache=True)
    #     # audio = youtube.streams.get_audio_only()
    #     # audio.download(download_path, song_name+'.mp4')
    #     # return audio.default_filename
    #     youtube = YouTube(song_url, use_oauth=True, allow_oauth_cache=True)
    #     audio = youtube.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
    #     # get_audio_only()
    #     # audio.download(download_path, song_name+'.mp4')
    #     return audio.default_filename

    # def download_song(self, song_url, download_path, song_name):
    #     if not os.path.exists(download_path):
    #         os.makedirs(download_path)

    #     try:
    #         yt = YouTube(song_url)
    #         audio_stream = yt.streams.filter(only_audio=True).first()
    #         mp4_file = os.path.join(download_path, f"{song_name}.mp4")
    #         audio_stream.download(output_path=download_path, filename=f"{song_name}.mp4")
    #         print(f"Downloaded and saved: {mp4_file}")
    #         self.convert_to_mp3(mp4_file)
    #         return f"{song_name}.mp3"
    #     except Exception as e:
    #         print(f"Error: {e}")
    #         return None

    # def convert_to_mp3(self, mp4_file):
    #     mp3_file = mp4_file.replace('.mp4', '.mp3')
    #     try:
    #         subprocess.call(['ffmpeg', '-y', '-i', mp4_file, mp3_file])
    #         os.remove(mp4_file)
    #         print(f"Converted {mp4_file} to {mp3_file}")
    #     except Exception as e:
    #         print(f"Error converting to mp3: {e}")

    # # def convert_to_mp3(self, song_location):
    # #     subprocess.call(['ffmpeg -y -i "' + song_location + '.mp4" "' + song_location + '.mp3"' ], shell=True)
    # #     os.remove(song_location + '.mp4')
    # # def add_metadata(self, mp3_file, song_name, song_artists, song_art):
    # #     # Use a library like eyeD3 or mutagen to add metadata
    # #     # Here’s a placeholder for adding metadata

    # #     try:
    # #         audiofile = eyed3.load(mp3_file)
    # #         if audiofile.tag is None:
    # #             audiofile.tag = eyed3.id3.Tag()
    # #             audiofile.tag.file_info = eyed3.id3.FileInfo(mp3_file)
    # #         audiofile.tag.artist = ', '.join(song_artists)
    # #         audiofile.tag.title = song_name
    # #         if song_art:
    # #             audiofile.tag.images.set(3, open(song_art, 'rb').read(), 'image/jpeg')
    # #         audiofile.tag.save()
    # #         print(f"Added metadata to {mp3_file}")
    # #     except Exception as e:
    # #         print(f"Error adding metadata: {e}")
    

    # def download_track(self, song_name, song_artists, song_art, download_path):
    #     print(song_name, song_artists)
    #     song_url = self.find_song(song_name, song_artists)
    #     self.download_song(song_url, download_path, song_name)
    #     song_location = download_path + '/' + song_name
    #     self.convert_to_mp3(song_location)
    #     # self.add_metadata(song_location + '.mp3', song_name, song_artists, song_art) 


#using yt_dlp library because pytube has a bug that doesn't allow downloading audio only
    def download_song(self, song_url, download_path, song_name):
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(download_path, f"{song_name}.mp3"),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([song_url])
            print(f"Downloaded and saved: {os.path.join(download_path, f'{song_name}.mp3')}")
            return f"{song_name}.mp3"
        except Exception as e:
            print(f"Error: {e}")
            return None

    # def convert_to_mp3(self, mp4_file):
    #     mp3_file = mp4_file.replace('.mp4', '.mp3')
    #     try:
    #         subprocess.call(['ffmpeg', '-y', '-i', mp4_file, mp3_file])
    #         os.remove(mp4_file)
    #         print(f"Converted {mp4_file} to {mp3_file}")
    #     except Exception as e:
    #         print(f"Error converting to mp3: {e}")
        
    def download_track(self, song_name, song_artists, song_art, download_path):
        print(f"Processing track: {song_name} by {', '.join(song_artists)}")
        song_url = self.find_song(song_name, song_artists)
        self.download_song(song_url, download_path, song_name)
        song_location = download_path + '/' + song_name
        # song_location = os.path.join(download_path, song_name)
        # self.convert_to_mp3(f"{song_location}.mp4")