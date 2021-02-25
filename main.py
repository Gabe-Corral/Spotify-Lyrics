import os
import time
import dbus
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from about import About

class SpotifyLyrics:

    def __init__(self):
        self.base_url = "https://genius.com/"
        self.artist_song = self.get_song_info()
        self.lyrics = self.scrape_lyrics()
        self.create_gui()

    def get_song_info(self):
        """returns the artist and song name in an array"""
        session_bus = dbus.SessionBus()
        spotify_bus = session_bus.get_object(
            "org.mpris.MediaPlayer2.spotify",
            "/org/mpris/MediaPlayer2"
        )

        spotify_metadata = dbus.Interface(
            spotify_bus,
            "org.freedesktop.DBus.Properties"
            ).Get(
                "org.mpris.MediaPlayer2.Player",
                "Metadata"
                )
        return [
            str(spotify_metadata['xesam:artist'][0].title()),
            str(spotify_metadata['xesam:title'])]

    def scrape_lyrics(self):
        """Returns lyrics scraped from genius.com"""
        song = self.artist_song[1].split(" ")
        artist = self.artist_song[0].split(" ")
        self.song = "-".join(song)
        self.artist = "-".join(artist)

        url = self.base_url + self.artist + "-" + self.song + "-" + "lyrics"
        self.current_url = url

        page = requests.get(url)
        html = BeautifulSoup(page.text, "html.parser")
        lyrics = html.find("div", class_="lyrics").get_text()
        return lyrics

    def create_gui(self):
        """Creates the gui using tkinter"""
        self.root = tk.Tk()
        self.root.wm_title("Spotify Lyrics")
        self.root.configure(bg="#586e75")
        self.root.geometry("800x800")

        self.create_scrollbar()

        self.create_labels_buttons()

        tk.mainloop()

    def create_scrollbar(self):
        """Creates a scrollbar to ensure enough room to view lyrics"""
        self.wrapper = tk.LabelFrame(self.root)
        self.canvas = tk.Canvas(self.wrapper, width=500)
        self.canvas.pack(side=tk.LEFT, fill="both")
        self.y_scroll = tk.Scrollbar(self.wrapper, orient="vertical",
        command=self.canvas.yview)
        self.y_scroll.pack(side=tk.RIGHT, fill="both")
        self.frame = tk.Frame(self.canvas)
        self.canvas.configure(yscrollcommand=self.y_scroll.set, bg='#586e75')
        self.canvas.bind("<Configure>",
        lambda e: self.canvas.configure(scrollregion = self.canvas.bbox('all')))
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.wrapper.pack(fill="both", side="left")

    def refresh_lyrics(self):
        """Refreshes lables, buttons, etc"""
        self.artist_song = self.get_song_info()
        self.lyrics = self.scrape_lyrics()

        self.destroy_all_widgets()
        self.create_scrollbar()

        self.create_labels_buttons()

    def destroy_all_widgets(self):
        """Removes all labels, buttons, etc"""
        children = self.root.winfo_children()
        for child in children:
            child.destroy()

    def create_labels_buttons(self):
        """Creates lyrics label, and necessary buttons"""
        self.lyrics_label = tk.Label(self.frame, text=self.lyrics,
        bg="#586e75", fg="#073642")
        self.lyrics_label.pack()

        self.refresh_button = tk.Button(self.root, text="Refresh",
        command=self.refresh_lyrics, bg='#586e75', fg="#073642")
        self.refresh_button.pack(fill="x")

        self.about_song_button = tk.Button(self.root, text="About Song",
        command=self.about_song, bg='#586e75', fg="#073642")
        self.about_song_button.pack(fill="x")

    def about_song(self):
        """Scrapes info about the song"""
        url = self.current_url
        page = requests.get(url)
        html = BeautifulSoup(page.text, "html.parser")
        about_song = html.find("div",
        class_="column_layout-column_span-initial_content").get_text()
        About(self.root, tk.Toplevel(self.root), about_song)

if __name__=="__main__":
    SpotifyLyrics()
