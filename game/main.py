from game.startNewGame import startNewGame


def main():
    player_name = input("Enter your screen name: ")
    game_id = startNewGame(player_name )
    print("Welcome to the flight game!")
    while True:
        current_airport = input("Enter your airport name: ")
        destination_airport = input("Enter your destination airport name: ")
main()
