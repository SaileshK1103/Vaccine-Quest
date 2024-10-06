from random import random, shuffle, choice
from geopy.distance import geodesic

import mysql.connector
connection = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='vaccine_game',
    user='xxx',
    password='xxx',
    charset='utf8mb4',
    collation='utf8mb4_unicode_ci'
)

def get_airports():
    sql = '''SELECT iso_country, ident, name, type, latitude_deg, longitude_deg 
    FROM airport 
    WHERE continent = 'EU' 
    AND type='large_airport'
    ORDER BY RAND() 
    LIMIT 30; '''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

# Helper function to get element name by ID
def get_element_name_by_id(element_id):
    sql = "SELECT name FROM element WHERE id = %s;"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (element_id,))
    result = cursor.fetchone()
    return result['name'] if result else None

def create_game(start_money, p_range, cur_airport, p_name, a_ports):
    cursor = connection.cursor(dictionary=True)
    # Insert new game
    sql = "INSERT INTO game (money, player_range, location, screen_name) VALUES (%s, %s, %s, %s);"
    cursor.execute(sql, (start_money, p_range, cur_airport, p_name))
    g_id = cursor.lastrowid

    # Get all elements and their quantities
    sql = "SELECT id, name, total_quantity FROM element;"
    cursor.execute(sql)
    elements = cursor.fetchall()

    # Create a list of all elements based on their quantities
    element_list = []
    for elem in elements:
        element_list.extend([elem['id']] * elem['total_quantity'])  # Using element ID

    # Shuffle elements for random distribution
    shuffle(element_list)

    # Assign elements to airports ensuring different airports
    assigned_airports = set()
    # Ensure the first airport does not get assigned an element
    assigned_airports.add(cur_airport)  # Add current airport as already assigned
    for elem_id in element_list:
        # Filter airports that are not yet assigned
        available_ports = [port for port in a_ports if port['ident'] not in assigned_airports]
        if not available_ports:
            raise Exception("Not enough unique airports to assign all elements.")
        selected_port = choice(available_ports)
        assigned_airports.add(selected_port['ident'])
        # Insert into port_contents
        element_name = get_element_name_by_id(elem_id)
        sql = "INSERT INTO port_contents (game_id, airport, content_type, content_value) VALUES (%s, %s, %s, %s);"
        cursor.execute(sql, (g_id, selected_port['ident'], 'element', element_name))

    # Assign 3 lucky boxes to different airports
    for _ in range(3):
        # Filter airports not yet assigned
        available_ports = [port for port in a_ports if port['ident'] not in assigned_airports]
        if not available_ports:
            raise Exception("Not enough unique airports to assign all lucky boxes.")
        selected_port = choice(available_ports)
        assigned_airports.add(selected_port['ident'])
        # Insert into port_contents
        sql = "INSERT INTO port_contents (game_id, airport, content_type) VALUES (%s, %s, %s);"
        cursor.execute(sql, (g_id, selected_port['ident'], 'lucky_box'))

    return g_id

# Get airport info
def get_airport_info(icao):
    sql = '''SELECT iso_country, ident, name, latitude_deg, longitude_deg
             FROM airport
             WHERE ident = %s'''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    return result

# Check if current airport has content (element or lucky box)
def check_port_contents(g_id, cur_airport):
    sql = """SELECT id, content_type, content_value, found 
             FROM port_contents 
             WHERE game_id = %s AND airport = %s;"""
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (g_id, cur_airport))
    result = cursor.fetchall()
    return result

# Calculate distance between two airports
def calculate_distance(current, target):
    start = get_airport_info(current)
    end = get_airport_info(target)
    return geodesic((start['latitude_deg'], start['longitude_deg']),(end['latitude_deg'], end['longitude_deg'])).km

# Get airports in range
def airports_in_range(icao, a_ports, p_range):
    in_range = []
    for a_port in a_ports:
        dist = calculate_distance(icao, a_port['ident'])
        if dist <= p_range and dist != 0:
            in_range.append(a_port)
    return in_range

# Update location and player stats
def update_location(icao, p_range, u_money, g_id):
    sql = '''UPDATE game SET location = %s, player_range = %s, money = %s WHERE id = %s'''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (icao, p_range, u_money, g_id))

# Mark content as found
def mark_content_found(content_id):
    sql = "UPDATE port_contents SET found = 1 WHERE id = %s;"
    cursor = connection.cursor()
    cursor.execute(sql, (content_id,))


