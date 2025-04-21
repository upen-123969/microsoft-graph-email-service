from datetime import datetime
from bson import ObjectId

class Email:
    @staticmethod
    def create_email(sender, recipient, subject, body, attachments=None):
        return {
            'sender': sender,
            'recipient': recipient,
            'subject': subject,
            'body': body,
            'attachments': attachments or [],
            'created_at': datetime.utcnow(),
            'is_read': False,
            'status': 'pending'
        }
    
    @staticmethod
    def get_by_id(email_id, db):
        return db.emails.find_one({'_id': ObjectId(email_id)})