DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS sections;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS team_memberships;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS organizations;

CREATE TABLE organizations (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    domain TEXT
);

CREATE TABLE users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    role TEXT DEFAULT 'Member',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE teams (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    organization_id TEXT NOT NULL,
    FOREIGN KEY(organization_id) REFERENCES organizations(id)
);

CREATE TABLE projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    team_id TEXT NOT NULL,
    description TEXT,
    created_at DATETIME,
    FOREIGN KEY(team_id) REFERENCES teams(id)
);

CREATE TABLE sections (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    project_id TEXT NOT NULL,
    FOREIGN KEY(project_id) REFERENCES projects(id)
);

CREATE TABLE tasks (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    assignee_id TEXT,
    project_id TEXT NOT NULL,
    section_id TEXT,
    parent_id TEXT,
    due_date DATETIME,
    created_at DATETIME NOT NULL,
    completed BOOLEAN DEFAULT 0,
    completed_at DATETIME,
    FOREIGN KEY(assignee_id) REFERENCES users(id),
    FOREIGN KEY(project_id) REFERENCES projects(id),
    FOREIGN KEY(section_id) REFERENCES sections(id),
    FOREIGN KEY(parent_id) REFERENCES tasks(id)
);

CREATE TABLE comments (
    id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    author_id TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    FOREIGN KEY(task_id) REFERENCES tasks(id),
    FOREIGN KEY(author_id) REFERENCES users(id)
);