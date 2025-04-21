from pymongo import MongoClient, monitoring
from urllib.parse import quote_plus
from flask import current_app

class MongoDB:
    def __init__(self, app=None):
        self.client = None
        self.db = None
        self.app = app  # Store the app instance
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize MongoDB connection with timeout and pooling"""
        self.client = MongoClient(
            app.config["MONGO_ATLAS_URI"],
            maxPoolSize=50,
            connectTimeoutMS=30000,
            socketTimeoutMS=30000
        )
        self.db = self.client[app.config["MONGO_DB_NAME"]]
        self._verify_connection(app)
        self._ensure_indexes()

    def _verify_connection(self, app):
        """Test the database connection"""
        try:
            self.client.admin.command("ping")
            app.logger.info("✅ MongoDB Connection Successful")
        except Exception as e:
            app.logger.error(f"❌ MongoDB Connection Failed: {str(e)}")
            raise

    def _ensure_indexes(self):
        """Create performance-optimizing indexes"""
        self.db.emails.create_index([("created_at", -1)])  # Time-based sorting
        self.db.emails.create_index([("status", 1)])      # Status filtering

# Singleton instance
mongo = MongoDB()