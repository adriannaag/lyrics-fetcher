import requests
import sys

from bs4 import BeautifulSoup


class Song:
    def __init__(self, title, author):
        self.title = title.replace(" ", "_")
        self.author = author.replace(" ", "_")

BASE_URL = 'https://www.tekstowo.pl/piosenka,'

def tekstowo_adress(song: Song) -> str:
    return f"{BASE_URL}{song.author},{song.title}"
    
def fetch_tekstowo_page(song: Song):
    addr = tekstowo_adress(song)
    return requests.get(addr)

LYRICS_FOOTER = """
Historia edycji tekstu

"""
def parse_lyrics(source):
    soup = BeautifulSoup(source, features="html.parser")
    lyrics_div = soup.find("div", {"id" : "songText"})
    if lyrics_div is None:
        raise ValueError("there is no song div")
    lyrics = lyrics_div.get_text()
    lyrics = lyrics[:-len(LYRICS_FOOTER)]
    lyrics = lyrics.strip()
    return lyrics

def get_title_and_name():
    print("Title of the song:")
    title = input()
    print("Author of the song:")
    name = input()
    print()
    return title, name

def main():
    title, name = get_title_and_name()
    song = Song(title, name)
    resp = fetch_tekstowo_page(song)
    if not resp.ok:
        print(f"Could not download lyrics. Status code: {resp.status_code}")
        sys.exit(1)
    try:
        lyrics = parse_lyrics(resp.text)
    except ValueError:
        print("Could not parse lyrics")
        sys.exit(2)
    print(lyrics)

if __name__ == '__main__':
    main()
