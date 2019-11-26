import os
import glob
import json

from collections import defaultdict

import wiki_scraping.queries as queries

# Characters data
characters = []
characters_name_to_id = dict()
parents = dict()
character_cultures = []
cultures = set()
aliases = []
titles = []
allegiances = []
lineages = []

base_path = os.getcwd()
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
                    place_death = death[place_death_idx:]

        characters.append({
            "id_char": char["id"],
            "name_char": char["name"],
            "place_birth": place_birth,
            "place_death": place_death,
            "mother": char.get("mother"),
            "father": char.get("father"),
        })

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
houses = defaultdict(dict)

file = base_path + '/region/Regions.json'
for region, region_houses in json.load(open(file, 'r')).items():
    regions.append({
        "region_name": region,
    })

    for house_type, houses_by_type in region_houses.items():
        for h in houses_by_type:
            houses[h]["name_house"] = h
            houses[h]["region"] = region
            if house_type == "Royal":
                houses[h]["is_royal"] = True
            elif house_type == "Great":
                houses[h]["is_great"] = True
            elif house_type == "Noble":
                houses[h]["is_noble"] = True
            elif house_type == "Exiled":
                houses[h]["is_exiled"] = True
            elif house_type == "Extinct":
                houses[h]["is_extinct"] = True
            elif house_type == "Deposed":
                houses[h]["is_deposed"] = True
            elif house_type == "Landed Knight":
                houses[h]["is_landed_knight"] = True

    for house in houses.values():
        if "is_royal" not in house:
            house["is_royal"] = False
        if "is_great" not in house:
            house["is_great"] = False
        if "is_noble" not in house:
            house["is_noble"] = False
        if "is_exiled" not in house:
            house["is_exiled"] = False
        if "is_extinct" not in house:
            house["is_extinct"] = False
        if "is_deposed" not in house:
            house["is_deposed"] = False
        if "is_landed_knight" not in house:
            house["is_landed_knight"] = False

for file in glob.glob(base_path + '/filter/region/Houses-of-*.json'):
    for h in houses:
        houses[h]["lord"] = None

    for house in json.load(open(file, 'r')).values():
        lord = house.get("lord")
        if lord:
            if isinstance(lord, list) or lord not in characters_name_to_id:
                lord = None
            else:
                lord = characters_name_to_id[lord]
        houses[house["name"]]["lord"] = lord

# Chapters and books data
books = dict()
chapters = []
appearances = []

file = base_path + '/chapter/chapter.json'
for chapter in json.load(open(file, 'r')):
    books[chapter["book_id"]] = chapter["book_name"]
    chapters.append({
        "id_chapter": chapter["chapter_id"],
        "name_chapter": chapter["chapter_name"],
        "id_book": chapter["book_id"],
        "pov": chapter["pov"]
    })

    chapter_appearances = chapter.get("character")
    if chapter_appearances:
        for character in chapter_appearances:
            appearances.append({
                "id_chapter": chapter["chapter_id"],
                "id_char": character
            })

books = [{"id_book": id, "name_book": name} for id, name in books.items()]


if __name__ == "__main__":
    # Characters
    queries.insert_dict_list('character', characters)
    queries.insert_dict_list('alias', aliases)
    queries.insert_dict_list('title', titles)
    queries.insert_dict_list('allegiance', allegiances)
    queries.insert_dict_list('culture', [{"name_culture": c} for c in cultures])
    queries.insert_dict_list('character_culture', character_cultures)
    queries.insert_dict_list('lineage', lineages)

    # Regions and houses
    queries.insert_dict_list('region', regions)
    queries.insert_dict_list('house', [h for h in houses.values()])

    # Chapters and Books
    queries.insert_dict_list('book', books)
    queries.insert_dict_list('chapter', chapters)
    queries.insert_dict_list('appearance', appearances)
