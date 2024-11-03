import os
from urllib.parse import quote_plus

# Base directory for the application
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret-key')

    # Azure Blob Storage settings
    BLOB_ACCOUNT = os.environ.get('BLOB_ACCOUNT', 'ENTER_STORAGE_ACCOUNT_NAME')
    BLOB_STORAGE_KEY = os.environ.get('BLOB_STORAGE_KEY', 'ENTER_BLOB_STORAGE_KEY')
    BLOB_CONTAINER = os.environ.get('BLOB_CONTAINER', 'ENTER_IMAGES_CONTAINER_NAME')
    BLOB_CONNECTION_STRING = os.environ.get('BLOB_CONNECTION_STRING')

    # SQL Database settings
    SQL_SERVER = os.environ.get('SQL_SERVER', 'ENTER_SQL_SERVER_NAME.database.windows.net')
    SQL_DATABASE = os.environ.get('SQL_DATABASE', 'ENTER_SQL_DB_NAME')
    SQL_USER_NAME = os.environ.get('SQL_USER_NAME', 'ENTER_SQL_SERVER_USERNAME')
    SQL_PASSWORD = os.environ.get('SQL_PASSWORD', 'ENTER_SQL_SERVER_PASSWORD')

    # SQLAlchemy database URI, may require adjustments for driver versions
    SQLALCHEMY_DATABASE_URI = (
        "mssql+pyodbc:///?odbc_connect={}".format(
            quote_plus(
                "Driver={ODBC Driver 17 for SQL Server};" +
                "Server={};Database={};UID={};PWD={};".format(
                    SQL_SERVER, SQL_DATABASE, SQL_USER_NAME, SQL_PASSWORD
                )
            )
        )
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Microsoft Authentication settings
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    AUTHORITY = "https://login.microsoftonline.com/common"  # Multi-tenant app; replace with tenant name if needed
    CLIENT_ID = os.environ.get("CLIENT_ID")

    # Redirect path for authentication
    REDIRECT_PATH = "/getAToken"  # Must match the app's redirect_uri set in Azure AD

    # Permissions scope for Microsoft Graph
    SCOPE = ["User.Read"]  # Requires user profile read access

    # Session settings for token cache
    SESSION_TYPE = "filesystem"  # Token cache will be stored in server-side session
