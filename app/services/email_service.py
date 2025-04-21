from datetime import datetime
from flask import current_app
from .mongo_service import mongo
from .graph_api import GraphAPIService

class EmailService:
    @staticmethod
    def create_email_document(sender, recipient, subject, body, status="pending"):
        """Create a properly structured email document"""
        return {
            "sender": sender,
            "recipient": recipient,
            "subject": subject,
            "body": body,
            "status": status,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

    @staticmethod
    def send_email(recipient, subject, body):
        """Send email and store in MongoDB"""
        try:
            # 1. Store in MongoDB first (as "pending")
            email_doc = EmailService.create_email_document(
                sender=current_app.config["GRAPH_USER_EMAIL"],
                recipient=recipient,
                subject=subject,
                body=body
            )
            result = mongo.db.emails.insert_one(email_doc)
            
            # 2. Send via Graph API
            GraphAPIService.send_email(recipient, subject, body)
            
            # 3. Update status to "sent"
            mongo.db.emails.update_one(
                {"_id": result.inserted_id},
                {"$set": {"status": "sent", "updated_at": datetime.utcnow()}}
            )
            return True
            
        except Exception as e:
            # Mark as failed if error occurs
            mongo.db.emails.update_one(
                {"_id": result.inserted_id},
                {"$set": {"status": "failed", "error": str(e)}}
            )
            raise

    @staticmethod
    def process_email_data(email_data):
        """Process raw email data from Graph API into a standardized format"""
        return {
            "message_id": email_data.get('id'),
            "subject": email_data.get('subject'),
            "sender": email_data.get('from', {}).get('emailAddress', {}).get('address'),
            "recipients": [recipient.get('emailAddress', {}).get('address') 
                         for recipient in email_data.get('toRecipients', [])],
            "received_at": email_data.get('receivedDateTime'),
            "body": email_data.get('body', {}).get('content'),
            "has_attachments": email_data.get('hasAttachments', False),
            "status": "received",
            "stored_at": datetime.utcnow()
        }

    @staticmethod
    def fetch_recent_emails(user_email, hours=24):
        """Fetch emails from Graph API and store in MongoDB"""
        try:
            # Fetch emails from Graph API
            emails = GraphAPIService.fetch_recent_emails(user_email, hours)
            
            if not emails:
                return 0
            
            # Process and store emails
            processed_emails = [EmailService.process_email_data(email) for email in emails]
            
            # Store in MongoDB
            if processed_emails:
                # First, remove any existing emails with the same message_id
                message_ids = [email['message_id'] for email in processed_emails]
                mongo.db.emails.delete_many({'message_id': {'$in': message_ids}})
                
                # Insert new emails
                mongo.db.emails.insert_many(processed_emails)
            
            return len(processed_emails)
            
        except Exception as e:
            current_app.logger.error(f"Email fetch failed: {str(e)}")
            return 0