CREATE TABLE alias (
    character   VARCHAR(100) NOT NULL,
    alias       VARCHAR(100) NOT NULL
);

ALTER TABLE alias ADD CONSTRAINT alias_pk PRIMARY KEY ( character,alias );

CREATE TABLE allegiance (
    character   VARCHAR(100) NOT NULL,
    house       VARCHAR(50) NOT NULL
);

ALTER TABLE allegiance ADD CONSTRAINT allegiance_pk PRIMARY KEY ( character,house );

CREATE TABLE appearance_chapter_character (
    id_book        VARCHAR(10) NOT NULL,
    pov            VARCHAR(100) NOT NULL,
    pov_sequence   INTEGER NOT NULL,
    character      VARCHAR(100) NOT NULL
);

ALTER TABLE appearance_chapter_character ADD CONSTRAINT appear_chap_char_pk PRIMARY KEY ( id_book,pov,pov_sequence,character );

CREATE TABLE battle (
    id_battle      VARCHAR(100) NOT NULL,
    name_battle    VARCHAR(100) NOT NULL,
    place_battle   VARCHAR(50) NOT NULL
);

ALTER TABLE battle ADD CONSTRAINT battle_pk PRIMARY KEY ( id_battle );

CREATE TABLE book (
    id_book     VARCHAR(10) NOT NULL,
    name_book   VARCHAR(50) NOT NULL
);

ALTER TABLE book ADD CONSTRAINT book_pk PRIMARY KEY ( id_book );

CREATE TABLE chapter (
    id_book         VARCHAR(10) NOT NULL,
    pov             VARCHAR(100) NOT NULL,
    pov_sequence    INTEGER NOT NULL,
    book_sequence   INTEGER NOT NULL
);

ALTER TABLE chapter ADD CONSTRAINT chapter_pk PRIMARY KEY ( pov,id_book,pov_sequence );

CREATE TABLE character (
    id_char       VARCHAR(100) NOT NULL,
    name_char     VARCHAR(100) NOT NULL,
    place_birth   VARCHAR(50) NOT NULL,
    place_death   VARCHAR(50) NOT NULL
);

ALTER TABLE character ADD CONSTRAINT character_pk PRIMARY KEY ( id_char );

CREATE TABLE character_culture (
    character   VARCHAR(100) NOT NULL,
    culture     VARCHAR(100) NOT NULL
);

ALTER TABLE character_culture ADD CONSTRAINT character_culture_pk PRIMARY KEY ( character,culture );

CREATE TABLE continent (
    continent_name   VARCHAR(50) NOT NULL
);

ALTER TABLE continent ADD CONSTRAINT continent_pk PRIMARY KEY ( continent_name );

CREATE TABLE culture (
    name_culture   VARCHAR(100) NOT NULL
);

ALTER TABLE culture ADD CONSTRAINT culture_pk PRIMARY KEY ( name_culture );

CREATE TABLE house (
    name_house         VARCHAR(50) NOT NULL,
    lord               VARCHAR(100),
    words              VARCHAR(250),
    region             VARCHAR(50),
    founder            VARCHAR(100),
    "Royal?"           INTEGER,
    "Great?"           INTEGER,
    "Noble?"           INTEGER,
    "Exiled?"          INTEGER,
    "Extinct?"         INTEGER,
    "Deposed?"         INTEGER,
    "Landed_Knight?"   INTEGER
);

ALTER TABLE house ADD CONSTRAINT house_pk PRIMARY KEY ( name_house );

CREATE TABLE house_battle (
    battle   VARCHAR(100) NOT NULL,
    house    VARCHAR(50) NOT NULL
);

ALTER TABLE house_battle ADD CONSTRAINT house_battle_pk PRIMARY KEY ( battle,house );

CREATE TABLE lineage (
    parent   VARCHAR(100) NOT NULL,
    child    VARCHAR(100) NOT NULL
);

ALTER TABLE lineage ADD CONSTRAINT lineage_pk PRIMARY KEY ( child,parent );

CREATE TABLE marriage (
    husband   VARCHAR(100) NOT NULL,
    wife      VARCHAR(100) NOT NULL
);

ALTER TABLE marriage ADD CONSTRAINT marriage_pk PRIMARY KEY ( husband,wife );

CREATE TABLE place (
    place_name   VARCHAR(50) NOT NULL,
    region       VARCHAR(50) NOT NULL
);

ALTER TABLE place ADD CONSTRAINT place_pk PRIMARY KEY ( place_name );

CREATE TABLE region (
    region_name   VARCHAR(50) NOT NULL,
    continent     VARCHAR(50) NOT NULL
);

ALTER TABLE region ADD CONSTRAINT region_pk PRIMARY KEY ( region_name );

CREATE TABLE season_appearance (
    character   VARCHAR(100) NOT NULL,
    season_1    INTEGER,
    season_2    INTEGER,
    season_3    INTEGER,
    season_4    INTEGER,
    season_5    INTEGER,
    season_6    INTEGER,
    season_7    INTEGER,
    season_8    INTEGER
);

