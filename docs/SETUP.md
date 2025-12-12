# Setup Guide

This document explains how to install, configure, and run the sample application. Follow these steps to prepare your environment, set required variables, and verify that everything is working correctly.

## Requirements

- Python 3.9 or later  
- pip installed  
- A terminal or command prompt  
- Optional: a valid Gemini API key for LLM based features

## 1. Install Dependencies

From the project root, install dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

This installs all required libraries, including the database driver and LLM client.

## 2. Environment Variables

Create a `.env` file or export the following variables directly in your shell.

### Required Variables

- `DATABASE_URL`  
  Specifies where the application stores data. If omitted, the app uses a local SQLite database file.

  Example:

      ```plaintext
      DATABASE_URL=sqlite:///app.db
      ```

- `AUTH_SECRET_KEY`  
Used to sign authentication tokens. Must be a non empty string.

    Example:

        ```plaintext
        AUTH_SECRET_KEY="supersecretvalue"
        ```

### Optional Variables

- `TOKEN_LIFETIME_SECONDS`  
Controls how long access tokens remain valid.

- `GEMINI_API_KEY`  
Enables LLM powered features such as enhanced documentation answers. Without this key, the application falls back to rule based behavior.

## 3. Initialize the Database

If using SQLite, the database file will be created automatically when the server runs. For PostgreSQL, ensure the database exists before starting the application:

    ```plaintext
    createdb appdb
    ```

You may also need to run migrations if schema changes are introduced.

## 4. Running the Application

To start the server:

    ```plaintext
    python app.py
    ```

By default, the server listens on:

    ```plaintext
    [http://localhost:5000](http://localhost:5000)
    ```

Once the server is running, you can test basic functionality by visiting the API endpoints or using a tool like curl or Postman.

## 5. Using the Docs Assistant (DocuBot)

If you have set `GEMINI_API_KEY`, you can run the documentation assistant:

    ```plaintext
    python main.py
    ```

This tool supports multiple modes including:

- naive LLM generation  
- retrieval only  
- full RAG (retrieval plus generation)

Each mode helps you explore different system behaviors.

## 6. Troubleshooting

- If authentication fails, confirm that `AUTH_SECRET_KEY` is set.  
- If database queries return errors, verify the `DATABASE_URL` format.  
- If LLM features do not work, ensure that `GEMINI_API_KEY` is defined in the environment.  
- If installation fails, check that you are using a compatible Python version.

## 7. Resetting the Environment

To reset the local database (SQLite only):

    ```plaintext
    rm app.db
    ```

Then rerun the setup steps above.
