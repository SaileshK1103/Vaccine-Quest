### Introduction
Vaccine Quest is a text-based adventure game that simulates a challenging scenario where players must gather resources to formulate a life saving vaccine.
The primary objective of the game is to fly through different airports, collect crucial vaccine components, and return to the base airport to complete 
the vaccine formulation.

### Game Storyline

The world is facing a critical shortage of COVID-19 vaccines, and the player must travel to different locations to gather the necessary elements to create a potent vaccine. 
The game takes players through multiple levels, each with unique hints and resource constraints. The final goal is to formulate the vaccine and distribute it to several 
affected regions, saving many lives as possible.

### Game Mechanics
The game is structured into different levels, each with increasing difficulty. Players must balance between managing their fuel and money while gathering the required vaccine elements. 
Failure to plan correctly will result in running out of resources, potentially costing lives. 

- Base Airport: The starting and ending point for the game. Players must return here to complete the vaccine formulation. 

- Levels: Each level introduces a new hint for collecting specific elements, requiring the player to decide the best route and manage resources carefully. 

- Hints: Provided before each level, offering clues to the player about where to find the next element. 

- Budget & Fuel: Players have a limited budget and fuel supply. They need to plan their trips accordingly. 

- Inventory Management: The player must pick up the elements one by one, ensuring the correct components are gathered for the vaccine. 

### Databse Design
- Drop all tables except airport and country,creat new tables : game, element and port_contents. sql query as below:

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS game;
DROP TABLE IF EXISTS goal;
DROP TABLE IF EXISTS goal_reached;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE game (
    id INT AUTO_INCREMENT PRIMARY KEY,
    money DECIMAL(10, 2) NOT NULL,
    player_range DECIMAL(10, 2) NOT NULL,
    location VARCHAR(10) NOT NULL,
    screen_name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP );

CREATE TABLE port_contents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT NOT NULL,
    airport VARCHAR(10) NOT NULL,
    content_type ENUM('element', 'lucky_box') NOT NULL,
    content_value CHAR(1) DEFAULT NULL,
    found TINYINT(1) DEFAULT 0 );

CREATE TABLE element (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name CHAR(1) NOT NULL,  -- Values like A, B, C, D
    total_quantity INT NOT NULL  -- Quantities: A:4, B:3, C:3, D:2
     );

INSERT INTO element (name, total_quantity) VALUES ('A', 4), ('B', 3), ('C', 3), ('D', 2) ON DUPLICATE KEY UPDATE name = VALUES(name), total_quantity = VALUES(total_quantity);

### Game Flow
### Links：
- [Trello board](https://trello.com/b/GG9OKmbC/challenger-flight-game-project)
- [Project tracking sheet](https://docs.google.com/spreadsheets/d/1vuq3BxNBDeG4BTiAt0iLGx4ohJ9QgnmPnivLulsLMhw/edit?gid=0#gid=0)
