-- postgresql database creation script
CREATE DATABASE taskapp;
\c taskapp;

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  email VARCHAR(255),
  profile_image_url TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  title VARCHAR(255) NOT NULL,
  group_id INTEGER REFERENCES groups(id),
  description TEXT,
  due_date DATE,
  priority INTEGER DEFAULT 0,
  completed BOOLEAN DEFAULT FALSE
);

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

CREATE TABLE roles (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

CREATE TABLE user_roles (
  user_id INTEGER NOT NULL REFERENCES users(id),
  role_id INTEGER NOT NULL REFERENCES roles(id),
  PRIMARY KEY (user_id, role_id)
);


-- add view for get count of tasks by user
CREATE OR REPLACE VIEW tasks_count AS
SELECT u.id AS user_id, u.username, COUNT(t.id) AS count
FROM users u
LEFT JOIN tasks t ON u.id = t.user_id
GROUP BY u.id;

-- Table for posting like 'tweets' on groups
CREATE TABLE group_posts (
  id SERIAL PRIMARY KEY,
  group_id INTEGER NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (group_id) REFERENCES groups(id)
);

-- table for upvotes on posts
CREATE TABLE post_upvotes (
  post_id INTEGER NOT NULL REFERENCES group_posts(id) ON DELETE CASCADE,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  PRIMARY KEY (post_id, user_id)
);

-- add view for stats of complete app, count of users, tasks and groups
CREATE OR REPLACE VIEW app_stats AS
SELECT
  (SELECT COUNT(*) FROM users) AS users_count,
  (SELECT COUNT(*) FROM tasks) AS tasks_count,
  (SELECT COUNT(*) FROM groups) AS groups_count;


-- Inser user admin
INSERT INTO users (username, password, name, email, profile_image_url)
VALUES ('admin', 'admin', 'Admin', 'admin@admin.com' ,'../default-user.webp');

INSERT INTO roles (name) VALUES ('admin');
INSERT INTO roles (name) VALUES ('user');

-- cambiar nombre de database
ALTER DATABASE taskapp RENAME TO taskapp_dev;
