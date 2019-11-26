import json
import string
import requests
from bs4 import BeautifulSoup
from wiki_scraping.utils import beautify_string


class Character:
    def __init__(self):
        self.__links = []
        self.base_url = 'https://awoiaf.westeros.org'
        self.__character_list()

    def __character_list(self):
        """
        Create a list of each character's ids
        for awioaf.westeros.org routing
        """

        # Request for get the characters' list
        req = requests.get(self.base_url + '/index.php/List_of_characters')

        # Parser for html page
        soup = BeautifulSoup(req.content, 'html.parser')

        # Isolate div 'mw-parser-output' from html page
        table = soup.find(name='div', attrs={'class': 'mw-parser-output'})

        # Get all list elements
        li_s = table.find_all(name='li')

        for li in li_s:
            self.__links.append(li.find(name='a').get('href')[11:])

    def get_characters(self):
        """
        Getter for character list
        """
        return self.__links

    def get_characters_description(self, character_id):
        """
        Get information about the character from wiki
        """
        character = {'id': character_id}

        # Request from web
        req = requests.get(self.base_url+'/index.php/'+character_id)
        soup = BeautifulSoup(req.content, 'html.parser')
        if req.status_code != 200:
            return None

        # Get name from header
        header = soup.find(name='h1', attrs={'id': 'firstHeading'})
        character['name'] = header.get_text()

        # Get table content
        table = soup.find(name='table', attrs={'class': 'infobox'})
        if table is None:
            return character

        tr_s = table.find_all(name='tr')
        for tr in tr_s:
            # Check if is a description field
            th = tr.find_all(name='th', attrs={'scope': 'row'})

            if len(th) > 0:
                # Field identifier
                id = th[0].get_text()

                # Check if there is a broken line (for multiple descriptions)
                br = tr.find_all(name='br')
                if len(br) > 0:
                    td = tr.find(name='td').get_text(strip=True, separator="--")
                    td = td.split("--")
                else:
                    td = tr.find(name='td').get_text()

                # Add raw description to dictionary
                character[id.lower()] = beautify_string(td)

        return character

    def get_characters_by_letter(self, letter):
        """
        Get a list of character by first letter
        """
        letter_list = []
        for character in self.get_characters():
            if character[0].lower() == letter.lower():
                letter_list.append(character)
        return letter_list


if __name__ == '__main__':
    characters = Character()

    # For all letters in alphabet
    for letter in string.ascii_lowercase:
        print('Get characters with first letter {}'.format(letter.upper()))
        desc = {}
        # For all characters starting with letter
        for ch in characters.get_characters_by_letter(letter):
            print(ch)
            desc[ch] = characters.get_characters_description(ch)
        file = open('character/Character-{}.json'.format(letter.upper()), 'w')
        file.write(json.dumps(desc, indent=4))
        file.close()
