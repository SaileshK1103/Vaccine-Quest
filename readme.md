### 1.Introduction

The purpose of this document is to provide a detailed and comprehensive requirement specification for the Game "Vaccine Quest". The document is targeted towards developers, project stakeholders, and testers, outlining the exact functionalities and requirements of the game. It aims to eliminate ambiguities in the development process, ensuring a common understanding of how the game should work and how users will interact with it. The document is organized into four main chapters: Introduction, Vision, Functional Requirements, and Quality Requirements.

### 2.Vision

The Flight Simulator Game "Vaccine Quest" is a console-based, interactive game where the player takes on a mission to save the world from a global health crisis by collecting essential vaccine components. The game provides an educational and engaging experience, where players fly between airports in Europe to collect elements A, B, C and D, which are necessary for the creation of a vaccine.

The player starts at a random airport with a certain budget and a limited range for their aircraft. At each airport, the player may find one of the essential elements or a lucky box, which they can open by spending part of their budget. The lucky box may contain an additional vaccine component or be empty. The objective of the game is to collect all three elements within the given budget and range, thereby winning the game. The player must carefully decide which airports to visit while managing their resources.

The game proceeds in stages:
- The player is given a budget and initial location.
- The player can choose the next airport to fly to, within the limited range.
- Upon arriving at an airport, the player may discover a vaccine element or a lucky box.
- The player continues to visit airports until they have collected all required elements or run out of resources.

The main idea is to provide a strategic challenge where players must optimize their choices to achieve the goal while managing limited resources.

### 3. Functional Requirements
The following functional requirements are presented as user stories:

- As a player, I can start a new game by providing my screen name, so that I can begin my mission.
- As a player, I can view a brief story about the mission, so that I understand the purpose and context of the game.
- As a player, I can see my current budget and remaining range, so that I can make informed decisions about my next move.
- As a player, I can choose an airport within my aircraft's range to fly to, so that I can progress in the game.
- As a player, I can view the name and details of the airport I arrive at, so that I know my current location.
- As a player, I can collect an element if it is available at the airport, so that I can progress towards my goal of creating the vaccine.
- As a player, I can decide whether to open a lucky box for $100, so that I can potentially gain an additional element.
- As a player, I receive feedback if the lucky box is empty or contains an element, so that I know the outcome of my actions.
- As a player, I can view a list of airports within my current range, so that I can plan my next move.
- As a player, I can enter the ICAO code of an airport to travel to, so that I can move to my chosen destination.
- As a player, I am notified if my chosen destination is not within range, so that I can choose a valid airport.
- As a player, I can collect all required elements to win the game, so that I achieve my mission.
- As a player, I receive a game-over message if I run out of resources, so that I know when the game ends.

### 4. Quality Requirements

- Performance Requirement
Fetching airport information from the database must take a maximum of two seconds to ensure smooth gameplay.

- Usability Requirement
The player must receive immediate feedback after performing an action (e.g., collecting an element, opening a lucky box) to maintain engagement and provide clarity.

- Accessibility Requirement
The game must be designed to be accessible to players aged 12 and above, with straightforward text instructions and no inappropriate content.

- Sustainability Requirement
The game should promote strategic decision-making and resource management, encouraging players to think critically about efficient use of resources, aligning with themes of sustainability.

- User Interface Requirement
The game should have a simple, console-based interface that is easy to understand for users who are not familiar with complex gaming systems.

### 5.Databse Design
- Drop all tables except airport and country,creat new tables : game, element and port_contents. Sql query as below:

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

### Links：
- [Trello board](https://trello.com/invite/b/66fe78af1372c2113a78bb63/ATTIcf230239528edd2871486693b07ee3a0C2140598/challenger-flight-game-project)
- [Project tracking sheet](https://docs.google.com/spreadsheets/d/1vuq3BxNBDeG4BTiAt0iLGx4ohJ9QgnmPnivLulsLMhw/edit?gid=0#gid=0)