ALTER TABLE season_appearance ADD CONSTRAINT season_appearance_pk PRIMARY KEY ( character );

CREATE TABLE title (
    character   VARCHAR(100) NOT NULL,
    title       VARCHAR(100) NOT NULL
);

ALTER TABLE title ADD CONSTRAINT title_pk PRIMARY KEY ( character,title );

ALTER TABLE character ADD CONSTRAINT character_place_fk FOREIGN KEY ( place_birth )
    REFERENCES place ( place_name )
NOT DEFERRABLE;

ALTER TABLE character ADD CONSTRAINT character_place_fkv2 FOREIGN KEY ( place_death )
    REFERENCES place ( place_name )
NOT DEFERRABLE;

ALTER TABLE house ADD CONSTRAINT house_character_fk FOREIGN KEY ( lord )
    REFERENCES character ( id_char )
NOT DEFERRABLE;

ALTER TABLE house ADD CONSTRAINT house_character_fkv2 FOREIGN KEY ( founder )
    REFERENCES character ( id_char )
NOT DEFERRABLE;

ALTER TABLE house ADD CONSTRAINT house_region_fk FOREIGN KEY ( region )
    REFERENCES region ( region_name )
NOT DEFERRABLE;

ALTER TABLE place ADD CONSTRAINT place_region_fk FOREIGN KEY ( region )
    REFERENCES region ( region_name )
NOT DEFERRABLE;

ALTER TABLE region ADD CONSTRAINT region_continent_fk FOREIGN KEY ( continent )
    REFERENCES continent ( continent_name )
NOT DEFERRABLE;

ALTER TABLE season_appearance ADD CONSTRAINT season_appearance_character_fk FOREIGN KEY ( character )
    REFERENCES character ( id_char )
NOT DEFERRABLE;

ALTER TABLE marriage ADD CONSTRAINT table_27_character_fk FOREIGN KEY ( husband )
    REFERENCES character ( id_char )
NOT DEFERRABLE;

ALTER TABLE marriage ADD CONSTRAINT table_27_character_fkv1 FOREIGN KEY ( wife )
    REFERENCES character ( id_char )
NOT DEFERRABLE;

ALTER TABLE lineage ADD CONSTRAINT table_28_character_fk FOREIGN KEY ( parent )
    REFERENCES character ( id_char )
NOT DEFERRABLE;

ALTER TABLE lineage ADD CONSTRAINT table_28_character_fkv1 FOREIGN KEY ( child )
    REFERENCES character ( id_char )
NOT DEFERRABLE;

ALTER TABLE chapter ADD CONSTRAINT table_31_book_fk FOREIGN KEY ( id_book )
    REFERENCES book ( id_book )
NOT DEFERRABLE;

ALTER TABLE chapter ADD CONSTRAINT table_31_character_fk FOREIGN KEY ( pov )
    REFERENCES character ( id_char )
NOT DEFERRABLE;

ALTER TABLE appearance_chapter_character ADD CONSTRAINT table_32_chapter_fk FOREIGN KEY ( pov,id_book,pov_sequence )
    REFERENCES chapter ( pov,id_book,pov_sequence )
NOT DEFERRABLE;

ALTER TABLE appearance_chapter_character ADD CONSTRAINT table_32_character_fk FOREIGN KEY ( character )
    REFERENCES character ( id_char )
NOT DEFERRABLE;

ALTER TABLE allegiance ADD CONSTRAINT table_36_character_fk FOREIGN KEY ( character )
    REFERENCES character ( id_char )
NOT DEFERRABLE;

ALTER TABLE allegiance ADD CONSTRAINT table_36_house_fk FOREIGN KEY ( house )
    REFERENCES house ( name_house )
NOT DEFERRABLE;

ALTER TABLE alias ADD CONSTRAINT table_38_character_fk FOREIGN KEY ( character )
    REFERENCES character ( id_char )
NOT DEFERRABLE;

ALTER TABLE title ADD CONSTRAINT table_39_character_fk FOREIGN KEY ( character )
    REFERENCES character ( id_char )
NOT DEFERRABLE;

ALTER TABLE character_culture ADD CONSTRAINT table_41_character_fk FOREIGN KEY ( character )
    REFERENCES character ( id_char )
NOT DEFERRABLE;

ALTER TABLE character_culture ADD CONSTRAINT table_41_culture_fk FOREIGN KEY ( culture )
    REFERENCES culture ( name_culture )
NOT DEFERRABLE;

ALTER TABLE battle ADD CONSTRAINT table_43_place_fk FOREIGN KEY ( place_battle )
    REFERENCES place ( place_name )
NOT DEFERRABLE;

ALTER TABLE house_battle ADD CONSTRAINT table_44_battle_fk FOREIGN KEY ( battle )
    REFERENCES battle ( id_battle )
NOT DEFERRABLE;

ALTER TABLE house_battle ADD CONSTRAINT table_44_house_fk FOREIGN KEY ( house )
    REFERENCES house ( name_house )
NOT DEFERRABLE;
