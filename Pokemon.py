# Import Packages
import pyodbc
import matplotlib.pyplot as plt
from PIL import Image
import pygame
import random
import math
from tabulate import tabulate
import time
import sys

# Initialize pygame music
pygame.mixer.init()

# Connect to SSMS
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=HavensPC;'
    'DATABASE=Pokemon;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()


# import images of Pokemon
#
# def download_pokemon_image(id, name):
#     url = f"https://pokeapi.co/api/v2/pokemon/{id}"
#     data = requests.get(url).json()
#
#     img_url = data["sprites"]["other"]["official-artwork"]["front_default"]
#     img_data = requests.get(img_url).content
#
#     with open(f"pokemon_images/{name.lower()}.png", "wb") as f:
#         f.write(img_data)

#
# for i in range(1, 1025):
#     download_pokemon_image(i, f"pokemon_{i}")



# Begin opening theme music
pygame.mixer.music.load(
    "C:\\Users\\haven\\Downloads\\Pokémon Red & Blue Music_ Opening Theme.mp3")
pygame.mixer.music.play(-1) #Plays until encounter

# Define type_text used to mimic talking
def type_text(text, speed=0.1):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(speed)
    print()

# Define sound effect for choosing menu options
def select_option_se():
    sfx_channel = pygame.mixer.Channel(1)
    select_option = (pygame.mixer.Sound
                     ("C:\\Users\\haven\\Downloads\\Pokemon select option SE (1).mp3"))
    sfx_channel.play(select_option)

# Begin Introduction

type_text("\nBooting up...", speed=0.2)

# Determine new game vs continue previous game
new_game_question =(input("\nWould you like to create a new game?\n "
                          "1) Yes\n "
                          "2) Continue previous game\n> "
                          ))
# Loop question
while new_game_question not in {"1","2"}:
    select_option_se()
    print ("\nPlease enter a valid option.")
    new_game_question =(input("\nWould you like to create a new game?\n "
                          "1) Yes\n "
                          "2) Continue previous game\n> "
                          ))

select_option_se()

# Branch for new game
if new_game_question == '1':
    type_text("\nHello", speed=0.2)
    type_text("...", speed=0.7)
    type_text("\nWhat do you like to be called?",speed=0.)
    trainer_name = input("> ")
    select_option_se()
    print("\nProfessor Oak:", end=" ")
    type_text('Greetings, ' + trainer_name + '!',speed=0.1)
    time.sleep(0.5)
    type_text("\nWelcome to the world of Pokémon! I'm professor Oak, the leading scientist studying these fascinating creatures we call Pokémon.",speed=0.06)
    type_text("I'm running some tests on Pokémon to develop a new revive serum, but I've run out of samples.",speed=0.06)
    type_text("To continue my work, I'm looking for a Pokémon trainer to catch more Pokémon for me.",speed=0.06)

    # Trigger the generation of a unique trainer_id in SSMS and pull output
    cursor.execute(
        """
        INSERT INTO trainer (trainer_name, date_created)
            OUTPUT INSERTED.trainer_id
        VALUES (?, GETDATE())
        """, (trainer_name,))

    # Define new trainer_id from outcome

    trainer_id = cursor.fetchone()[0]
    # COMMIT TO SSMS
    conn.commit()

    # Ask question
    ready_question = (input("\nWould you help by catching 3 Pokémon?\n "
                            "1) Yes\n "
                            "2) No\n> "
                            ))

    # Loop question
    while ready_question not in {"1","2"}:
        select_option_se()
        print("\nPlease enter a valid option.")
        ready_question = (input("\nWould you help by catching 3 Pokémon?\n "
                                "1) Yes\n "
                                "2) No\n> "
                                ))

    select_option_se()

    # Define game script to allow both questions to lead into script
    def ready_initiation():

        type_text("\nGreat! Before heading off on your journey, you'll need these:",speed=0.06)
        print("\n******************************************")
        print("  Obtained a bundle of various Pokeballs")
        print("******************************************\n")

        # Obtain item sound effect
        sfx_channel = pygame.mixer.Channel(1)
        obtain_item = (pygame.mixer.Sound
                          ("C:\\Users\\haven\\Downloads\\Pokemon obtain Item SE.mp3"))
        sfx_channel.play(obtain_item)
        # Delay text for full sound effect
        while sfx_channel.get_busy():
            pygame.time.delay(10)

        type_text("These are Pokéballs - powerful devices you can use to capture and store the Pokémon you encounter.",speed=0.05)
        type_text("Just throw one at a Pokémon and try and catch it! Remember, stronger Pokémon are harder to catch than weaker Pokémon.",speed=0.05)
        type_text("However, if you throw a stronger pokeball, your chances improve.",speed=0.05)
        type_text("Good luck!\n", speed=0.05)
        type_text("...", speed=0.6)

        # Computer initialization sound effect
        sfx_channel = pygame.mixer.Channel(1)
        computer_initialize = (pygame.mixer.Sound
                         ("C:\\Users\\haven\\Downloads\\Pokemon Computer SE.mp3"))
        sfx_channel.play(computer_initialize)

        print("Computer:", end=" ")
        type_text("Starting your adventure!")
        type_text("...", speed=0.6)
        print(f"\nTrainer Name: {trainer_name}")
        type_text(f"Here's your trainer ID: {trainer_id}")

        # New ID sound effect
        sfx_channel = pygame.mixer.Channel(1)
        new_id = (pygame.mixer.Sound
                          ("C:\\Users\\haven\\Downloads\\Pokemon Give ID SE (1).mp3"))
        sfx_channel.play(new_id)
        # Delay for sound effect
        while sfx_channel.get_busy():
            pygame.time.delay(10)

        type_text("You'll need it to continue your progress if you leave. Write it down!",speed=0.07)

    # Branch question - use defined ready_initiation for both options
    if ready_question == '1':
        ready_initiation()
    else:
        type_text("\nWell", speed=0.1)
        type_text("...", speed=0.6)
        type_text("I'm sending you in anyways! Let's act like you said yes.", speed=0.06)
        type_text("...", speed=0.6)
        ready_initiation()

