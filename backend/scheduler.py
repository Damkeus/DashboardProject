"""APScheduler configuration for automated daily updates."""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from datetime import datetime

from config import settings
from database.database import SessionLocal
from services.data_aggregator import data_aggregator

logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler = BackgroundScheduler()


def scheduled_data_update():
    """Job function to run scheduled data updates."""
    logger.info("Starting scheduled data update")
    
    db = SessionLocal()
    try:
        result = data_aggregator.update_all_data(db, update_type='automatic')
        logger.info(f"Scheduled update completed: {result['status']}")
    except Exception as e:
        logger.error(f"Scheduled update failed: {e}")
    finally:
        db.close()


def start_scheduler():
    """Initialize and start the scheduler."""
    try:
        # Add job with cron trigger
        scheduler.add_job(
            scheduled_data_update,
            trigger=CronTrigger(
                hour=settings.update_schedule_hour,
                minute=settings.update_schedule_minute,
                timezone=settings.update_schedule_timezone
            ),
            id='daily_update',
            name='Daily Data Update',
            replace_existing=True
        )
        
        scheduler.start()
        logger.info(
            f"Scheduler started - updates will run daily at "
            f"{settings.update_schedule_hour:02d}:{settings.update_schedule_minute:02d} "
            f"{settings.update_schedule_timezone}"
        )
    except Exception as e:
        logger.error(f"Failed to start scheduler: {e}")


def stop_scheduler():
    """Stop the scheduler gracefully."""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler stopped")


def get_scheduler_status():
    """Get current scheduler status."""
    return {
        'running': scheduler.running,
        'jobs': [
            {
                'id': job.id,
                'name': job.name,
                'next_run': job.next_run_time.isoformat() if job.next_run_time else None
            }
            for job in scheduler.get_jobs()
        ]
    }
