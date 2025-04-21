import click
from flask.cli import with_appcontext
from ..services.email_service import EmailService

@click.command("test-email")
@with_appcontext
def test_email():
    """Send a test email"""
    try:
        EmailService.send_email(
            recipient="test@example.com",
            subject="Test Email",
            body="This is a test email from our service"
        )
        click.echo("✅ Test email sent successfully!")
    except Exception as e:
        click.echo(f"❌ Failed: {str(e)}")