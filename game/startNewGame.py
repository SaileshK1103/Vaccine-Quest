import uuid

from databasae.databaseConnection import create_connection

# Player registration function
def register_player(player_name,email,airport_ident):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO player_profile (player_name,email,airport_ident) VALUES (%s,%s,%s)",
                   (player_name,email,airport_ident))
    connection.commit()
    player_id = cursor.lastrowid
    connection.close()
    return player_id

# Initialize game settings
def initialize_game(player_id, airport_ident):
    return {
        'player_id': player_id,
        'money': 5000,
        'fuel': 100,
        'airport_ident': airport_ident,
        'inventory': {}
    }

# Travel function
def travel(game_state, destination):
    print(f"Travelling to {destination}")
    game_state['fuel'] -= 10 #simulate fuel deduction
    if game_state['fuel'] <= 0:
        print("You have run out of fuel!")
        return False
    else:
        return True

# Collect element function
def collect_element(game_state, element_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO player_inventory (player_id, element_id, collected) VALUES (%s, %s,%s)",
                       (game_state['player_id'], element_id,1))
    connection.commit()
    connection.close()
    game_state['inventory'][element_id] = True
    print(f"Collected element ID: {element_id}")

# Check inventory function
def check_inventory(game_state):
    print("Your inventory:")
    for element_id in game_state['inventory'].keys():
        print(f"Element ID: {element_id}")

# Hint function

def get_hint(level):
    hints = {
        1: "Travel to the airport known for its icy cold conditions to find the base solution.",
        2: "Head to the next airport for an essential ingredient.",
    }
    return hints.get(level, "No more hints available.")