# Branch for "continue game option"
else:
    # Define trainer_id to allow return of values (yes it should probably be before else)
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


    trainer_name, trainer_id = trainer_id_check()
    print(f"\nWelcome back, {trainer_name}!")

start_encounter_question = input("\nStart an encounter?\n "
                                 "1) Yes\n "
                                 "2) Exit Game\n> "
                                 )
# Loop for invalid options
while start_encounter_question not in {"1","2"}:
    select_option_se()
    print("\nPlease enter a valid option.")
    start_encounter_question = input("\nStart an encounter?\n "
                                     "1) Yes\n "
                                     "2) Exit Game\n> "
                                     )

# Branch question for starting encounter or exiting game
if start_encounter_question == '1':
    print("\nStarting an encounter...")
else:
    print("Goodbye, see you next time!")
    sys.exit()

# Stop initialization music before encounter
pygame.mixer.music.stop()

# Define encounter with a random Pokemon
def encounter():
    import random

    # Battle Music (Background loop)
    pygame.mixer.music.load("C:\\Users\\haven\\Downloads\\Trainer Battle - Pokémon Red_Blue_Yellow Soundtrack.mp3")
    pygame.mixer.music.play(-1)  # -1 loops forever

    # Pick a random Pokémon to encounter
    pokedex_id = random.randint(1,1025)

    # Use pokedex_id to pull base Pokemon stats
    cursor.execute(
        """SELECT * FROM pokemon_species WHERE pokedex_ID = ?""", (pokedex_id,))
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]

    # Extract the first row
    row = rows[0]

    # Assign base stats using index
    pokemon_data = {
    "pokedex_id": row[0],
    "pokemon_name": row[1],
    "legendary_type": row[2],
    "type_1": row[3],
    "type_2": row[4],
    "game_of_origin": row[5],
    "base_hp": row[6],
    "base_attack": row[7],
    "base_defense": row[8],
    "base_sp_attack": row[9],
    "base_sp_defense": row[10],
    "base_speed": row[11],
    "base_catch_rate": row[13],
    # Set level of pokemon (RANDOM)
    "level": random.randint(5, 30)
    }
    # Display image of pokemon with Matlab
    sprite = Image.open(f"pokemon_images/pokemon_{pokedex_id}.png")
    sprite_small = sprite.resize((150, 150))

    fig, ax = plt.subplots()
    ax.imshow(sprite)
    ax.axis('off')
    fig.patch.set_alpha(0)  # Make figure background transparent
    plt.show()

    # Print encounter info

    type_text(f"\nYou've encountered a {pokemon_data['pokemon_name']}!")

    if pokemon_data['legendary_type'] == "Legendary":
        print(f"{pokemon_data['pokemon_name']} is a legendary type!\n")
        time.sleep(1)
    elif pokemon_data['legendary_type'] == "Sub-Legendary":
        print(f"{pokemon_data['pokemon_name']} is a sub-legendary type!\n")
        time.sleep(1)
    elif pokemon_data['legendary_type'] == "Mythical":
        print(f"{pokemon_data['pokemon_name']} is a mythical type!\n")
        time.sleep(1)
    print("Level:", pokemon_data["level"])
    print("HP:", pokemon_data["base_hp"])
    # Return index for catch attempt on same Pokemon
    return pokemon_data


