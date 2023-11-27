from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.schema import ReminderSchema
from src.database.config import db
from src.database.models import Reminder



reminder = Blueprint('reminder', __name__,url_prefix='/reminder')



reminder_schema = ReminderSchema()


@reminder.post('/add')
@jwt_required()
def add_reminder():
    data = request.json

    data['user_id'] = get_jwt_identity()


    errors = reminder_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    create_reminder = Reminder(**data)

    db.session.add(create_reminder)
    db.session.commit()
    return jsonify({
        "message": "Reminder created successfully",
        "status": "success",
        "data": reminder_schema.dump(create_reminder)
    })






