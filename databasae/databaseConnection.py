#create database for game
create database vaccine_game;
use vaccine_game;
show databases;
use vaccine_game;
show tables;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE player_data;
DROP TABLE goal_elements;
DROP TABLE random_airports;
SET FOREIGN_KEY_CHECKS = 1;


CREATE TABLE game (
    id INT AUTO_INCREMENT PRIMARY KEY,
    money DECIMAL(10, 2) NOT NULL,
    player_range DECIMAL(10, 2) NOT NULL,
    location VARCHAR(10) NOT NULL,
    screen_name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE element (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name CHAR(1) NOT NULL,  -- A, B, C, D
    total_quantity INT NOT NULL  -- A:1, B:1, C:1, D:1
);

INSERT INTO element (name, total_quantity) VALUES
('A', 1),
('B', 1),
('C', 1),
('D', 1)
ON DUPLICATE KEY UPDATE name = VALUES(name), total_quantity = VALUES(total_quantity);

CREATE TABLE port_contents (
  id INT AUTO_INCREMENT PRIMARY KEY,
  game_id INT NOT NULL,
  airport VARCHAR(10) NOT NULL,
  content_type ENUM('element', 'lucky_box') NOT NULL,
  content_value CHAR(1) DEFAULT NULL,
  found TINYINT(1) DEFAULT 0
 );
ALTER TABLE port_contents
ADD CONSTRAINT fk_game_id
FOREIGN KEY (game_id) REFERENCES game(id);


