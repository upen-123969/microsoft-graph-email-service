import click
from datetime import datetime
from flask.cli import with_appcontext
from ..services.mongo_service import mongo

@click.command("seed-db")
@with_appcontext
def seed_db():
    """Insert test emails into MongoDB"""
    emails = [
        {
            "sender": "admin@example.com",
            "recipient": "user1@example.com",
            "subject": "Welcome!",
            "body": "This is your first email.",
            "created_at": datetime.utcnow(),
            "status": "delivered"
        },
        {
            "sender": "notifications@service.com",
            "recipient": "user1@example.com",
            "subject": "Your subscription",
            "body": "Your premium plan is active.",
            "created_at": datetime.utcnow(),
            "status": "delivered"
        }
    ]
    
    result = mongo.get_collection("emails").insert_many(emails)
    print(f"Inserted {len(result.inserted_ids)} test emails!")