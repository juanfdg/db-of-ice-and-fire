import os
import glob
import json
import pandas as pd

from collections import defaultdict

import wiki_scraping.queries as queries

# Data base path
base_path = os.getcwd()

# Characters data
characters = dict()
characters_name_to_id = dict()
parents = dict()
character_cultures = []
cultures = set()
aliases = []
titles = []
allegiances = []
lineages = []

for file in glob.glob(base_path + '/filter/character/Character-*.json'):
    for char in json.load(open(file, 'r')).values():
        born = char.get("born")
        death = char.get("died")

        # Find places of birth and death
        place_birth = None
        if born:
            if born.strip().startswith("At "):
                place_birth = born[3:]
            else:
                place_birth_idx = born.find(", at ")
                if place_birth_idx > 0:
                    place_birth = born[place_birth_idx+5:]

        place_death = None
        if death:
            if death.strip().startswith("At "):
                place_birth = death[3:]
            else:
                place_death_idx = death.find(", at")
                if place_death_idx > 0:
                    place_death = death[place_death_idx+5:]

        characters[char["id"]] = {
            "id_char": char["id"],
            "name_char": char["name"],
            "place_birth": place_birth,
            "place_death": place_death,
            "mother": char.get("mother"),
            "father": char.get("father"),
        }

        # Characters name to id map
        characters_name_to_id[char["name"]] = char["id"]

        # Culture of character, if present
        culture = char.get("culture")
        if culture:
            if isinstance(culture, list):
                for c in culture:
                    character_cultures.append({
                        "character": char["id"],
                        "culture": c
                    })
                    cultures.add(c)
            else:
                character_cultures.append({
                    "character": char["id"],
                    "culture": culture
                })
                cultures.add(culture)

        # Aliases and titles of character, if present
        character_alias = char.get("alias")
        if character_alias:
            if isinstance(character_alias, list):
                for a in character_alias:
                    aliases.append({
                        "character": char["id"],
                        "alias": a
                    })
            else:
                aliases.append({
                    "character": char["id"],
                    "alias": character_alias
                })

        character_title = char.get("titles")
        if character_title:
            if isinstance(character_title, list):
                for t in character_title:
                    titles.append({
                        "character": char["id"],
                        "title": t
                    })
            else:
                titles.append({
                    "character": char["id"],
                    "title": character_title
                })

        # Allegiances of character, if present
        character_allegiance = char.get("allegiance")
        if character_allegiance:
            if isinstance(character_allegiance, list):
                for a in character_allegiance:
                    allegiances.append({
                        "character": char["id"],
                        "house": a
                    })
            else:
                allegiances.append({
                    "character": char["id"],
                    "house": character_allegiance
                })

        # Store parents names as tuple (father, mother) for later processing
        parents[char["id"]] = (char.get("father"), char.get("mother"))


def add_lineage(parent, child):
    if isinstance(parent, list):
        for p in parent:
            if p in characters_name_to_id:
                lineages.append({
                    "parent": characters_name_to_id[p],
                    "child": child
                })
    else:
        if parent and parent in characters_name_to_id:
            lineages.append({
                "parent": characters_name_to_id[parent],
                "child": child
            })


# Lineages with parent name translated to id
for child, (father, mother) in parents.items():
    add_lineage(father, child)
    add_lineage(mother, child)

# Houses data
regions = []
region_houses = defaultdict(dict)
houses = defaultdict(dict)
houses_name_to_id = dict()
house_lords = set()

file = base_path + '/region/Regions.json'
for region, houses_of_region in json.load(open(file, 'r')).items():
    regions.append({
        "region_name": region,
    })

    for house_type, houses_by_type in houses_of_region.items():
        for h in houses_by_type:
            region_houses[(h, region)]["house"] = h
            region_houses[(h, region)]["region"] = region
            if house_type == "Royal Houses":
                region_houses[(h, region)]["is_royal"] = True
            elif house_type == "Great Houses":
                region_houses[(h, region)]["is_great"] = True
            elif house_type == "Noble Houses":
                region_houses[(h, region)]["is_noble"] = True
            elif house_type == "Exiled Houses":
                region_houses[(h, region)]["is_exiled"] = True
            elif house_type == "Extinct Houses":
                region_houses[(h, region)]["is_extinct"] = True
            elif house_type == "Deposed":
                region_houses[(h, region)]["is_deposed"] = True
            elif house_type == "Landed Knights":
                region_houses[(h, region)]["is_landed_knight"] = True

