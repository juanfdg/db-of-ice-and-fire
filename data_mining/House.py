import json
import requests
from bs4 import BeautifulSoup
from data_mining.utils import beautify_string


class House:
    def __init__(self):
        self.__links = []
        self.regions = {}
        self.base_url = 'https://awoiaf.westeros.org'

    def get_regions_links(self):
        # Request for get the westeros region description
        req = requests.get(self.base_url + '/index.php/Houses_of_Westeros')

        # Parser for html page
        soup = BeautifulSoup(req.content, 'html.parser')

        # Isolate a list of tables 'navbox'
        navboxs = soup.find_all(name='table', attrs={'class': 'navbox'})

        links = []
        for navbox in navboxs[:-1]:
            title = navbox.find_all(name='th', attrs={'class': 'navbox-title'})
            links.append(title[0].find(name='a').get('href'))

        return links

    def houses_by_region(self, region_link):
        # Request for get the westeros region description
        req = requests.get(self.base_url + region_link)

        # Parser for html page
        soup = BeautifulSoup(req.content, 'html.parser')

        # Isolate the div of houses for that region
        table = soup.find(name='table', attrs={'class': 'nowraplinks collapsible uncollapsed navbox-subgroup'})
        trs = table.find_all(name='tr')

        self.regions[region_link[26:]] = {}
        for tr in trs[1:]:
            elements = tr.find_all(name='li')
            if len(elements) > 0:
                label = tr.find(name='td').get_text()
                # print(label)
                house_link = []
                for e in elements:
                    # print('\t', e.find(name='a').get('href')[11:])
                    house_link.append(e.find(name='a').get('href')[11:])
                self.regions[region_link[26:]][label] = house_link

    def get_house_description(self, house_id):
        """
        Get information about the house from wiki
        """
        house = {'id': house_id}

        # Request from web
        req = requests.get(self.base_url + '/index.php/' + house_id)
        soup = BeautifulSoup(req.content, 'html.parser')
        if req.status_code != 200:
            return None

        # Get name from header
        header = soup.find(name='h1', attrs={'id': 'firstHeading'})
        house['name'] = header.get_text()

        # Get table content
        table = soup.find(name='table', attrs={'class': 'infobox'})
        if table is None:
            return house

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
                house[id.lower()] = beautify_string(td)

        return house


if __name__ == '__main__':
    houses = House()
    # Get all the regions houses
    for region in houses.get_regions_links():
        houses.houses_by_region(region)

    # Save the regions dictionary
    regions = open('region/Regions.json', 'w')
    regions.write(json.dumps(houses.regions, indent=4))
    regions.close()

    # For all regions in westeros
    for region in houses.regions.keys():
        print(region)
        desc = {}
        # For all levels in a regions
        for level in list(houses.regions[region].keys()):
            print('\t', level)
            # For all houses in a level
            for house_id in houses.regions[region][level]:
                print('\t\t', house_id)
                desc[house_id] = houses.get_house_description(house_id)
        file = open('region/Houses-of-{}.json'.format(region), 'w')
        file.write(json.dumps(desc, indent=4))
        file.close()
