# Python/SQL Game: Pokémon Catching Adventure!

<img width="250" height="250" alt="image" src="https://github.com/user-attachments/assets/a2751be7-33a9-4e1c-8fea-b88aaddf07ee" />

## Goal of the game

Professor Oak, a research scientist seen throughout the original games, is on the verge of a scientific breakthrough - a powerful new revive serum to heal fainted Pokémon. To complete his research, he needs a trainer to help him acquire Pokémon samples, which can only be retrieved from Pokémon after they've been caught in a Pokéball. 

Catch Pokémon, return them to Professor Oak’s laboratory, and survive encounters with wild Pokémon and hostile opponents along the way!

(This is a text-based Python game focused on recreating the main catching experience of the Pokémon games. It features OG music, characters, and sound effects reminiscent of the original games on the Gameboy. I also implemented realistic mechanics like weighted catch rates, unique IVs, and Pokédex building. Please let me know what you think! I'd appreciate feedback of any kind.)

![gengar1-ezgif com-resize (1)](https://github.com/user-attachments/assets/ecd27be5-3fa4-4dbd-b321-55d6be2f9ae6)



### Watch the game being played on Youtube! ([https://www.youtube.com/watch?v=9modyBxMpoA](https://youtu.be/9modyBxMpoA))


<img width="130" height="306" alt="image" src="https://github.com/user-attachments/assets/bc64999d-9a9a-4c00-9aec-22cdb965ccfb" />


## How to Download and Play the Game:

### Step 1: Download the SQL tables on your SSMS server:

[Table Creation.sql](https://github.com/user-attachments/files/24363922/Table.Creation.sql)

- *Run query to create tables*

### Step 2:  Download Excel sheet with Pokémon data:

[Modified Pokémon Database.csv](https://github.com/user-attachments/files/24363961/Modified.Pokemon.Database.csv)

### Step 3: Import Data:

[Insert Values.sql](https://github.com/user-attachments/files/24363973/Insert.Values.sql)

- *Make sure to rewrite the file location in the query*

### Step 4: Download the Python Project: 

- *This project utilized Pycharm with Python interpreter 3.11 for development, and may be required to play the game*

### Step 5: Download all python packages listed at the top of the file:

### Step 6: Connect to SSMS from Python:

May first require 
```pip install pyodbc``` ran in terminal.

Replace the SSMS connection in the Python file to match your server (Line 15-22) -

For Windows authentication -
```Python
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};' # Your driver might be 18
    'SERVER=localhost;'
    'DATABASE=Pokemon;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()
```
For username/password authentification -
```Python
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=HavensPC;"
    "DATABASE=Pokemon;"
    "UID=your_username;"
    "PWD=your_password;"
)
```

### That's it - you're ready to play!

<img width="533" height="378" alt="image" src="https://github.com/user-attachments/assets/b1ad8e78-e9a5-439d-9e06-4deedfbcb091" />

*
*
*

# Development

*This section is dedicated towards explaining how the game is developed.* 

## SQL Server Management Studio (SSMS) Backend

This Pokémon game's backend design was created to mirror what modern Pokémon game databases look like - a perpetual push and pull of information using queries to dictate game experiences and track important information. I also designed the backend to be a pseudo "live" database, where multiple unique games can exist at one time without conflict. This is accomplished through intentional table designs that utilize primary and foreign keys to maintain uniqueness and properly communicate between each other. 

### ERD Diagram:

<img width="950" height="566" alt="image" src="https://github.com/user-attachments/assets/2bcbc6a8-c531-4ee7-96a2-f2d92e4654bc" />


### SQL Table Queries:

#### Trainer - 

The first table created is the trainer table. This will house the trainer's unique ID, along with their name and the date their account was created. This table is essential to make all data related to a player's game unique to just them. This is a standalone table with no relationships.

```sql
CREATE TABLE trainer
(
trainer_id INT IDENTITY(1,1) PRIMARY KEY,
trainer_name VARCHAR(255) NOT NULL,
date_created DATETIME NOT NULL
);
```

#### pokémon_Species -

All 1025 Pokémon that have existed in the Pokémon universe also need to be loaded into a table along with their base stats. These stats are used during the encounter sequence for generating unique stats for each Pokémon. This is a standalone table with no relationships to other tables.

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

Since manually typing in each Pokémon and its stats would take hours, I downloaded an online database to Excel and modified it to fit my table. 

You can access the Excel sheet here: [Modified Pokemon Database.csv](https://github.com/user-attachments/files/24351705/Modified.Pokemon.Database.csv)

Once the CSV is saved to your computer, you can run an SQL query to load it into the table:

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

#### Pokéball -

We also need to add the Pokéball data to be later returned to Python when catching Pokémon.

```sql
create table pokeball
(
pokeball_id integer primary key,
pokeball_name varchar(255) not null,
catch_rate_mult float not null
)
```

For this game, I only included Pokéballs, Greatballs, Ultraballs, and Masterballs. Each ball contains a different catch probability multiplier, with higher tier balls offering progressivly greater multipliers.

```sql
insert into pokeball (pokeball_id,pokeball_name,catch_rate_mult)
values
(1, 'pokeball',1),
(2, 'greatball',1.5),
(3, 'ultraball',2),
(4, 'masterball',100)
```

#### Trainer_pokemon -

Lastly, we need to build a trainer_pokemon table. This will include the data of every Pokémon caught by a trainer, and is the foundation for developing a "live" database. Once a trainer catches a Pokémon, Python runs an insert statement to transfer all of the associated information with that captured Pokémon and the trainer who caught it. The instance_id is the Primary Key that unique defines the capture, which will now always be associatted with that unique Pokémon. This table has a one to many relationship with the trainer table, as each instance_id is associated with only one trainer while each trainer can have multiple instance_ids. Additionally, it also has a many to many relationship with the Pokeball table. Each instance_id can be associated with many pokeballs and each pokeball can be used in multiple instance_ids. 

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

# Python Front End

### Choosing between a new game and continuing previous game

The player is directed to choose between starting a new game or continuing where they left off:

```Python
new_game_question =(input("\nWould you like to create a new game?\n "
                          "1) Yes\n "
                          "2) Continue previous game\n> "
                          ))
```

#### New Game:

The selection of "new game" starts the trigger in the database to generate a new row in the trainer table that includes a unique trainer ID. The generated trainer_id is then returned to Python to match the future Pokemon encounters with a defined player in the databases.

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

#### Continue Game:

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


## Encountering Pokémon

Encountering a Pokémon in the games usually starts by walking into a section of the map deemed conducive to spawning Pokémon, such as grass, caves, and bodies of water. Without an actual character or map to enter these areas, I built a system to encounter random Pokémon instead.

Since every Pokémon has a unique pokedex_id from 1-1025, I just did a uniform roll for an integer between 1 and 1025. So if the roll landed on 1, the trainer would encounter Bulbasaur, who has a unique pokedex_id of 1. For my game inside Python, I downloaded images of each Pokémon, named the images their corresponding pokedex_id, matched the integer roll to the picture name, then displayed it with a MatLab import.

<img width="1331" height="324" alt="image" src="https://github.com/user-attachments/assets/b87adc94-4765-4755-b8bf-5b17ef0bb4f6" />



In every Pokémon game, each encounter with a Pokémon is unique. Although trainers can encounter the same Pokémon multiple times, and similarly that Pokémon can belong to many trainers, every Pokémon differs in their stats.  

The original Pokémon database, which was originally created using complex arrays locked into the memory of the game, assigned base stats to each Pokémon, and then used unique formulas/multipliers to generate variety in those stats during each encounter. These adjusted stats are commonly known as "IVs". That's what I replicated in my game, but using SSMS as the arrays.


Once an encounter with a Pokémon began, I used that Pokémon's base states stored in the table and run it through the actual formulas used in the Pokémon games. I decided to not use the original formulas for the Red/Blue games, as these formulas were engineered to little memory inside a Gameboy. I elected to mirror the more modern Pokémon games, which still utilizes the same random generation principles as the original, but allows for more randomness. There are two main formulas used in modern games, the health formula and the general base stat formula (attack, defense, speed, etc.). Each of these formulas require a uniform roll of an integer between 0 and 31, giving a 1 in 32 (~3.1%) chance per stat. The probability of a Pokémon having a specific IV value across all six stats is therefore (1/32)⁶. Or, in other words, the probability of encountering two statistically identical Pokémon is about 1 in 1.07 billion. Not truly unique, but just about!

### IV Stats Formuala:

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

Encounters with Pokemon are always triggered by the selection of an encounter option in a menu prompt. 

#### There are 3 different menus that trigger a unique encounter.

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

Each "Encounter new Pokémon" selection restarts the encounter from the beginning, reselecting a Pokémon ID and assigning unique IV stats. 


## Capturing Pokémon

In all Pokémon games, similar to stats, each Pokémon has a defined base catch rate. Once an encounter begins, that catch rate is adjusted through an advanced formula to account for variations in stats like level, hp, and speed. Better, more powerful Pokémon like legendaries are almost always harder to catch than less powerful Pokémon. Pokémon with lower capture rates often promote the concept of battling Pokémon with your own Pokémon before capturing. As your Pokémon attacks, the enemies Pokémon's hp is decreases, which then increases that Pokémon's catch rate.
However, since my game doesn't contains battling mechanics, as it focuses more on the catching experience, I created a small formula for catching Pokémon, which still uses the original base catch rates but doesn't allow for changes from stat variation of hp reduction by battling. 
```Python
        # Adjusted catch rate (Original formula based on the OG catch_rate)
        adjusted_catch_rate = ((base_catch_rate
                               / 1.5
                               )
                               * pokeball_mult)
        adjusted_catch_rate = min(adjusted_catch_rate, 100.0)  # cap catch_rate at 100%
```

### Throwing Pokéballs

During the catching sequence of the original and modern Pokemon games, trainers have always had the ability to choose the type of Pokéballs they throw. Some Pokéballs are inherently better than others, such as the ultraball increasing the catch rate above greatballs. But, some Pokéballs also have unique effects, such a weather, nighttime, and type matching boosts.  

Unfortunately, my game doesn't include weather patterns, locations, or any other unique elements that would favor a certain Pokéball type over another. In conjunction, given the chance to choose between an evidently strong ball and a weak ball, a player would choose to use the stronger ball every time. Therefore, I have a weighted random roll that determines whether the trainer throws a Pokéball, Greatball, Ultraball, or Masterball (100% catch rate), with stronger balls having a lower probability. In python, once the weighted roll picks a number, it matches that number to the Primary Key in the SSMS Pokéball table.

In the future, I would like to explore giving a finite number of stronger balls to the trainer at the start and allow them to choose what balls they throw. This would encourage a strategy to save stronger balls for stronger Pokémon. 

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

#### 1. The Pokémon broke free -

This result is dependent on the uniform roll of the catch rate compared to the catch rate percentage of the Pokémon. If the roll is greater than the catch rate, the Pokémon breaks free.
```Python
  # Perform the catch roll
        roll = random.uniform(0, 100)
        caught = roll < adjusted_catch_rate
```

#### 2. The Pokémon runs away -

if a trainer has an unsuccessful attempt at capturing a Pokémon, there's a 25% chance the Pokémon will run away and be uncatchable. This returns "pokemon_escaped".
```Python
            escape_roll = random.randint(1, 4)
            if escape_roll == 1:
                return "pokemon_escaped!"
```

#### 3. The trainer chooses to run away -

If the Pokémon does not run away, the trainer can choose to run away instead, leaving that Pokémon behind to encounter a new one. This returns "you_escaped".
```Python
                  another_try = input("\nWould you like to throw another Pokéball? \n "
                                        "1) Yes\n "
                                        "2) Encounter new Pokémon\n> "
                                        ).strip().upper()
```

#### 4. The Pokémon is caught -

This result is also dependent on the same uniform roll as the Pokémon breaking free. If the roll is less than the catch rate, the Pokémon is considered caught. This returns "caught"
```Python
  # Perform the catch roll
        roll = random.uniform(0, 100)
        caught = roll < adjusted_catch_rate
```

##### To summarize, there are three potential return possibilites after throwing a Pokéball. Each of them branch off into various triggers.
- "Pokemon_escaped" - Branches into menu asking for new encounter
- "You_escaped" - Branches into menu asking for new encounter
- "Caught" - Branches into the caught action, recording the capture in the database and increasing the capture count of their game. 


### Successful Pokémon Capture Database Trigger:
Once a Pokémon is caught, I built python trigger to create another row in the database with all of the Pokémon's information and unique IVs, which creates a sequential instance_id in SSMS. The trainer_id is also attached to the captured Pokémon so that it can be joined to the trainer table for an official Pokedex. 

```Python
          cursor.execute(
                """INSERT INTO 
                         trainer_pokemon (trainer_id, pokedex_id, pokemon_name, iv_hp, iv_attack, iv_defense, iv_sp_attack, iv_sp_defense, iv_speed, level, pokeball_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (trainer_id, pokedex_id, pokemon_name, final_hp, final_attack, final_defense, final_sp_atk, final_sp_def, final_speed, level, pokeball_id)
            )
```

## Building a Pokedex of Captured Pokémon.

Once a Pokémon is caught, trainers are given access to their Podex, which catalogs the Pokémon they've caught. It includes both the general information of each captured Pokémon along with their IV_stats that were calculated during the encounter. Each additional capture adds to the Pokedex, and each successful capture gives menu access to view a newly updated Pokedex.

The pokedex is built by utilizing the trainer_pokemon, pokemon_species, and pokeball tables. The trainer_pokemon table contains the unique captured Pokémon and their IV stats, the pokemon_species table includes the generation information related to each Pokémon (name, type, game of origin, etc.), and the pokeball table gives us the Pokéball name used to capture the Pokémon. Even though the caught Pokémon of each trainer exists in the trainer_pokeball table, we can use the trainers trainer_id to limit results to their captured Pokémon.  

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

To allow infinite encounters and catch attempts with Pokémon, loops needed to be developed to constantly reroute the player. 

This diagram represents the main gameplay loop used in the game:

<img width="1700" height="1024" alt="Game Loop (5)" src="https://github.com/user-attachments/assets/ce736fd4-4bb2-47ab-96d2-f1fb2faef00f" />


As shown, the menus, encounter system, and catch attempt system are separated. The encounter system is defined as "p" at the end of the encounter process, remaining defined until it is redefined by another encounter trigger. This allows the catch attempt system to use "p" to pull the most recently encountered Pokémon, excluding any of the Pokémon encountered previously that were also "p". Then, these menus and systems are looped back based on the result of the catch attempt or a menu choice.

## Game storyline triggers.

When starting a new game, each trainer is given a capture count of 0, and each Pokémon capture increases that count. When continuing a previous game, the capture count is defined through a query that counts the total Pokémon caught associated with the trainer_id.

- Continuing previous game:
  
```Python
      cursor.execute("""select count(pokedex_id) from trainer_pokemon a where a.trainer_id = ?""", (trainer_id,))
        capture_count = cursor.fetchone()[0]
```

After the player catches their first Pokémon, Professor Oak is triggered to begin his dialogue and deliver a Pokedex. Once delivered, a trainer has access to the menu options that include viewing their current Pokedex. This is done by gatekeeping the option based on the capture count.

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

After the player has their third capture, Team Rocket appears in attempt to steal the trainer's Pokémon. The trainer is knocked out, but saved by a nearby trainer who heard the commotion. The trainer then awakes to Nurse Joy and professor Oak in a Pokémon health center. 

Once the player catches four Pokémon, they are given access to the "Type Scanner" and "Electric Stabalizer device". These devices are then used in the Kirin region to capture electric Pokémon and finalize Professor Oak's sample. 

### Electric Stabilizer:

Obtaining this device activates a different pool of Pokémon to reflect entering the Kirin region. I hand picked the Pokémon in the Kirin region to allow for more objective oriented gameplay -

```Python
 capture_count = cursor.fetchone()[0]
        electric_stabilizer = 0

    # Begin encounter
    while True:
        if capture_count > 3 and electric_stabilizer <= 100:
                fixed_pokedex_ids = [25, 135, 125,642,172,466,881,796,479,95,383,445,450,464,389,75,922,995,989]
                p = encounter(fixed_pokedex_ids)
        else:
            p = encounter()
```
Each electric Pokémon captured adds to the stabilizer percentage. Stronger Pokémon add more percentage, while legendaries automatically set the percentage to 100%.

```Python
            if electric_id in (796,642): #Xurkitree and Thunderous
                electric_stabilizer += 100
                print("+100% (Legendary Bonus)")
            elif electric_id in (172,479):
                electric_stabilizer += 20
                print("+25%")
            elif electric_id in (989,466):
                electric_stabilizer += 40
                print("+40%")
            elif "Electric" in (type_1, type_2):
                electric_stabilizer += 25
                print("+30%")
```

### Type Scanner:

The type scanner shows the trainer the type of the Pokémon they have encountered. It's gatekept until the electric stabilizer is obtain.

```Python
print("\nWould you like to throw a Pokéball?")
            print("1) Yes")
            print("2) Encounter new Pokémon")
            if capture_count > 3:
                print("3) Scan Pokemon Type")

            want_throw = input("> ").strip()

            # Loop for invalid options
            valid_choices = {"1", "2"}
            if capture_count > 3:
                valid_choices.add("3")
            while want_throw not in valid_choices:
                select_option_se()
                print("\nPlease enter a valid option.")
                print("\nWould you like to throw a Pokéball?")
                print("1) Yes")
                print("2) Encounter new Pokémon")
                if capture_count > 3:
                    print("3) Scan Pokémon Type")
                want_throw = input("> ").strip()
```


## The Ending
After the electric stabilizer reaches 100%, the game is successfully completed, rewarding the player with a special message from professor Oak and victory music from the original games. Once the game is complete, the player still has the opportunity to encounter and capture more Pokémon to add to their pokedex, but can no longer access the Kirin region.

Thanks for reading!











