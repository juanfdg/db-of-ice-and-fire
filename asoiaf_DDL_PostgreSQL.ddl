create table if not exists book
(
	id_book varchar not null
		constraint book_pk
			primary key,
	name_book varchar not null
);

alter table book owner to got;

create table if not exists continent
(
	continent_name varchar(50) not null
		constraint continent_pk
			primary key
);

alter table continent owner to got;

create table if not exists culture
(
	name_culture varchar(100) not null
		constraint culture_pk
			primary key
);

alter table culture owner to got;

create table if not exists region
(
	region_name varchar(50) not null
		constraint region_pk
			primary key
);

alter table region owner to got;

create table if not exists place
(
	place_name varchar(50) not null
		constraint place_pk
			primary key,
	region varchar(50) not null
		constraint place_region_fk
			references region
);

alter table place owner to got;

create table if not exists battle
(
	id_battle varchar(100) not null
		constraint battle_pk
			primary key,
	name_battle varchar(100) not null,
	place_battle varchar(50) not null
		constraint table_43_place_fk
			references place
);

alter table battle owner to got;

create table if not exists character
(
	id_char varchar(100) not null
		constraint character_pk
			primary key,
	name_char varchar(100) not null,
	place_birth varchar(50) not null
		constraint character_place_fk
			references place,
	place_death varchar(50) not null
		constraint character_place_fkv2
			references place
);

alter table character owner to got;

create table if not exists alias
(
	character varchar(100) not null
		constraint table_38_character_fk
			references character,
	alias varchar(100) not null,
	constraint alias_pk
		primary key (character, alias)
);

alter table alias owner to got;

create table if not exists chapter
(
	id_book varchar not null
		constraint table_31_book_fk
			references book,
	pov varchar not null
		constraint table_31_character_fk
			references character,
	id_chapter varchar not null
		constraint chapter_pk
			primary key,
	name_chapter varchar
);

alter table chapter owner to got;

create table if not exists appearance_chapter_character
(
	id_chapter varchar not null
		constraint appearance_chapter_character_pk
			primary key
		constraint appearance_chapter_character_chapter_id_chapter_fk
			references chapter,
	id_character varchar not null
		constraint table_32_character_fk
			references character
);

alter table appearance_chapter_character owner to got;

create table if not exists character_culture
(
	character varchar(100) not null
		constraint table_41_character_fk
			references character,
	culture varchar(100) not null
		constraint table_41_culture_fk
			references culture,
	constraint character_culture_pk
		primary key (character, culture)
);

alter table character_culture owner to got;

create table if not exists house
(
	name_house varchar(50) not null
		constraint house_pk
			primary key,
	lord varchar(100)
		constraint house_character_fk
			references character,
	words varchar(250),
	region varchar(50)
		constraint house_region_fk
			references region,
	founder varchar(100)
		constraint house_character_fkv2
			references character,
	is_royal boolean,
	is_great boolean,
	is_noble boolean,
	is_exiled boolean,
	is_extinct boolean,
	is_deposed boolean,
	is_landed_knight boolean
);

alter table house owner to got;

create table if not exists allegiance
(
	character varchar(100) not null
		constraint table_36_character_fk
			references character,
	house varchar(50) not null
		constraint table_36_house_fk
			references house,
	constraint allegiance_pk
		primary key (character, house)
);

alter table allegiance owner to got;

create table if not exists house_battle
(
	battle varchar(100) not null
		constraint table_44_battle_fk
			references battle,
	house varchar(50) not null
		constraint table_44_house_fk
			references house,
	constraint house_battle_pk
		primary key (battle, house)
);

alter table house_battle owner to got;

create table if not exists lineage
(
	parent varchar(100) not null
		constraint table_28_character_fk
			references character,
	child varchar(100) not null
		constraint table_28_character_fkv1
			references character,
	constraint lineage_pk
		primary key (child, parent)
);

alter table lineage owner to got;

create table if not exists season_appearance
(
	character varchar(100) not null
		constraint season_appearance_pk
			primary key
		constraint season_appearance_character_fk
			references character,
	season_1 integer,
	season_2 integer,
	season_3 integer,
	season_4 integer,
	season_5 integer,
	season_6 integer,
	season_7 integer,
	season_8 integer
);

alter table season_appearance owner to got;

create table if not exists title
(
	character varchar(100) not null
		constraint table_39_character_fk
			references character,
	title varchar(100) not null,
	constraint title_pk
		primary key (character, title)
);

alter table title owner to got;

