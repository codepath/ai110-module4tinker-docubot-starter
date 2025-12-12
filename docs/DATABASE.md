# Database Guide

This document describes the database layer used in the sample application. It covers connection details, table structures, and common query patterns that appear throughout the codebase.

## Overview

The application uses a lightweight SQLite database for local development. In production environments, it can be configured to use PostgreSQL by providing the correct connection string.

All database interactions are handled through the `db.py` module, which provides helper functions for connecting, executing queries, and mapping results into Python objects.

## Connection Configuration

The database connection is determined by the `DATABASE_URL` environment variable.

Examples:

- SQLite (default):

    ```plaintext
    sqlite:///app.db
    ```

- PostgreSQL:

    ```plaintext
    postgres://user:password@localhost:5432/appdb
    ```

If `DATABASE_URL` is not provided, the application creates a local SQLite database file named `app.db`.

## Tables

### users

Stores basic account information.

| Column       | Type      | Description                         |
|--------------|-----------|-------------------------------------|
| user_id      | INTEGER   | Primary key                         |
| email        | TEXT      | Unique email address                |
| password_hash| TEXT      | Hashed password                     |
| joined_at    | TEXT      | ISO 8601 timestamp                  |

### projects

Represents projects owned or shared with users.

| Column       | Type      | Description                         |
|--------------|-----------|-------------------------------------|
| project_id   | TEXT      | Primary key (string identifier)     |
| name         | TEXT      | Human readable name                 |
| description  | TEXT      | Optional longer description         |
| status       | TEXT      | active, archived, or pending        |
| owner_id     | INTEGER   | Foreign key referencing users       |

### permissions

Maps users to projects and defines what actions they can take.

| Column     | Type    | Description                             |
|------------|---------|-----------------------------------------|
| user_id    | INTEGER | Foreign key                             |
| project_id | TEXT    | Foreign key                             |
| role       | TEXT    | admin, editor, or viewer                |

A user listed as admin automatically has full access to the project.

## Query Helpers

The `db.py` module exposes several helpful functions:

- `get_user_by_id(user_id)`  
Returns a dictionary with user details or None if not found.

- `get_all_users()`  
Returns a list of all user records.

- `get_projects_for_user(user_id)`  
Returns all projects where the user has at least viewer access.

- `get_project_details(project_id)`  
Returns a single project record, including its metadata.

These functions are thin wrappers over SQL queries and intentionally simple to make debugging easier.

## Common Failure Cases

- Missing or invalid `DATABASE_URL`  
- Incorrect table schema after manual edits  
- Queries returning empty results due to missing foreign key references  
- SQLite locking errors when multiple writes happen quickly  

If schema inconsistencies appear, run database migrations again or recreate the local SQLite file.

## Notes for Development

Developers often encounter confusion between SQLite and PostgreSQL behavior. In particular:

- SQLite allows many implicit type conversions  
- SQLite ignores certain constraint violations that PostgreSQL enforces  
- Timestamps may appear in different formats across engines  

Always test schema related changes using both database backends when possible.
