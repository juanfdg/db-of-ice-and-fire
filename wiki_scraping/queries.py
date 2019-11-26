from psycopg2 import connect
from psycopg2.extras import RealDictCursor, execute_batch

conn = connect(dbname="got",
               user="got",
               password="got",
               host="localhost",
               port="5432")
cursor = conn.cursor(cursor_factory=RealDictCursor)

ALIAS_QUERY = """
INSERT INTO alias (character,
                   alias)
VALUES (%(character)s,
        %(alias)s)
"""

ALLEGIANCE_QUERY = """
INSERT INTO allegiance (character,
             house)
VALUES (%(character)s,
        %(house)s)
"""

APPEARANCE_QUERY = """
INSERT INTO appearance_chapter_character(id_chapter,
                                         id_character)
VALUES (%(id_chapter)s,
        %(character)s)
"""

BATTLE_QUERY = """
INSERT INTO battle (id_battle,
                    name_battle,
                    place_battle)
VALUES (%(id_battlle)s,
        %(name_battle)s,
        %(place_battle)s)
"""

BOOK_QUERY = """
INSERT INTO book (id_book,
                  name_book)
VALUES (%(id_book)s,
        %(name_book)s)
"""

CHAPTER_QUERY = """
INSERT INTO chapter (id_chapter,
                     name_chapter,
                     id_book,
                     pov)
VALUES (%(id_chapter)s,
        %(name_chapter)s,
        %(id_book)s,
        %(pov)s)
"""

CHARACTER_QUERY = """
INSERT INTO character (id_char,
                       name_char,
                       place_birth,
                       place_death)
VALUES (%(id_char)s,
        %(name_char)s,
        %(place_birth)s,
        %(place_death)s)
"""

CULTURE_QUERY = """
INSERT INTO culture (name_culture)
VALUES (%(name_culture)s)
"""

CHARACTER_CULTURE_QUERY = """
INSERT INTO culture (character,
                     culture)
VALUES (%(character)s,
        %(culture)s)
"""

HOUSE_QUERY = """
INSERT INTO house (name_house, 
                   lord,
                   region,
                   is_royal,
                   is_great,
                   is_noble,
                   is_exiled,
                   is_extinct,
                   is_deposed,
                   is_landed_knight)
VALUES (%(name_house)s,
        %(lord)s,
        %(region)s,
        %(is_royal)s,
        %(is_great)s,
        %(is_noble)s,
        %(is_exiled)s,
        %(is_extinct)s,
        %(is_deposed)s,
        %(is_landed_knight)s)
"""

REGION_QUERY = """
INSERT INTO region (region_name)
VALUES (%(region_name)s)
"""


HOUSE_BATTLE_QUERY = """
INSERT INTO house_battle (battle,
                          house)
VALUES (%(battle)s,
        %(house)s)
"""

LINEAGE_QUERY = """
INSERT INTO lineage (parent,
                     child)
VALUES (%(parent)s,
        %(child)s)
"""

TITLE_QUERY = """
INSERT INTO title (character,
                   title)
VALUES (%(character)s,
        %(title)s)
"""

table_to_query = {
    "alias": ALIAS_QUERY,
    "allegiance": ALLEGIANCE_QUERY,
    "appearance": APPEARANCE_QUERY,
    "battle":  BATTLE_QUERY,
    "book": BOOK_QUERY,
    "chapter": CHAPTER_QUERY,
    "character": CHARACTER_QUERY,
    "culture": CULTURE_QUERY,
    "character_culture": CHARACTER_CULTURE_QUERY,
    "house": HOUSE_QUERY,
    "region": REGION_QUERY,
    "house_battle": HOUSE_BATTLE_QUERY,
    "lineage": LINEAGE_QUERY,
    "title": TITLE_QUERY
}


def insert_dict_list(table, dict_list):
    execute_batch(cursor, table_to_query[table], dict_list)
    conn.commit()
