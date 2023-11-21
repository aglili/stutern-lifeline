from src.database.config import db
import datetime
import random
import string

def generate_id(length=8):
    """Generate a random string of given length."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    preferred_language = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    medical_histories = db.relationship('MedicalHistory', backref=db.backref('user', lazy=True))
    country = db.Column(db.String, nullable=True)
    is_verified = db.Column(db.Boolean, default=False)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.id = f"user_{generate_id()}"

    def __str__(self) -> str:
        return f"{self.id}"

class MedicalHistory(db.Model):
    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    allergy_description = db.Column(db.String, nullable=True)
    general_medical_condition = db.Column(db.String, nullable=True)
    blood_type = db.Column(db.String, nullable=True)
    sickle_cell_status = db.Column(db.String, nullable=True)
    genotype = db.Column(db.String, nullable=True)
    height = db.Column(db.String, nullable=True)
    weight = db.Column(db.String, nullable=True)
    blood_pressure = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    
    def __init__(self, *args, **kwargs):
        super(MedicalHistory, self).__init__(*args, **kwargs)
        self.id = f"medical_history_{generate_id()}"

    def __str__(self) -> str:
        return f"{self.id}"
