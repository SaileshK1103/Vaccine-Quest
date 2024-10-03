import mysql.connector

def create_connection():
    connection = mysql.connector.connect(
        user = 'sailesh',
        password = 'sailesh1103',
        host = 'localhost',
        port = '3306',
        database = 'flight_game',
        autocommit = True,
        charset = 'utf8mb4',
        collation = 'utf8mb4_unicode_ci'
    )
    return connection

def create_tables():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS player_profile (
            player_id INT AUTO_INCREMENT PRIMARY KEY,
            player_name VARCHAR(40) NOT NULL,
            email VARCHAR(255) NOT NULL,
            airport_ident VARCHAR(40) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
            FOREIGN KEY (airport_ident) REFERENCES airport(ident) ON DELETE CASCADE ON UPDATE CASCADE
            ) ENGINE=InnoDB;

        ''')

    cursor.execute('''
                CREATE TABLE IF NOT EXISTS player_game (
                player_id INT,
                money INT DEFAULT 5000,
                fuel INT DEFAULT 100,
                FOREIGN KEY (player_id) REFERENCES player_profile (player_id)
                ) ENGINE=InnoDB;
            ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vaccine_element (
            element_id INT AUTO_INCREMENT PRIMARY KEY,
            element_name VARCHAR(40) NOT NULL,
            description VARCHAR(100) NOT NULL,
            airport_ident VARCHAR(40) CHARACTER SET latin1 COLLATE latin1_swedish_ci,
            FOREIGN KEY (airport_ident) REFERENCES airport(ident)
            ) ENGINE=InnoDB;
        ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS player_inventory (
                player_id INT,
                element_id INT,
                collected BOOLEAN DEFAULT 0,
                FOREIGN KEY (player_id) REFERENCES player_profile(player_id),
                FOREIGN KEY (element_id) REFERENCES vaccine_element(element_id)
            ) ENGINE=InnoDB;
        ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_level (
                level_id INT AUTO_INCREMENT PRIMARY KEY,
                level_number INT NOT NULL,
                hint VARCHAR(255) NOT NULL,
                budget INT NOT NULL,
                fuel_cost INT NOT NULL
            )
        ''')

    cursor.close()
    connection.close()

def drop_table():
    connection = create_connection()
    cursor = connection.cursor()
    # Disable foreign key checks
    cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')

    # Drop all tables
    #cursor.execute('DROP TABLE IF EXISTS player_inventory;')
    #cursor.execute('DROP TABLE IF EXISTS player_game;')
    #cursor.execute('DROP TABLE IF EXISTS vaccine_element;')
    cursor.execute('DROP TABLE IF EXISTS player_profile;')
    #cursor.execute('DROP TABLE IF EXISTS game_level;')
    #cursor.execute('DROP TABLE IF EXISTS goal_reached;')
    #cursor.execute('DROP TABLE IF EXISTS goal;')
    #cursor.execute('DROP TABLE IF EXISTS game;')

    # Enable foreign key checks back
    cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')

    cursor.close()
    connection.close()

#drop_table()
