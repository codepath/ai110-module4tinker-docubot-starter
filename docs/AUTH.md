# Authentication Guide

This document explains how authentication works in the sample application. It covers token generation, required environment variables, and the expected client workflow.

## Overview

The application uses a simple token based system. Every request to a protected endpoint must include a valid access token in the Authorization header. Tokens are short lived and tied to a single user.

## Token Generation

Tokens are created by the `generate_access_token` function in the `auth_utils.py` module. The function takes a user ID and returns a signed JSON Web Token string.

Internally, the token is signed using the secret stored in the `AUTH_SECRET_KEY` environment variable. If the key is missing or empty, token creation will fail.

The token payload includes:

- `user_id`
- `issued_at`
- `expires_at`
- `permissions` (optional)

## Validating Requests

Requests are validated by the `require_auth` decorator. This decorator ensures that:

1. A token is present in the Authorization header  
2. The token signature is valid  
3. The token has not expired  
4. The user has permission to access the requested resource  

If validation fails, the client receives a 401 Unauthorized response.

## Environment Variables

The authentication system depends on two variables:

- `AUTH_SECRET_KEY`  
  A secret string used to sign all access tokens. Must be long and unpredictable.

- `TOKEN_LIFETIME_SECONDS`  
  Controls how long a generated token remains valid. Defaults to 3600 seconds if not set.

Both variables must be configured before starting the server.

## Client Workflow

A typical client follows this sequence:

1. Send credentials to `/api/login`
2. Receive an access token in the response
3. Include the token in the Authorization header for all subsequent requests:

    ```plaintext
    Authorization: Bearer <token>
    ```

4. Refresh the token when it expires by calling `/api/refresh`

Clients should never store tokens in URL query parameters.

## Common Failure Cases

- Token signed with a stale or rotated key  
- Clock skew causing premature expiration  
- Missing Authorization header  
- Incorrect token format (extra whitespace or missing Bearer prefix)

If unexpected authentication failures occur, rotate the secret key and instruct users to log in again.
