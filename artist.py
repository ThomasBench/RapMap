from bs4 import BeautifulSoup  # parcourir la page
import requests as re  # Récup la page web
from typing import List, Set
import bs4
from driver import create_chrome_driver, create__tor_driver
from typing import List, Tuple
from selenium.webdriver.common.by import By
from time import sleep
from tqdm.notebook import tqdm
import pickle

# from classes import Artist, Song, Album


class Artist():
    def __init__(self, link, name):
        self.link = link
        self.name = name
        self.songs = dict()
        self.featurings = set()
    def __repr__(self):
        return f"Artist({self.name})"
    
    def __eq__(self, other: "Artist"):
        return (
            self.__class__ == other.__class__ and
            self.link == other.link and 
            self.name == other.name
        )
    def __hash__(self):
        return hash(self.link)
    def test(self):
        return self
    def update_songs(self):
        albums = artist_to_albums(self)
        for album in tqdm(albums):
            song_links, song_names = album_to_song_links(album)
            for i,link in enumerate(song_links):
                if song_names[i] not in self.songs:
                    song = Song(link,song_names[i], self, link_to_artists(link))
                    self.songs[song_names[i]] = song
                    if self in song.writers:
                        self.featurings.update(song.writers)

    def save(self):
        with open(f'./data/{self.name}.pickle', 'wb') as file:
            pickle.dump(self, file) 


class Song():
    def __init__(self, link: str, name: str, artist: Artist, writers: Set[Artist]):
        self.link = link
        self.artist = artist
        self.writers = writers
        self.name = name

    def __repr__(self):
        return f"Song(by = {self.artist}, name: {self.name})"
    def __eq__(self, other: "Song"):
        return (
            self.__class__ == other.__class__ and
            self.link == other.link
        )
    def __hash__(self):
        return hash(self.link)

class Album():
    def __init__(self, artist: Artist, name: str, link: str, year: int, song_list: List[str] = []):
        self.artist = artist
        self.name = name
        self.link = link
        self.songs = song_list
        self.year = year

    def __repr__(self):
        return f"Album(by {self.artist}, name: {self.name})"


def div_to_type(div: str) -> str:
    return div.find("div").text


def a_to_artist(a: bs4.element.Tag) -> Artist:
    artist_name = a.text
    artist_link = a["href"]
    return Artist(artist_link, artist_name)


def link_to_artists(lien: str) -> Set[Artist]:
    content = re.get(lien).text
    artists = set()
    filtered_content = BeautifulSoup(content).findAll(
        "div", class_="SongInfo__Credit-nekw6x-3")
    ecrit_par = [c for c in filtered_content if div_to_type(c) == "Written By"]
    if len(ecrit_par) <=0:
        return []

    for element in ecrit_par[0].findAll('a'):
        artists.add(a_to_artist(element))
    return artists




# DRIVER = create_chrome_driver()
# DRIVER.get("http://check.torproject.org")