# if answer5 == 'Y':
#     catch_result = catch_attempt(p)
#     if catch_result == "Captured":
#         # to do later
#     elif catch_result == "escaped"

def catch_attempt(p):
    # Unpack values from the unique encounter (p)
    base_catch_rate = float(p["base_catch_rate"])
    base_hp = p["base_hp"]
    base_attack = p["base_attack"]
    base_defense = p["base_defense"]
    base_sp_attack = p["base_sp_attack"]
    base_sp_defense = p["base_sp_defense"]
    base_speed = p["base_speed"]
    level = p["level"]
    pokemon_name = p["pokemon_name"]
    pokedex_id = p["pokedex_id"]
    type_1 = p["type_1"]
    type_2 = p["type_2"]

    # Loop for repeated throws
    while True:
        # Choose a random Pokéball type
        # unique integers associated with each Pokeball type in SSMS: 1-4
        numbers = [1, 2, 3, 4]
        # Assign lower probability for stronger pokeballs
        probabilities = [0.5, 0.3, 0.15, 0.05]
        # Extract id
        pokeball_id = random.choices(numbers, probabilities, k=1)[0]

        # Use pokeball_id to extract pokeball information
        cursor.execute("SELECT * FROM pokeball WHERE pokeball_id = ?", (pokeball_id,))
        row = cursor.fetchone()
        # Allow error for table issues
        if not row:
            print("Invalid pokeball id from DB. Aborting throw.")
            return "escaped"

        pokeball_name = row[1]
        pokeball_mult = float(row[2])

        # Adjusted catch rate (Original formula based on the OG catch_rate)
        adjusted_catch_rate = ((base_catch_rate
                               / 2.0
                               )
                               * pokeball_mult)
        adjusted_catch_rate = min(adjusted_catch_rate, 100.0)  # cap catch_rate at 100%

        # Throw Pokeball sound effect
        sfx_channel = pygame.mixer.Channel(1)
        pokeball_sound = pygame.mixer.Sound(
            "C:\\Users\\haven\\Downloads\\Pokeball Throw Sound Effect Gen 8.mp3")
        sfx_channel.play(pokeball_sound)

        # Display pokeball type and adjusted_catch_rate
        if pokeball_name.lower() == "ultraball":
            type_text(f"\nYou threw an {pokeball_name}!\n",speed = 0.08)
        else:
            type_text(f"\nYou threw a {pokeball_name}!\n",speed = 0.08)

        print("Catch Rate:", f"{adjusted_catch_rate:.1f}%\n")

        # Generate unique IVs of encounter (Original Pokemon formula)
        # define random integer to use during formula
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

        headers = ["Stat", "Value"]
        stats = [
            ["Pokedex ID", pokedex_id],
            ["Pokemon Name", pokemon_name],
            ["Type 1", type_1],
            ["Type 2", type_2],
            ["HP", final_hp],
            ["Attack", final_attack],
            ["Defense", final_defense],
            ["Sp. Atk", final_sp_atk],
            ["Sp. Def", final_sp_def],
            ["Speed", final_speed],
            ["Level", level],
        ]

        # Perform the catch roll
        roll = random.uniform(0, 100)
        caught = roll < adjusted_catch_rate

        # Play the roll animation text
        # Random amount of rolls 1-3 - regardless of adjusted_catch_rate
        pokeball_roll = random.randint(1, 3)

        # Pokeball wobble sound effect
        sfx_channel = pygame.mixer.Channel(1)
        pokeball_sound = pygame.mixer.Sound(
            "C:\\Users\\haven\\Downloads\\Single Wobble (2).mp3")

        # Activate sound effect for each roll
        for _ in range(pokeball_roll):
            sfx_channel.play(pokeball_sound)

            type_text("The Pokéball rolls...",speed = 0.1)

            while sfx_channel.get_busy():
                pygame.time.delay(10)

        # Begin successful catch branch
        if caught:
            print(f"\nYou caught {p['pokemon_name']}!\n")
            # Insert stats into database
            cursor.execute(
                """INSERT INTO trainer_pokemon 
                   (trainer_id, pokedex_id, pokemon_name, iv_hp, iv_attack, iv_defense, iv_sp_attack, iv_sp_defense, iv_speed, level, pokeball_id)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (trainer_id, pokedex_id, pokemon_name, final_hp, final_attack, final_defense, final_sp_atk, final_sp_def, final_speed, level, pokeball_id)
            )
            #Committ to SSMS
            conn.commit()

            # Display inserted row
            cursor.execute(
                """
                SELECT TOP 1 *   
                FROM trainer_pokemon
                WHERE trainer_id = ?
                ORDER BY instance_id DESC
                """,
                (trainer_id,)
            )
            print(tabulate(stats, headers=headers, tablefmt="pretty"))
            row = cursor.fetchone()
            # print("What's added to the database:", row)

            # Return successful catch
            return "caught"

        #Begin unsuccessful catch branch
        else:
            print(f"{pokemon_name} broke free!")

            # Broke free sound effect
            sfx_channel = pygame.mixer.Channel(1)
            broke_free = (pygame.mixer.Sound
                              ("C:\\Users\\haven\\Downloads\\Pokemon Running Away sound effect.mp3"))
            sfx_channel.play(broke_free)
            time.sleep(0.5)

            # Chance for pokemon to run away from encounter
            escape_roll = random.randint(1, 4)
            if escape_roll == 1:
                return "pokemon_escaped!"
            else:
                # Ask to throw another pokeball
                another_try = input("\nWould you like to throw another Pokéball? \n "
                                "1) Yes\n "
                                "2) Encounter new Pokémon\n> "
                                ).strip().upper()
                # Loop for invalid options
                while another_try not in {"1", "2"}:
                    select_option_se()
                    print("Please enter a valid option.")
                    another_try = input("\nWould you like to throw another Pokéball? \n "
                                        "1) Yes\n "
                                        "2) Encounter new Pokémon\n> "
                                        ).strip().upper()
                if another_try == "1":
                    continue   # loop back to throw again at same Pokémon
                else:
                    return "you_escaped!"


# MAIN GAME LOOP

def main():
    # Set Pokedex to allow empty generation without error
    pokedex = []
    headers = []

    # Define menu option
    def again_option(capture_count, pokedex, headers):
        while True:
            print("\nWould you like to encounter a new Pokémon?")
            print("1) Yes")

            # Gatekeep Pokedex access before capture
            if capture_count > 0:
                print("2) View Pokédex")

            print("3) Exit Game")

            again_answer = input("> ").strip()

            select_option_se()

            # Assign valid options
            valid_choices = {"1", "3"}
            # add option to access Pokedex once a Pokemon has been caught
            if capture_count > 0:
                valid_choices.add("2")

            if again_answer not in valid_choices:
                print("\nThat's not a valid answer. Please try again.")
                continue # Loop back at menu

            if again_answer == "2":
                print(tabulate(pokedex, headers=headers, tablefmt="pretty"))
                continue # Loop back at menu

            if again_answer == "3":
                sys.exit()

            return again_answer

    # Set capture count to 0 if new game is created
    if new_game_question == "1":
        capture_count = 0
    else:
        # Pull capture count in continued game
        cursor.execute("""select count(pokedex_id) from trainer_pokemon a where a.trainer_id = ?""", (trainer_id,))
        capture_count = cursor.fetchone()[0]

    # Begin encounter
    while True:
        p = encounter()

        # Ask if player wants to try catching encountered Pokemon
        want_throw = input("\nWould you like to throw a Pokéball? \n "
                           "1) Yes\n "
                           "2) Encounter new Pokémon\n> "
                           ).strip().upper()
        # Loop for invalid options
        while want_throw not in {"1", "2"}:
            select_option_se()
            print("\nPlease enter 1 or 2.")
            want_throw = input("\nWould you like to throw a Pokéball? \n "
                               "1) Yes\n "
                               "2) Encounter new Pokémon\n> "
                               ).strip().upper()

        # If player want's to engage, initiate catch attempt and define result
        if want_throw == "1":
            result = catch_attempt(p)

            # Begin insertion into database if caught
            if result == "caught":
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
                                        left join trainer b
                                                  on a.trainer_id = b.trainer_id
                                        join pokemon_species c
                                             on a.pokedex_id = c.pokedex_id
                                        join pokeball d
                                             on a.pokeball_id = d.pokeball_id
                               where a.trainer_id = ?""", (trainer_id,))
                pokedex = cursor.fetchall()
                headers = ["pokemon_name", "pokedex_id", "level", "type_1", "type_2", "game_of_origin", "iv_hp",
                           "iv_attack", "iv_defense", "iv_sp_attack", "iv_sp_defense", "iv_speed", "pokeball_name"]

                # Increase capture count
                capture_count += 1

                print("Capture Count:", capture_count)

                # Stop battle music
                pygame.mixer.music.stop()
                # Start capture music
                sfx_channel = pygame.mixer.Channel(1)
                capture_sound = pygame.mixer.Sound(
                    "C:\\Users\\haven\\Downloads\\POKEMON - Capture Sound Effect [Free Ringtone Download].mp3")
                sfx_channel.play(capture_sound)
                while sfx_channel.get_busy():  # Wait until sound effect finishes
                    time.sleep(0.1)

                # Successful capture music besides third capture
                if capture_count != 3:
                    pygame.mixer.music.load(
                        "C:\\Users\\haven\\Downloads\\Pokémon Insurgence - Telnor Town.mp3")
                    pygame.mixer.music.play(1)  # Plays once

                # Begin dialogue after first capture
                if capture_count == 1:
                    print("\nProfessor Oak:", end=" ")
                    type_text(f"You caught your first Pokémon! You're already on your way to becoming a Pokémon master.",speed = 0.05)
                    type_text(f"{p['pokemon_name']} will be perfect for my first sample, but I still need a few more samples to refine my serum.",speed = 0.05)
                    type_text("Oh, before encountering more Pokémon, you'll need this:",speed = 0.05)
                    print("\n******************************************")
                    print("            Obtained a Pokédex")
                    print("******************************************\n")

                    # Obtain item sound effect
                    sfx_channel = pygame.mixer.Channel(1)
                    obtain_item = (pygame.mixer.Sound
                                      ("C:\\Users\\haven\\Downloads\\Pokemon obtain Item SE.mp3"))
                    sfx_channel.play(obtain_item)
                    while sfx_channel.get_busy():
                        pygame.time.delay(10)

                    type_text("This Pokédex catalogs the Pokémon you've caught. Here's what yours looks like so far:\n",speed = 0.05)

                    print(tabulate(pokedex, headers= headers, tablefmt="pretty"))

                    # View pokedex sound effect
                    sfx_channel = pygame.mixer.Channel(1)
                    pokedex_sound = (pygame.mixer.Sound
                                      ("C:\\Users\\haven\\Downloads\\Pokedex Sound.mp3"))
                    sfx_channel.play(pokedex_sound)
                    time.sleep(2)

                    type_text("\nAfter every capture, you'll have the option to view your Pokédex.",speed = 0.05)

                # Begin game completion dialogue
                if capture_count == 3:

                    pygame.mixer.music.load(
                        "C:\\Users\\haven\\Downloads\\Pokemon Red_Blue Ending.mp3")
                    pygame.mixer.music.play(-1)  # Plays until encounter

                    print("\nProfessor Oak:", end=" ")
                    type_text("You actually did it, nice job!! This is exactly what I need to make my revive serum.",speed = 0.06)
                    type_text("Once it's developed, I'll release it to every Pokémon health center in the area. It will cut the amount of time a Pokémon takes to heal in half!",speed = 0.06)
                    type_text("Don't let the completion of my research stop you from continuing your journey! Feel free to continue catching Pokémon to add to your Pokédex. You'll become a Pokémon master before you know it!",speed = 0.06)

                # Ask for a new encounter regardless of capture count
                # Use previous menu
                choice = again_option(capture_count, pokedex, headers)
                if choice == "3":
                    print("Goodbye, see you next time!")
                    break

            # Handle option for choosing to encounter new Pokemon
            elif result == "you_escaped!":
                print(f"\nYou ran away from {p['pokemon_name']}!")

            #Handle option for pokemon escaping from escape_roll
            if result == "pokemon_escaped!":
                print(f"\n{p['pokemon_name']} ran away!")
                time.sleep(0.5)
                print("\nProfessor Oak:", end=" ")
                type_text(f"It looks like {p['pokemon_name']} fled! Some Pokémon don't want to be caught. Try again with another Pokemon.",speed = 0.05)
                choice = again_option(capture_count, pokedex, headers)
        else:
            print(f"\nYou left the wild {p['pokemon_name']} alone.")

# Restrict running to file execution
if __name__ == "__main__":
    main()

