# Optional dataset to load text directly rather than from files.

sample_docs = {
    "auth.md": """
    Authentication Overview
    -----------------------
    The system uses token-based authentication.
    The function `generate_token()` creates a new access token.
    """,

    "database.py": """
    def connect_to_db():
        # Opens a database connection.
        pass

    def fetch_user(id):
        # Returns user data from the database.
        pass
    """,

    "api_reference.txt": """
    Available Endpoints:
    - /login
    - /logout
    - /users
    """
}
