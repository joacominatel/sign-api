-- postgresql database creation script
CREATE DATABASE taskapp;
\c taskapp;

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  email VARCHAR(255),
  role VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  title VARCHAR(255) NOT NULL,
  description TEXT,
  due_date DATE,
  completed BOOLEAN DEFAULT FALSE
);

-- Inser user admin
INSERT INTO users (username, password, name, email, role)
VALUES ('admin', 'admin', 'Admin', 'admin@admin.com', 'admin');

-- insert example data on table tasks
INSERT INTO tasks (user_id, title, description, due_date, completed)
VALUES (1, 'Task 1', 'Description of task 1', '2021-12-31', FALSE),
       (1, 'Task 2', 'Description of task 2', '2021-12-31', FALSE),
       (2, 'Task 3', 'Description of task 3', '2021-12-31', FALSE),
        (3, 'Task 4', 'Description of task 4', '2021-12-31', FALSE),
        (4, 'Task 5', 'Description of task 5', '2021-12-31', FALSE);

-- Create table groups for share tasks with other users
CREATE TABLE groups (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  owner_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE group_members (
  group_id INTEGER NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  PRIMARY KEY (group_id, user_id)
);

ALTER TABLE users ADD COLUMN profile_image_url TEXT;

-- add column to table tasks for share tasks with groups
ALTER TABLE tasks ADD COLUMN group_id INTEGER REFERENCES groups(id);