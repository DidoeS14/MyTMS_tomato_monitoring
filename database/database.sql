-- Create a new database (if not already created)
CREATE DATABASE IF NOT EXISTS tomato;

-- Select the database
USE tomato;

-- Create the `disease` table
CREATE TABLE disease (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    area VARCHAR(100) NOT NULL,
    ill_count INT DEFAULT 0
);

-- Create the `growth` table
CREATE TABLE growth (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    area VARCHAR(100) NOT NULL,
    green_count INT DEFAULT 0,
    half_ripened_count INT DEFAULT 0,
    fully_ripened_count INT DEFAULT 0
);





