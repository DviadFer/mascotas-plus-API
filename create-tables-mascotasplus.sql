CREATE DATABASE IF NOT EXISTS mascotasplusdb;

USE mascotasplusdb;

CREATE TABLE tUser (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  surname VARCHAR(100) NOT NULL,
  email VARCHAR(200) NOT NULL UNIQUE,
  encrypted_password VARCHAR(100) NOT NULL,
  active_session_token CHAR(20)
);

CREATE TABLE tWalk (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  datetime DATETIME NOT NULL,
  latitude DECIMAL(8,6) NOT NULL,
  longitude DECIMAL(9,6) NOT NULL,
  author_id INTEGER NOT NULL,
  
  FOREIGN KEY (author_id) REFERENCES tUser(id)
);

CREATE TABLE tCompanion (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  requester_id INTEGER NOT NULL,
  walk_id INTEGER NOT NULL,
  message VARCHAR(500) NOT NULL,
  is_accepted BOOLEAN NOT NULL DEFAULT FALSE,
  
  FOREIGN KEY (requester_id) REFERENCES tUser(id),
  FOREIGN KEY (walk_id) REFERENCES tWalk(id)
);

