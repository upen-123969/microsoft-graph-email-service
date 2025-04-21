from flask import Blueprint, request, jsonify, current_app
from flask_restx import Api, Resource, fields
from ..services.email_service import EmailService
from ..services.mongo_service import mongo
from datetime import datetime, timedelta

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint, version='1.0', title='Email Service API')

# Swagger models
email_model = api.model('Email', {
    'recipient': fields.String(required=True, description='Recipient email address'),
    'subject': fields.String(required=True, description='Email subject'),
    'body': fields.String(required=True, description='Email body'),
    'attachments': fields.List(fields.Raw, description='Optional attachments')
})

@api.route('/emails')
class EmailList(Resource):
    @api.expect(email_model)
    def post(self):
        """Send a new email"""
        data = request.json
        try:
            EmailService.send_email(
                recipient=data['recipient'],
                subject=data['subject'],
                body=data['body'],
                attachments=data.get('attachments')
            )
            return {'status': 'success'}, 201
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 400

    def get(self):
        """Fetch and store new emails from the last 24 hours"""
        try:
            # Get user email from request or config
            user_email = request.args.get('user_email', current_app.config['GRAPH_USER_EMAIL'])
            
            # Fetch new emails from Graph API and store in MongoDB
            emails_synced = EmailService.fetch_recent_emails(user_email, hours=24)
            
            # Get the stored emails from MongoDB
            stored_emails = list(mongo.db.emails.find(
                {'stored_at': {'$gte': datetime.utcnow() - timedelta(hours=24)}}
            ).sort('received_at', -1))
            
            # Convert ObjectId to string for JSON serialization
            for email in stored_emails:
                email['_id'] = str(email['_id'])
            
            return jsonify({
                'status': 'success',
                'emails_synced': emails_synced,
                'emails': stored_emails
            })
            
        except Exception as e:
            current_app.logger.error(f"Error fetching emails: {str(e)}")
            return {'status': 'error', 'message': str(e)}, 500