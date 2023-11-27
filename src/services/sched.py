import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.utils import send_reminder
from src.database.models import Reminder, User

def start_scheduler():
    db_url = os.getenv('SQLALCHEMY_DATABASE_URI') 
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    reminders = session.query(Reminder).filter_by(is_completed=False).all()
    for reminder in reminders:
        user = session.query(User).filter_by(id=reminder.user_id).first()
        if user:
            user_email = user.email
            send_reminder(reminder.title, reminder.description, user_email)
            reminder.is_completed = True


    session.commit()
    session.close()


start_scheduler()
