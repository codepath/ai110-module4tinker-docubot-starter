# API Reference

This document lists the main API endpoints available in the sample application. It describes each route's purpose, required parameters, and expected responses. All protected endpoints require a valid access token.

## Base URL

    ```plaintext
    /api
    ````

## Authentication Endpoints

### POST /api/login

Authenticates a user and returns a short lived access token.

Request Body:

    ```json
    {
    "username": "example",
    "password": "secret"
    }
    ````

Successful Response:

    ```json
    {
    "access_token": "<token>"
    }
    ```

Notes:

* Returns 401 if credentials are invalid.
* The token must be included in the Authorization header for protected endpoints.

### POST /api/refresh

Exchanges an existing valid token for a new one with an updated expiration time.

Headers:

    ```plaintext
    Authorization: Bearer <token>
    ```

Response:

    ```json
    {
    "access_token": "<new_token>"
    }
    ```

## User Data Endpoints

### GET /api/users/<user_id>

Fetches profile data for a specific user.

Headers:

    ```plaintext
    Authorization: Bearer <token>
    ```

Response Example:

    ```json
    {
    "user_id": 42,
    "email": "user@example.com",
    "joined_at": "2024-01-15T10:22:00Z"
    }
    ```

Failure Cases:

* 401 if the token is missing or expired
* 403 if the user lacks permission to view this profile
* 404 if no user exists with the given ID

### GET /api/users

Returns a list of all users. Only accessible to admins.

Headers:

    ```plaintext
    Authorization: Bearer <token>
    ```

Successful Response:

    ```json
    [
    {
        "user_id": 1,
        "email": "admin@example.com"
    },
    {
        "user_id": 2,
        "email": "guest@example.com"
    }
    ]
    ```

Notes:

* Returns 403 for non admin accounts.

## Project Data Endpoints

### GET /api/projects

Returns all projects visible to the calling user.

Headers:

    ```plaintext
    Authorization: Bearer <token>
    ```

Response Example:

    ```json
    [
    {
        "project_id": "alpha",
        "name": "Alpha Project",
        "status": "active"
    }
    ]
    ```

### GET /api/projects/<project_id>

Fetches detailed information for a single project.

Headers:

    ```plaintext
    Authorization: Bearer <token>
    ```

Response Example:

    ```json
    {
    "project_id": "alpha",
    "name": "Alpha Project",
    "description": "Internal research initiative.",
    "status": "active",
    "owner": 1
    }
    ```

Failure Cases:

* 401 for missing token
* 403 if caller cannot access the project
* 404 if the project does not exist

## Error Formats

All error responses follow this structure:

    ```json
    {
    "error": "Description of the problem"
    }
    ```

Common error messages include:

* "Unauthorized"
* "Forbidden"
* "Not Found"
* "Invalid Request"
