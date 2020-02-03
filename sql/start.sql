CREATE DATABASE yallaDb;
CREATE USER 'samasri2'@'localhost' IDENTIFIED BY '1';
GRANT ALL PRIVILEGES ON yallaDb.* TO 'samasri2'@'localhost';
FLUSH PRIVILEGES;

