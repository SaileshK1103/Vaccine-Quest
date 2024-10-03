import uuid

from databasae.databaseConnection import create_connection


def startNewGame(screen_name):
    connection = create_connection()
    cursor = connection.cursor()
    game_id = str(uuid.uuid4())
    initial_co2_budget = 10000
    initial_location = "EFHK"  # Example airport

    insert_query = ("INSERT INTO game (id, co2_consumed, co2_budget, location, screen_name) "
                    "VALUES (%s, %s, %s, %s, %s)")
    cursor.execute(insert_query, (game_id, 0, initial_co2_budget, initial_location, screen_name))
    connection.commit()

    cursor.close()
    connection.close()

    return game_id