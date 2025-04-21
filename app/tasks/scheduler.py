from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import current_app
from ..services.email_service import EmailService

def init_scheduler(app):
    """Initialize the scheduler with the Flask app context"""
    scheduler = BackgroundScheduler()
    
    def fetch_emails_job():
        """Job to fetch emails periodically"""
        with app.app_context():
            try:
                user_email = current_app.config['GRAPH_USER_EMAIL']
                emails_synced = EmailService.fetch_recent_emails(user_email, hours=24)
                current_app.logger.info(f"Periodic email sync completed. Synced {emails_synced} emails.")
            except Exception as e:
                current_app.logger.error(f"Error in periodic email sync: {str(e)}")
    
    # Add the job to run every 30 minutes
    scheduler.add_job(
        fetch_emails_job,
        trigger=IntervalTrigger(minutes=30),
        id='fetch_emails_job',
        name='Fetch emails every 30 minutes',
        replace_existing=True
    )
    
    # Start the scheduler
    scheduler.start()
    
    # Shut down the scheduler when the app is shutting down
    @app.teardown_appcontext
    def shutdown_scheduler(exception=None):
        scheduler.shutdown() 