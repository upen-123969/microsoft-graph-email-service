import pytest
from unittest.mock import patch, MagicMock
from app.services.email_service import EmailService
from app.extensions import mongo

@pytest.fixture
def mock_mongo():
    with patch('app.extensions.mongo.db') as mock_db:
        yield mock_db

@pytest.fixture
def mock_graph():
    with patch('app.services.graph_api.GraphAPIService') as mock:
        yield mock

def test_send_email_success(mock_mongo, mock_graph):
    mock_mongo.emails.insert_one.return_value.inserted_id = '123'
    mock_graph.send_email.return_value = True
    
    result = EmailService.send_email('test@example.com', 'Test', 'Body')
    assert result is True
    mock_mongo.emails.update_one.assert_called_once()

def test_fetch_emails(mock_mongo, mock_graph):
    mock_graph.fetch_recent_emails.return_value = [{'id': '1'}]
    
    count = EmailService.fetch_and_store_emails()
    assert count == 1
    mock_mongo.emails.insert_many.assert_called_once_with([{'id': '1'}])