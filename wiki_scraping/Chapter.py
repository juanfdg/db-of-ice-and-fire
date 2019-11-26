import re
import json
import string
import requests
from bs4 import BeautifulSoup
from wiki_scraping.utils import beautify_string


class Chapter:
    def __init__(self):
        self.base_url = 'https://awoiaf.westeros.org'
        self.chapters = []

    def chapter_list(self):
        """
        Create a list of chapter
        for awioaf.westeros.org routing
        """

        # Request for get the characters' list
        req = requests.get(self.base_url + '/index.php/Chapters')

        # Parser for html page
        soup = BeautifulSoup(req.content, 'html.parser')

        # Isolate div 'mw-parser-output' from html page
        divs = soup.find_all(name='div', attrs={'style': 'background:#F2EEE6;color:#333;border:6px double white;margin:-3px -3px 2px -3px;padding:8px 12px;'})

        for div in divs[:5]:
            book_id = div.find(name='a').get('href')[11:]
            book_name = div.find(name='h2').get_text()
            print(book_name)

            for li in div.find_all(name='li')[:-1]:
                chapter_id = li.find(name='a').get('href')[11:]
                chapter_name = li.get_text()
                print('\t', chapter_id)

                pov, character = self.get_character_by_chapter(chapter_id)

                self.chapters.append({'book_id': book_id,
                                      'book_name': book_name,
                                      'chapter_id': chapter_id,
                                      'chapter_name': chapter_name,
                                      'pov': pov,
                                      'character': character})

    def get_character_by_chapter(self, chapter_id):
        """
        Given an chapter id
        get the character list of that chapter
        """
        # Request for get the characters' list
        req = requests.get(self.base_url + '/index.php/' + chapter_id)
        # Parser for html page
        soup = BeautifulSoup(req.content, 'html.parser')
        content = soup.find(name='div', attrs={'class': 'mw-parser-output'})

        pov, character = None, []

        # Search for POV
        infobox = content.find(name='table', attrs={'class': 'infobox'})
        for tr in infobox.find_all(name='tr'):
            th = tr.find(name='th')
            if th is not None:
                if th.get_text() == 'POV':
                    a = tr.find(name='a')
                    pov = a.get('href')[11:]
                    break

        # Search for another character
        wikitable = content.find(name='table', attrs={'class': 'wikitable'})
        # If wikitable exists in
        if wikitable is not None:
            for a in wikitable.find_all(name='a'):
                character.append(a.get('href')[11:])
        else:
            for h2 in content.find_all(name='h2'):
                if re.search(r'haracter', h2.get_text()):
                    character_div = h2.find_next_sibling()
                    for a in character_div.find_all(name='a'):
                        character.append(a.get('href')[11:])
                    break

        return pov, character


if __name__ == '__main__':
    chapters = Chapter()
    chapters.chapter_list()

    file = open('chapter/chapter.json', 'w')
    file.write(json.dumps(chapters.chapters, indent=4))
    file.close()
