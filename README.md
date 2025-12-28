# Python/SQL Project: Catch a Pokemon
<img width="150" height="340" alt="image" src="https://github.com/user-attachments/assets/bc64999d-9a9a-4c00-9aec-22cdb965ccfb" />


# Summary:
The original Pokemon games, Red and Blue, reshaped the video game industry when it was released. Video games at the time focused on linearity; a clear beginning and end with not much content in between. Princess peach is captured, go on this quest to save her. While many Pokemon enthusiasts remember its game for the lovable characters and story, Pokemon was one of the first games to develop an experience buiilt on repitition: a loop of collection, storing, and managing Pokemon that could be enjoyed beyond the main story. Within this gameplay loop, the original develpopers needed to use data to their advantage. Games 

### Please take a look at the final product before reading!
Available on Youtube using this link: "YOUTUBE LINK"

Goal of the game:
Professor Oak, a research scientist who makes frequent apperances throughout the original games, is creating a new revive serum to help heal Pokemon. He needs a trainer to help him aquire Pokemon samples, which can only be retrieved from Pokemon after they've been caught in a Pokeball. Your objective is to capture 3 Pokemon and hand them over to professor Oak to complete his research.

## How to Download and play the game:

Step 1: 

Download the sql tables on your SSMS server:



# Important Development Explanations

*This section is dedicated towards explaining how the game is developed* 

## Developing the backend databases:

The original pokemon game didn't have to worry about overlapping data coming in from millions of players, since every game was unqiue. However, in a live database, every trainer needs to be uniquely defined, and every action made by a trainer needs that unique signature. 

```sql
CREATE TABLE trainer
(
trainer_id INT IDENTITY(1,1) PRIMARY KEY,
trainer_name VARCHAR(255) NOT NULL,
date_created DATETIME NOT NULL
);
```

Next, all 1025 Pokemon that have existed in the Pokemon universe need to be loaded into a table, along with their base stats. These stats are used during the encounter sequence for generating unique stats for each Pokemon. Since manually typing each Pokemon and its stats would take hours, I downloaded on online database into Excel and modified it to fit my table and game. 

