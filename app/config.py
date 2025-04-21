import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MongoDB
    MONGO_URI = os.getenv("MONGO_ATLAS_URI")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "email_service")
    
    # Microsoft Graph
    GRAPH_CLIENT_ID = os.getenv("GRAPH_CLIENT_ID")
    GRAPH_CLIENT_SECRET = os.getenv("GRAPH_CLIENT_SECRET")
    GRAPH_TENANT_ID = os.getenv("GRAPH_TENANT_ID")
    GRAPH_USER_EMAIL = os.getenv("GRAPH_USER_EMAIL")
    