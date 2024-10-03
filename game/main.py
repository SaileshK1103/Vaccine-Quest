from databasae.databaseConnection import create_tables, drop_table
from game.startNewGame import initialize_game, travel, collect_element, check_inventory, get_hint, register_player


def main():
    create_tables()
    #drop_table()
    print("Welcome to Quest Vaccine Game!")
    player_name = input("Enter your name: ")
    email = input("Enter your email: ")
    player_id = register_player(player_name,email)
    game_state = initialize_game(player_id)
    current_level = 1

    while True:
        print(f"\n You are at your base station: {game_state['base_airport']}")
        print(f"Money: $ {game_state['money']} | Fuel: {game_state['fuel']}")
        print("Actions: 1. Travel 2. Check Inventory 3. USe Hint 4. Formulate Vaccine 5. Quit")
        action = input("Choose your action: ")

        if action == "1":
            destination = input("Enter the destination airport")
            if travel(game_state, destination): # Simulate collecting an element
                collect_element(game_state,1)
                current_level +=1
                if current_level > 2: # assume element id 1 is collected
                    print("You have completed the game!")
                    break
        elif action == "2":
            check_inventory(game_state)
        elif action == "3":
            print("Hint", get_hint(current_level))
        elif action == "4":
            print("Formulating the vaccine...(not yet implemented)")
if __name__ == "__main__":
    main()