# Function to buy extra range
def buy_extra_range(player_range, money):
    while True:
        # Ask the player how much range they want to buy
        range_to_buy = input("How much range do you want to buy? (in km, multiples of 100): ").strip()

        # Validate the input
        try:
            range_to_buy = int(range_to_buy)
            if range_to_buy <= 0 or range_to_buy % 100 != 0:
                print("Please enter a valid amount (must be a positive multiple of 100).")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        # Calculate cost
        cost = (range_to_buy // 100) * 100

        # Check if the player has enough money
        if cost > money:
            print(f"You don't have enough money. You need ${cost} but only have ${money}.")
            continue

        # Deduct the cost and update the range
        money -= cost
        player_range += range_to_buy
        print(f"You bought an extra {range_to_buy}km of range.")
        print(f"New range: {player_range}km, Remaining money: ${money}")
        break  # Exit the loop after successful purchase

    return player_range, money

# GAME STARTS
# Ask to show the story
storyDialog = input('Do you want to read the background story? (Y/N): ')
if storyDialog.upper() == 'Y':
    print("Your mission is to fly to different airports to collect essential elements (A, B, C, D) needed to create a vaccine.")
    print("Each element has a limited number available in the game.")
    print("A random airport will also contain a lucky box, which costs $100 to open.")
    print("The lucky box may contain an additional element or be empty.")
    print("If you collect all required elements within the budget provided at the start of the game, you win!")

# GAME SETTINGS
print('Press enter to start! ')
player = input('Type player name: ')
game_over = False
win = False

# Start money = 1000
money = 1000
# Start range in km = 6000
player_range = 6000

# Elements collected
collected_elements = []

# All airports
all_airports = get_airports()
# Start_airport ident
start_airport = all_airports[0]['ident']

# Current airport
current_airport = start_airport

# Create game and assign contents
try:
    game_id = create_game(money, player_range, start_airport, player, all_airports)
except Exception as e:
    print(f"Error creating game: {e}")
    connection.close()
    exit()

# GAME LOOP
while not game_over:
    # Get current airport info
    airport = get_airport_info(current_airport)
    print(f"You are at {airport['name']}(ICAO: {airport['ident']}).base airport:{start_airport}")
    print(f"You have ${money:.0f} and {player_range:.0f}km of range.")

    # Option to buy extra range
    buy_range = input('Do you want to buy extra range? (Y/N): ').strip().upper()
    if buy_range == 'Y':
        if money < 100:  # Check if the player has money to buy any range
            print("You don't have enough money to buy extra range.")
        else:
            player_range, money = buy_extra_range(player_range, money)

    # Pause
    input("\033[32mPress Enter to continue...\033[0m")

    # Show airports in range
    airports = airports_in_range(current_airport, all_airports, player_range)
    print(f"\033[34mThere are {len(airports)} airports in range:\033[0m")
    if len(airports) == 0:
        print('You are out of range.')
        game_over = True
        break  # Exit the loop if there are no airports in range
    else:
        print("Airports:")
        for airport in airports:
            ap_distance = calculate_distance(current_airport, airport['ident'])
            print(f"{airport['name']}, ICAO: {airport['ident']}, Distance: {ap_distance:.0f}km")

    # Ask for destination only if there are airports in range
    dest = input('Enter destination ICAO: ').strip().upper()
    # Validate destination
    dest_airports = [airport['ident'] for airport in airports]
    if dest not in dest_airports:
        print("Invalid destination. Please choose an airport within range.")
        continue
    # calculate distance to destination
    selected_distance = calculate_distance(current_airport, dest)
    if selected_distance > player_range:
        print("You don't have enough range to fly to this destination.")
        continue
    player_range -= selected_distance
    update_location(dest, player_range, money, game_id)
    current_airport = dest
    if player_range < 0:
        game_over = True
    # Check for contents at new airport
    contents = check_port_contents(game_id, current_airport)
    for content in contents:
        if content['found'] == 0:
            if content['content_type'] == 'element':
                # Automatically collect the element
                collected_elements.append(content['content_value'])
                print(f"You found Element {content['content_value']} at {airport['name']}!")
                mark_content_found(content['id'])
            elif content['content_type'] == 'lucky_box':
                # Ask if the player wants to open the lucky box
                question = input('Do you want to open the lucky box by $100? (Y/N): ')
                if question.upper() == 'Y':
                    if money >= 100:
                        money -= 100
                        # Randomly decide the lucky box content
                        lucky_box_result = choice(['A', 'B', 'C', 'D', 'Empty'])
                        if lucky_box_result in ['A', 'B', 'C', 'D']:
                            if lucky_box_result in collected_elements:
                                print(f"The lucky box is empty. You already have Element {lucky_box_result}.")
                            else:
                                collected_elements.append(lucky_box_result)
                                print(f"Congratulations! You found Element {lucky_box_result} in the lucky box.")
                        else:
                            print('The lucky box is empty.')
                        mark_content_found(content['id'])
                    else:
                        print("You don't have enough money to open the lucky box.")


# GAME OVER
# Show game result
print(f"{'You won!' if win else 'You lost!'}")
if win:
    print(f"Congratulations! You collected all required elements: {', '.join(collected_elements)}.")
else:
    print(f"You have ${money:.0f} left and {player_range:.0f}km of range remaining.")

# Show collected elements regardless of win/loss
if collected_elements:
    print(f"You collected the following elements: {', '.join(collected_elements)}.")
else:
    print("You didn't collect any elements.")
