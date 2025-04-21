import requests
from flask import current_app
from datetime import datetime, timedelta

class GraphAPIService:
    @staticmethod
    def get_access_token():
        """Get access token using client credentials flow"""
        url = f"https://login.microsoftonline.com/{current_app.config['GRAPH_TENANT_ID']}/oauth2/v2.0/token"
        
        payload = {
            'client_id': current_app.config['GRAPH_CLIENT_ID'],
            'client_secret': current_app.config['GRAPH_CLIENT_SECRET'],
            'scope': 'https://graph.microsoft.com/.default',
            'grant_type': 'client_credentials',
        }
        
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return response.json().get('access_token')

    @staticmethod
    def send_email(recipient, subject, body, attachments=None):
        """Send email using Microsoft Graph API"""
        access_token = GraphAPIService.get_access_token()
        url = f"https://graph.microsoft.com/v1.0/users/{current_app.config['GRAPH_USER_EMAIL']}/sendMail"
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        email_data = {
            "message": {
                "subject": subject,
                "body": {
                    "contentType": "Text",
                    "content": body
                },
                "toRecipients": [{
                    "emailAddress": {
                        "address": recipient
                    }
                }]
            },
            "saveToSentItems": "true"
        }
        
        if attachments:
            email_data["message"]["attachments"] = attachments
        
        response = requests.post(url, headers=headers, json=email_data)
        response.raise_for_status()
        return True

    @staticmethod
    def fetch_recent_emails(user_email, hours=24):
        """Fetch emails from the last specified hours for a specific user"""
        access_token = GraphAPIService.get_access_token()
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        cutoff_iso = cutoff_time.isoformat() + 'Z'
        
        url = f"https://graph.microsoft.com/v1.0/users/{user_email}/messages"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        params = {
            '$filter': f'receivedDateTime ge {cutoff_iso}',
            '$select': 'id,subject,from,toRecipients,receivedDateTime,body,hasAttachments',
            '$top': 100,
            '$orderby': 'receivedDateTime desc'
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json().get('value', [])