for rh in region_houses.values():
    if "is_royal" not in rh:
        rh["is_royal"] = False
    if "is_great" not in rh:
        rh["is_great"] = False
    if "is_noble" not in rh:
        rh["is_noble"] = False
    if "is_exiled" not in rh:
        rh["is_exiled"] = False
    if "is_extinct" not in rh:
        rh["is_extinct"] = False
    if "is_deposed" not in rh:
        rh["is_deposed"] = False
    if "is_landed_knight" not in rh:
        rh["is_landed_knight"] = False

for file in glob.glob(base_path + '/filter/region/Houses-of-*.json'):
    for house in json.load(open(file, 'r')).values():
        lord = house.get("lord")
        if lord:
            if isinstance(lord, list):
                for l in lord:
                    if l in characters_name_to_id:
                        house_lords.add((house["id"], characters_name_to_id[l]))
            elif lord in characters_name_to_id:
                house_lords.add((house["id"], characters_name_to_id[lord]))

        houses[house["id"]] = {
            "id_house": house["id"],
            "name_house": house["name"]
        }
        houses_name_to_id[house["id"]] = house["name"]

house_lords = [{"house": h, "lord": l} for h, l in house_lords]
houses = [h for h in houses.values()]

allegiances = [{
    "character": char,
    "house": houses_name_to_id[h]
} for char, h in allegiances if h in houses]

# Chapters and books data
books = dict()
chapters = []
appearances = set()

file = base_path + '/chapter/chapter.json'
for chapter in json.load(open(file, 'r')):
    books[chapter["book_id"]] = chapter["book_name"]
    # Edge case where pov refers actually to alias of character
    pov = chapter["pov"].strip()
    if pov not in characters_name_to_id:
        alias = pov
        for a in aliases:
            if a["alias"] == alias:
                pov = a["character"]
            if pov == "Catelyn":
                pov = "Catelyn_Stark"
            if pov == "Davos":
                pov = "Davos_Seaworth"
            if pov == "Sansa":
                pov = "Sansa_Stark"
            if pov == "Jon":
                pov = "Jon_Snow"
            if pov == "Daenerys":
                pov = "Daenerys_Targaryen"
            if pov == "Jaime":
                pov = "Jaime_Lannister"
            if pov == "Tyrion":
                pov = "Tyrion_Lannister"
            if pov == "Arya":
                pov = "Arya_Stark"
            if pov == "Samwell":
                pov = "Samwell_Tarly"

    else:
        pov = characters_name_to_id[pov]

    chapters.append({
        "id_chapter": chapter["chapter_id"],
        "name_chapter": chapter["chapter_name"],
        "id_book": chapter["book_id"],
        "pov": pov
    })

    chapter_appearances = chapter.get("character")
    if chapter_appearances:
        for character in chapter_appearances:
            if character in characters:
                appearances.add((chapter["chapter_id"], character))

books = [{"id_book": id, "name_book": name} for id, name in books.items()]
appearances = [{"chapter": chap, "character": char} for (chap, char) in appearances]

# Battles data
battle_csv = pd.read_csv('battles/battles.csv')
involved = []
for i in range(battle_csv.shape[0]):
    for key in ['attacker_1', 'attacker_2', 'attacker_3', 'attacker_4',
                'defender_1', 'defender_2', 'defender_3', 'defender_4']:
        if type(battle_csv.loc[i, key]) == str:
            involved.append(
                (battle_csv.loc[i, 'battle_number'], battle_csv.loc[i, key]))

battles = [{'id_battle': str(battle_csv.loc[i, 'battle_number']),
            'name_battle': battle_csv.loc[i, 'name'],
            'place_battle': battle_csv.loc[i, 'location']}
            for i in range(battle_csv.shape[0])]

house_battles = [{'battle': bt, 'house': f'House_{hs}'} for bt, hs in involved]


if __name__ == "__main__":
    queries.delete_all()

    # Regions and houses
    queries.insert_dict_list('region', regions)
    queries.insert_dict_list('house', houses)
    queries.insert_dict_list('house_region', [rh for rh in region_houses.values()])

    # Characters
    queries.insert_dict_list('character', [c for c in characters.values()])
    queries.insert_dict_list('alias', aliases)
    queries.insert_dict_list('title', titles)
    queries.insert_dict_list('allegiance', allegiances)
    queries.insert_dict_list('culture', [{"name_culture": c} for c in cultures])
    queries.insert_dict_list('character_culture', character_cultures)
    queries.insert_dict_list('lineage', lineages)

    # House - Character relations
    queries.insert_dict_list('house_lord', house_lords)

    # Chapters and Books
    queries.insert_dict_list('book', books)
    queries.insert_dict_list('chapter', chapters)
    queries.insert_dict_list('appearance', appearances)

    # Battles
    queries.insert_dict_list('battle', battles)
    queries.insert_dict_list('house_battle', house_battles)
