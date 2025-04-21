# Microsoft Graph API Email Service

This application integrates with Microsoft Graph API to send emails and periodically retrieve new emails, storing them in a MongoDB database.

## Features

- **Send Emails**: API endpoint to send emails via Microsoft Graph API
- **Retrieve Emails**: Periodically fetches and stores new emails from the past 24 hours
- **Scheduling**: Automatically runs email fetching at configurable intervals
- **MongoDB Storage**: Efficiently stores email data with proper indexing
- **Docker Support**: Easy deployment with Docker and docker-compose

## Technologies Used

- Python 3.9+
- Flask
- MongoDB
- Microsoft Graph API
- APScheduler
- Docker & Docker Compose

## Setup Instructions

### Prerequisites

1. Python 3.9 or higher
2. MongoDB (local or hosted)
3. Free Outlook account for testing
4. Microsoft Entra (Azure AD) application registration

### Microsoft Entra ID Setup

1. Create a free Outlook account if you don't have one
2. Sign in to the [Azure Portal](https://portal.azure.com)
3. Navigate to "Microsoft Entra ID" > "App registrations" > "New registration"
4. Register a new application with the following settings:
   - Name: Email Service App
   - Supported account types: Accounts in this organizational directory only
   - Redirect URI: Web - http://localhost:5000
5. After registration, note the Application (client) ID and Directory (tenant) ID
6. Create a client secret:
   - Navigate to "Certificates & secrets" > "New client secret"
   - Provide a description and expiration period
   - Copy the secret value (only visible once)
7. Add API permissions:
   - Navigate to "API permissions" > "Add a permission"
   - Select "Microsoft Graph" > "Application permissions"
   - Add the following permissions:
     - Mail.Read
     - Mail.Send
     - User.Read
   - Click "Grant admin consent"

### Environment Variables

Create a `.env` file with the following variables:

```
# Microsoft Graph API Configuration
MS_CLIENT_ID=your_client_id
MS_CLIENT_SECRET=your_client_secret
MS_TENANT_ID=your_tenant_id
MS_USER_EMAIL=your_outlook_email

# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=email_service
MONGO_COLLECTION_NAME=emails

# Scheduler Configuration
EMAIL_FETCH_INTERVAL=30  # In minutes

# Flask Configuration
DEBUG=True
HOST=0.0.0.0
PORT=5000
```

### Installation (Local)

1. Clone this repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python -m app
   ```

### Installation (Docker)

1. Clone this repository
2. Create `.env` file as described above
3. Build and run using docker-compose:
   ```bash
   docker-compose up -d
   ```

## API Endpoints

### Send Email

```
POST /api/email/send
Content-Type: application/json

{
  "to_email": "recipient@example.com",
  "subject": "Test Email",
  "body": "<p>This is a test email</p>",
  "attachments": [
    {
      "name": "test.txt",
      "content_type": "text/plain",
      "content": "SGVsbG8gV29ybGQhCg=="  // Base64 encoded content
    }
  ]
}
```

### Manually Trigger Email Fetch

```
POST /api/email/fetch
Content-Type: application/json

{
  "hours": 24  // Optional, defaults to 24
}
```

### Get Stored Emails

```
GET /api/email/emails?hours=24
```

## Testing

Run the tests using pytest:

```bash
pytest tests/
```

## How I Used AI Coding Tools

Throughout this project, I utilized several AI coding tools to expedite development:

1. **Initial Setup**: Used GitHub Copilot to generate the project structure and basic Flask application skeleton.

2. **Microsoft Graph API Integration**: Leveraged ChatGPT to understand the authentication flow and API endpoints for Microsoft Graph, then adapted the suggestions to fit our specific use case.

3. **Code Refinement**: Used GitHub Copilot to help write more efficient MongoDB queries and proper indexing strategies.

4. **Documentation**: Generated base documentation structure with ChatGPT, then customized it to include all relevant setup instructions and API details.

5. **Debugging**: When encountering issues with token acquisition, used ChatGPT to diagnose potential problems and suggest solutions.

The AI tools significantly accelerated development, especially for boilerplate code and standard patterns. However, all generated code was reviewed and modified to ensure it met the specific requirements of this project.

## Future Improvements

- Add robust error handling and retries for API requests
- Implement rate limiting to prevent Graph API quota exhaustion
- Add user authentication for API endpoints
- Create a web interface for viewing and managing emails
- Implement attachment download functionality