You can access the excel table here: [Modified Pokemon Database.csv](https://github.com/user-attachments/files/24351705/Modified.Pokemon.Database.csv)

Once the CSV is saved to your computer, you can run an sql query to load it into the table:

```sql
BULK INSERT pokemon_species
FROM 'YourFileLocation\Modified Pokemon Database.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FORMAT='CSV',
    TABLOCK
);
```

After creating the Pokemon_species table, we need to add the Pokeball data to be later retrieved when catching Pokemon. Later on, I explain how throwing balls are incorperating into the game.

```sql
create table pokeball
(
pokeball_id integer primary key,
pokeball_name varchar(255) not null,
catch_rate_mult float not null
)
```

For this game, I only included pokeballs, greatballs, ultraballs, and masterballs, with each ball containing a different catch probability multiplier. 

```sql
insert into pokeball (pokeball_id,pokeball_name,catch_rate_mult)
values
(1, 'pokeball',1),
(2, 'greatball',1.5),
(3, 'ultraball',2),
(4, 'masterball',100)
```

Lastly, we need to built a trainer_pokemon database. 

```SQL
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
```

# Developing the game in Python

## Choosing between a new game and conitnuing previous game

At the beginning of the game, when prompted for a new game or continue game, the selection of "new game" starts the trigger in the database to generate a new row in the trainer table that includes a unique trainer ID. The generated trainer_id is then returned to Python to match the future Pokemon encounters with a defined player in the databases.

```python
    cursor.execute(
        """
        INSERT INTO trainer (trainer_name, date_created)
            OUTPUT INSERTED.trainer_id
        VALUES (?, GETDATE())
        """, (trainer_name,))

    # Define new trainer_id from outcome

    trainer_id = cursor.fetchone()[0]
```

If a player chooses to continue their previous game, they are directed to input their trainer_id. If a match was found in the database, their progress would begin where they left off. This does not match how save states work, but it was a good alternative for saving progress in this small-scale project. 

```Python
    def trainer_id_check():
        # Loop unique ID question if trainer_id doesn't exist (or non-numeric option)
        while True:
            print("\nWhat's your trainer_id?")
            select_option_se()
            try:
                trainer_id = int((input("")).strip())
            except ValueError:
                print("\nPlease enter a number.")
                continue
            #print(trainer_id)
            select_option_se()

            # Use input for search in database
            cursor.execute("""select trainer_id from trainer where trainer_id = ?""", (trainer_id,))
            trainer_ids = cursor.fetchone()

            #print(trainer_ids)

            #Loop for non-existing trainer_id, continue from beginning if trainer_id doesn't exist
            if trainer_ids is None:
                print("\nTrainer ID not found.")
                continue
            else:
                # If trainer_id exists, pull trainer_name using trainer_id input
                cursor.execute("""select trainer_name from trainer where trainer_id = ?""", (trainer_id,))
                trainer_name = cursor.fetchone()[0]
                return trainer_name,trainer_id
```


## Encountering Pokemon

Encountering a Pokemon in the games usually starts by walking into a section of the map deemed condusive to spawning Pokemon, such as grass, caves, and bodies of water. Without an actual character and map to enter these areas, I built a system to encounter a random pokemon instead.

Since every Pokemon has a unique pokedex_id from 1-1025, I just did a uniform roll for an integer between 1 and 1025. So if the roll landed on 1, the trainer would encounter bulbasaur, who has a unique pokedex_id of 1. For my game inside Python, I downloaded images of each pokemon, named the images their corresponding pokedex_id, matched the integer roll to the picture name, then displayed it with a MatLab import.

<img width="1331" height="324" alt="image" src="https://github.com/user-attachments/assets/b87adc94-4765-4755-b8bf-5b17ef0bb4f6" />



In every Pokemon game, each encounter with a Pokemon is unique. Although trainers can encounter the same Pokemon multiple times, and similarily that Pokemon can belong to many trainers, every Pokemon differs in their stats.  

The original Pokemon database, which was originally created using complex arrays locked into the memory of the game, assigned base stats to each Pokemon, and then used unique formulas/multipliers to generate variety in those stats during each encounter. These adjusted stats are commonly known as "IVs". That's what I replicated in my game 



Therefore, to mimic this style in SQL, I created a simple table with each Pokemon and their base stats:

```sql
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
```

Once an encounter with a Pokemon began, I used that Pokemon's base states stored in the table and run it through the actual formulas used in the Pokemon games. I decided to not use the original formulas for the Red/Blue games, as these formulas were engineered to  little memory inside a gameboy. I elected to mirror the more modern Pokemon games, which still utilizes the same random generation principles as the original, but allows for more randomness. There are two main formulas used in modern games, the health formula and the general base stat formula (attack, defense, speed, etc.). Each of these formulas require a uniform roll of an integer between 0 and 31, giving a 1 in 32 (~3.1%) chance per stat. The probability of a Pokémon having a specific IV value across all six stats is therefore (1/32)⁶. Or, in other words, the probability of encountering two statistically identical Pokemon is about 1 in 1.07 billion. Not truly unique, but just about!

Here's the code for running this calculation in python:

```Python
        def generate_iv():
            return random.randint(0, 31)

        hp_iv = generate_iv()
        atk_iv = generate_iv()
        def_iv = generate_iv()
        sp_atk_iv = generate_iv()
        sp_def_iv = generate_iv()
        speed_iv = generate_iv()

        # Stat calculation functions
        def calculate_hp(base_hp_val, iv, lvl):
            return math.floor(((2 * base_hp_val + iv) * lvl) / 100) + lvl + 10

        def calculate_stat(base_val, iv, lvl):
            return math.floor(((2 * base_val + iv) * lvl) / 100) + 5

        final_hp = calculate_hp(base_hp, hp_iv, level)
        final_attack = calculate_stat(base_attack, atk_iv, level)
        final_defense = calculate_stat(base_defense, def_iv, level)
        final_sp_atk = calculate_stat(base_sp_attack, sp_atk_iv, level)
        final_sp_def = calculate_stat(base_sp_defense, sp_def_iv, level)
        final_speed = calculate_stat(base_speed, speed_iv, level)
```

Encounters are always triggered by the selection of an encounter option in a menu prompt. 

#### There are 3 different menues that trigger a unique encounter.

- The beginning of the game menu
```Python
        start_encounter_question = input("\nStart an encounter?\n "
                                         "1) Yes\n "
                                         "2) Exit Game\n> "
                                         )
 ```
- Unsuccessful capture attempt menu:
```Python
 another_try = input("\nWould you like to throw another Pokéball? \n "
                                "1) Yes\n "
                                "2) Encounter new Pokémon\n> "
                                ).strip().upper()
```
- Successful capture attempt menu

```Python
print("\nWould you like to encounter a new Pokémon?")
            print("1) Yes")

            # Gatekeep Pokedex access before capture
            if capture_count > 0:
                print("2) View Pokédex")

            print("3) Exit Game")

            again_answer = input("> ").strip()
```

Each "Encounter new Pokemon" selection restarts the encounter from the beginning, reselecting a Pokemon ID and assigning unique IV stats. 


## Capturing Pokemon

In all Pokemon games, similar to stats, each pokemon has a defined base catch rate. Once an encounter begins, that catch rate is adjusted through an advanced formula to account for variations in stats like level, hp, and speed. Better, more powerful Pokemon like legendaries are almost always harder to catch than less powerful pokemon. Pokemon with lower capture rates often promote the concept of battling Pokemon with your own Pokemon before capturing. As your Pokemon attacks, the enemies Pokemon's hp is decreases, which then increase that Pokemon's catch rate.
However, since my game has no battling mechanic and focuses more on just the catching experience, I created a small formula for catching Pokemon, which still uses the original base catch rates but doesn't allow for changes from stat variation of hp reduction by battling. 

### Throwing Pokeballs

Furthermore, during the catching sequence of the game, trainers have the ability to choose the type of pokeballs they throw. Some Pokeballs are inherently better than others, such as the ultraball increasing the catch rate above greatballs. Moreover, some pokeballs have unique effects, the catch rate of any pokemon its thrown at, while other pokeballs are more situational, with abilities tailored to the weather, pokemon type, or location/time of day. 

Unfortuantely, my game doesn't include weather patterns, locations, or any other unique elements that would favor a certain pokeball type over another. In conjunction, given the chance to choose between an evidently strong ball and a weak ball, a player would choose to use the stronger ball every time. Therefore, I have a weighted random roll that determines whether the trainer throws a pokeball, greatball, ultraball, or masterball (100% catch rate), with stronger balls having a lower probability. In the future, I would like to explore giving a finite number of stronger balls to trainer at the start, and allowing trainers to choose what balls they throw. This would encourage a strategy to save stronger balls for stronger Pokemon. 

In python, once the weighted roll picks a number, it matches that number to the Primary Key in the SSMS Pokeball table:

```Python
        # unique integers associated with each Pokeball type in SSMS: 1-4
        numbers = [1, 2, 3, 4]
        # Assign lower probability for stronger pokeballs
        probabilities = [0.5, 0.3, 0.15, 0.05]
        # Extract id
        pokeball_id = random.choices(numbers, probabilities, k=1)[0]

     # Use pokeball_id to extract pokeball information
        cursor.execute("SELECT * FROM pokeball WHERE pokeball_id = ?", (pokeball_id,))
        row = cursor.fetchone()
```

After throwing a ball, many different things can happen -

#### 1. The Pokemon broke free

This result is dependent on the uniform roll of the catch rate compared to the catch rate percentage of the Pokemon. If the roll is greater than the catch rate, the Pokemon breaks free
```Python
  # Perform the catch roll
        roll = random.uniform(0, 100)
        caught = roll < adjusted_catch_rate
```

#### 2. The Pokemon runs away 

if a trainer has an unsuccessful attempt at capturing a Pokemon, there's a 25% chance the Pokemon will run away and be uncatchable. This returns "pokemon_escaped".
```Python
            escape_roll = random.randint(1, 4)
            if escape_roll == 1:
                return "pokemon_escaped!"
```

#### 3. The trainer chooses to run away

If the Pokemon does not run away, the trainer can choose to run away instead, leaving that Pokemon behind to encounter a new one. This returns "you_escaped".
```Python
                  another_try = input("\nWould you like to throw another Pokéball? \n "
                                        "1) Yes\n "
                                        "2) Encounter new Pokémon\n> "
                                        ).strip().upper()
```

#### 4. The Pokemon is caught

This result is also dependent on the same uniform roll as the Pokemon breaking free. If the roll is less than the catch rate, the Pokemon is considered caught. This returns "caught"
```Python
  # Perform the catch roll
        roll = random.uniform(0, 100)
        caught = roll < adjusted_catch_rate
```

##### In total, there are three potential things the code can return after throwing a pokeball. Each of them branch off into various triggers
- "Pokemon_escaped" - Branches into menu asking for new encounter
- "You_escaped" - Branches into menu asking for new encounter
- "Caught" - Branches into the caught action, recording the capture in the database and increasing the capture count of their game. 


### Successful Pokemon Capture Database Trigger:
Once a Pokemon is caught, I built python trigger to create another row in the database with all of the Pokemon's information and unique IVs, which creates a sequential instance_id in SSMS. The trainer_id is also attached to the captured pokemon so that it can be joined to the trainer table for an official Pokedex. 

```Python
          cursor.execute(
                """INSERT INTO 
                         trainer_pokemon (trainer_id, pokedex_id, pokemon_name, iv_hp, iv_attack, iv_defense, iv_sp_attack, iv_sp_defense, iv_speed, level, pokeball_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (trainer_id, pokedex_id, pokemon_name, final_hp, final_attack, final_defense, final_sp_atk, final_sp_def, final_speed, level, pokeball_id)
            )
```

## Building a Pokedex of Captured Pokemon.

Once a pokemon is caught, trainers are given access to their Podex, which catalogs the Pokemon they've caught. It includes both the general information of each captured Pokemon along with their IV_stats that were calculated during the encounter. Each additionall capture adds to the Pokedex, and each successfuly capture gives access to view their newly updated Pokedex.

The pokedex is built by utilizing the trainer_pokemon, pokemon_species, and pokeball tables. The trainer_pokemon table contains the unique captured Pokemon and their IV stats, the pokemon_species table includes the generation information related to each Pokemon (name, type, game of origin, etc.), and the pokeball table gives us the pokeball name used to capture the Pokemon. Even though the caught pokemon of each trainer exists in the trainer_pokeball table, we can use the trainers trainer_id to limit results to their captured pokemon.  

```python
       cursor.execute("""
                               select a.pokemon_name,
                                      a.pokedex_id,
                                      level,
                                      type_1,
                                      case when type_2 = 'NULL' then '' else type_2 end as type_2,
                                      game_of_origin,
                                      iv_hp,
                                      iv_attack,
                                      iv_defense,
                                      iv_sp_attack,
                                      iv_sp_defense,
                                      iv_speed,
                                      pokeball_name
                               from trainer_pokemon a
                                        join pokemon_species c
                                             on a.pokedex_id = c.pokedex_id
                                        join pokeball d
                                             on a.pokeball_id = d.pokeball_id
                               where a.trainer_id = ?""", (trainer_id,))
                pokedex = cursor.fetchall()
```

## Designing the main gameplay loop:

To allow infinite encounters and catch attempts with pokemon, loops needed to be developed to constantly reroute the player. 

This diagram represents the main gameplay loop used in the game:

<img width="2062" height="1041" alt="Game Loop (2)" src="https://github.com/user-attachments/assets/81a230a7-cf2f-452f-9984-56c062f44014" />

As shown, the menus, encounter system, and catch attempt system are separated. The encounter system is defined as "p" at the end of the encounter process, remaining defined until it is redefined by another encounter trigger. This allows the catch attempt system to utilize only the last encountered Pokemon, exluding any of the Pokemon encountered previously that were also "p". Then, these menus and systems are looped back based on the result of the catch attempt or a menu choice.

## Game storyline triggers.

When starting a new game, each trainer is given a capture count of 0, and each Pokemon capture increases that count. When continuing a previous game, the capture count is defined through a query that counts the total Pokemon caught associated with the trainer_id.

```Python
      cursor.execute("""select count(pokedex_id) from trainer_pokemon a where a.trainer_id = ?""", (trainer_id,))
        capture_count = cursor.fetchone()[0]
```

After the player catches their first Pokemon, Professor Oak is triggered to begin his dialogue and deliver a Pokedex. Once delivered, a trainer has access to the menu options that include viewing their current Pokedex. This is done by gatekeeping the option based on the capture count.

```Python
 print("\nWould you like to encounter a new Pokémon?")
            print("1) Yes")

            # Gatekeep Pokedex access before capture
            if capture_count > 0:
                print("2) View Pokédex")

            print("3) Exit Game")

            again_answer = input("> ").strip()
```

However, when this menu appears when the capture count is 0, it's slightly adjar considering there's no option 2, only options 1 & 3. I could fix this by switching option 2 and 3, but having the option "View Pokedex" after the option to "Exit Game" sounds strager. So, this menu is a working progress. 

After a third capture, the game is successfuly completed, rewaring the player with a special message from professor Oak and vistory music from the original games. Once the game is complete, the player still has the opportunity to encounter and capture more pokemon to add to their pokedex. No additional dialogue exists beyond the 3 main captures, however.  











