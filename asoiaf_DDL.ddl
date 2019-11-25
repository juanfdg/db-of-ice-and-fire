-- Gerado por Oracle SQL Developer Data Modeler 4.2.0.932
--   em:        2019-11-25 19:23:52 BRST
--   site:      Oracle Database 12cR2
--   tipo:      Oracle Database 12cR2



CREATE TABLE alias (
    character   VARCHAR2(100) NOT NULL,
    alias       VARCHAR2(100) NOT NULL
)
    LOGGING;

ALTER TABLE alias ADD CONSTRAINT alias_pk PRIMARY KEY ( character,alias );

CREATE TABLE allegiance (
    character   VARCHAR2(100) NOT NULL,
    house       VARCHAR2(50) NOT NULL
)
    LOGGING;

ALTER TABLE allegiance ADD CONSTRAINT allegiance_pk PRIMARY KEY ( character,house );

CREATE TABLE appearance_chapter_character (
    id_book        VARCHAR2(10) NOT NULL,
    pov            VARCHAR2(100) NOT NULL,
    pov_sequence   INTEGER NOT NULL,
    character      VARCHAR2(100) NOT NULL
)
    LOGGING;

--  ERROR: PK name length exceeds maximum allowed length(30) 
ALTER TABLE appearance_chapter_character ADD CONSTRAINT appearance_chapter_character_pk PRIMARY KEY ( id_book,pov,pov_sequence,character );

CREATE TABLE battle (
    id_battle      VARCHAR2(100) NOT NULL,
    name_battle    VARCHAR2(100) NOT NULL,
    place_battle   VARCHAR2(50) NOT NULL
)
    LOGGING;

ALTER TABLE battle ADD CONSTRAINT battle_pk PRIMARY KEY ( id_battle );

CREATE TABLE book (
    id_book     VARCHAR2(10) NOT NULL,
    name_book   VARCHAR2(50) NOT NULL
)
    LOGGING;

ALTER TABLE book ADD CONSTRAINT book_pk PRIMARY KEY ( id_book );

CREATE TABLE chapter (
    id_book         VARCHAR2(10) NOT NULL,
    pov             VARCHAR2(100) NOT NULL,
    pov_sequence    INTEGER NOT NULL,
    book_sequence   INTEGER NOT NULL
)
    LOGGING;

ALTER TABLE chapter ADD CONSTRAINT chapter_pk PRIMARY KEY ( pov,id_book,pov_sequence );

CREATE TABLE character (
    id_char       VARCHAR2(100) NOT NULL,
    name_char     VARCHAR2(100) NOT NULL,
    place_birth   VARCHAR2(50) NOT NULL,
    place_death   VARCHAR2(50) NOT NULL
)
    LOGGING;

ALTER TABLE character ADD CONSTRAINT character_pk PRIMARY KEY ( id_char );

CREATE TABLE character_culture (
    character   VARCHAR2(100) NOT NULL,
    culture     VARCHAR2(100) NOT NULL
)
    LOGGING;

ALTER TABLE character_culture ADD CONSTRAINT character_culture_pk PRIMARY KEY ( character,culture );

CREATE TABLE continent (
    continent_name   VARCHAR2(50) NOT NULL
)
    LOGGING;

ALTER TABLE continent ADD CONSTRAINT continent_pk PRIMARY KEY ( continent_name );

CREATE TABLE culture (
    name_culture   VARCHAR2(100) NOT NULL
)
    LOGGING;

ALTER TABLE culture ADD CONSTRAINT culture_pk PRIMARY KEY ( name_culture );

CREATE TABLE house (
    name_house         VARCHAR2(50) NOT NULL,
    lord               VARCHAR2(100),
    words              VARCHAR2(250),
    region             VARCHAR2(50),
    founder            VARCHAR2(100),
    "Royal?"           NUMBER,
    "Great?"           NUMBER,
    "Noble?"           NUMBER,
    "Exiled?"          NUMBER,
    "Extinct?"         NUMBER,
    "Deposed?"         NUMBER,
    "Landed_Knight?"   NUMBER
)
    LOGGING;

ALTER TABLE house ADD CONSTRAINT house_pk PRIMARY KEY ( name_house );

CREATE TABLE house_battle (
    battle   VARCHAR2(100) NOT NULL,
    house    VARCHAR2(50) NOT NULL
)
    LOGGING;

ALTER TABLE house_battle ADD CONSTRAINT house_battle_pk PRIMARY KEY ( battle,house );

CREATE TABLE lineage (
    parent   VARCHAR2(100) NOT NULL,
    child    VARCHAR2(100) NOT NULL
)
    LOGGING;

ALTER TABLE lineage ADD CONSTRAINT lineage_pk PRIMARY KEY ( child,parent );

CREATE TABLE marriage (
    husband   VARCHAR2(100) NOT NULL,
    wife      VARCHAR2(100) NOT NULL
)
    LOGGING;

ALTER TABLE marriage ADD CONSTRAINT marriage_pk PRIMARY KEY ( husband,wife );

CREATE TABLE place (
    place_name   VARCHAR2(50) NOT NULL,
    region       VARCHAR2(50) NOT NULL
)
    LOGGING;

ALTER TABLE place ADD CONSTRAINT place_pk PRIMARY KEY ( place_name );

CREATE TABLE region (
    region_name   VARCHAR2(50) NOT NULL,
    continent     VARCHAR2(50) NOT NULL
)
    LOGGING;

ALTER TABLE region ADD CONSTRAINT region_pk PRIMARY KEY ( region_name );

CREATE TABLE season_appearance (
    character   VARCHAR2(100) NOT NULL,
    season_1    NUMBER,
    season_2    NUMBER,
    season_3    NUMBER,
    season_4    NUMBER,
    season_5    NUMBER,
    season_6    NUMBER,
    season_7    NUMBER,
    season_8    NUMBER
)
    LOGGING;

ALTER TABLE season_appearance ADD CONSTRAINT season_appearance_pk PRIMARY KEY ( character );

CREATE TABLE title (
    character   VARCHAR2(100) NOT NULL,
    title       VARCHAR2(100) NOT NULL
)
    LOGGING;

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



-- Relatório do Resumo do Oracle SQL Developer Data Modeler: 
-- 
-- CREATE TABLE                            18
-- CREATE INDEX                             0
-- ALTER TABLE                             43
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           0
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          0
-- CREATE MATERIALIZED VIEW                 0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   1
-- WARNINGS                                 0
