import requests
import spotipy
import constants
import os
import time
from pynput.keyboard import Key, Controller
import subprocess

class spotifree(object):
    
    def __init__(self):
        self.client_id = constants.CLIENT_ID
        self.client_secret = constants.CLIENT_SECRET
        self.redirect_uri = constants.REDIRECT_URI
        self.username = constants.USERNAME
        self.scope = constants.SCOPE
        self.token = self.setup_spotify()
        self.keyboard = Controller()
        self.path = constants.PATH
        
    def close_spotify(self):
        if os.name == "nt":
            os.system("taskkill /f /im spotify.exe")
            
    def setup_spotify(self):
        token = spotipy.util.prompt_for_user_token(self.username, self.scope, self.client_id,self.client_secret, self.redirect_uri)
        return spotipy.Spotify(auth=token)
    
    def play(self):
        self.keyboard.press(Key.media_play_pause)
    
    def restart_spotify(self):
        self.close_spotify()
        self.start_spotify()
        time.sleep(5)
        self.next_track()
        
    def next_track(self):
        self.keyboard.press(Key.media_next)
        self.keyboard.release(Key.media_next)
        
    def start_spotify(self):
        SW_HIDE = 0
        info = subprocess.STARTUPINFO()
        info.dwFlags = subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = SW_HIDE
        subprocess.Popen(self.path, startupinfo=info)
        
  
    def get_current_track(self):
        current_track = None
        last_track = ""
        """
        Get the current track playing on Spotify
        """
        print('Just hunting for ads :D')
        while True:
            try:
                    current_track = self.token.current_user_playing_track()   
                    if current_track:
                        if current_track['currently_playing_type'] == 'ad':
                            self.restart_spotify()
                            print('Ad skipped')
                            continue  
                        
                    if current_track['item']['name'] != last_track: 
                            wait = current_track["item"]['duration_ms'] - current_track['progress_ms']
                            time.sleep(wait/1000 - 8)
                            last_track = current_track['item']['name']
            except Exception as e:
                print(e)
                self.play()
                time.sleep(10)
        
if __name__ == '__main__':
    spotifree = spotifree()
    spotifree.get_current_track()