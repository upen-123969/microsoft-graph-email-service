from flask.cli import AppGroup
from ..services.mongo_service import mongo

db_cli = AppGroup('db')

@db_cli.command('check')
def check_db():
    """Verify MongoDB connection and documents"""
    count = mongo.db.emails.count_documents({})
    print(f"📊 Total emails: {count}")
    for email in mongo.db.emails.find().limit(2):
        print(f"✉️ {email['subject']} (From: {email['sender']})")