USE POKEMON

Create table pokemon_species
(
pokedex_id integer Primary Key,
pokemon_name varchar(255) not null,
Legendary_Type varchar(255),
type_1 varchar(255) not null,
type_2 varchar(255),
game_of_origin varchar(255),
base_hp integer not null,
base_attack integer not null,
base_defense integer not null,
base_sp_attack integer not null,
base_sp_defense integer not null,
base_speed integer not null,
base_level integer,
catch_rate integer not null,
pre_evolution_id varchar(255),
evolution_path varchar(255)
)

Create table moves
(
move_id integer Primary Key,
move_name varchar(255),
type varchar(255),
power integer,
accuracy integer
)

create table pokeball
(
pokeball_id integer primary key,
pokeball_name varchar(255) not null,
catch_rate_mult float not null
)


CREATE TABLE trainer
(
trainer_id INT IDENTITY(1,1) PRIMARY KEY,
trainer_name VARCHAR(255) NOT NULL,
date_created DATETIME NOT NULL,
total_pokemon INT
);


Create table trainer_pokemon
(
instance_id integer identity Primary Key,
trainer_id integer REFERENCES trainer(trainer_id) not null,
pokedex_id integer REFERENCES pokemon_species(pokedex_id) not null,
pokemon_name varchar(255) not null,
iv_hp integer not null,
iv_attack integer not null,
iv_defense integer not null,
iv_sp_attack integer not null,
iv_sp_defense integer not null,
iv_speed integer not null,
level integer not null,
pokeball_id integer REFERENCES pokeball(pokeball_id) not null
)

/*
drop table trainer_pokemon
drop table trainer
drop table moves
drop table pokemon_species
drop table pokeball
*/
/*
select * from trainer
select * from pokemon_species
select * from trainer_pokemon
*/

-- Future ideas: Pokeball type is randomized, with each ball applying a different multiplier to the catch rate. That pokeball is then logged in the trainer_pokemon table 
-- Every encounter provides a random amount of chances to catch the same pokemon - up to 3 times. If the third time fails, then the pokemon escapes. 



--truncate table trainer
--truncate table pokemon_species
--truncate table trainer_pokemon

--delete from  trainer where
--1=1

--delete from  pokemon_species where
--1=1

insert into pokeball (pokeball_id,pokeball_name,catch_rate_mult)
values
(1, 'pokeball',1),
(2, 'greatball',1.5),
(3, 'ultraball',2),
(4, 'masterball',100)



--select * from pokemon_species where pokemon_name like '%z%'



--select * from trainer_pokemon where trainer_id >24

--select * from 

--select count(pokedex_id) from trainer_pokemon a 
--where a.trainer_id = '15'


--select distinct pokedex_id where trainer_id 
--select * from pokemon_species where Legendary_Type not like 'null' order by pokemon_name


select a.pokemon_name,a.pokedex_id,level,type_1,type_2,game_of_origin,iv_hp,iv_attack,iv_defense,iv_sp_attack,iv_sp_defense,iv_speed,pokeball_name
from trainer_pokemon a 
left join trainer b
on a.trainer_id = b.trainer_id
join pokemon_species c
on a.pokedex_id = c.pokedex_id
join pokeball d
on a.pokeball_id = d.pokeball_id 
--where b.trainer_id = '311'