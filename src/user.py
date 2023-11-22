from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from src.database.models import User,MedicalHistory
from src.constants import status
from src.schema import UpdateMedicalHistorySchema
from src.database.config import db







user = Blueprint('user',__name__,url_prefix='/user')

medical_history_schema = UpdateMedicalHistorySchema()

@user.get('/records')
@jwt_required()
def get_health_records():
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    records = MedicalHistory.query.filter_by(user_id=user.id).first()

    return jsonify(
        {
            "status":"success",
            "data":{
                "allergies":records.allergy_description,
                "general_medical_condition":records.general_medical_condition,
                "blood_type":records.blood_type,
                "genotype":records.genotype,
                "height":records.height,
                "weight":records.weight,
                "blood_pressure":records.blood_pressure
            }
        }
    ),status.HTTP_200_OK


@user.patch('/records')
@jwt_required()
def update_medical_history():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    data = request.json

    data['user_id'] = user_id

    errors = medical_history_schema.validate(data)
    if errors:
        return jsonify({"status":"error","errors":errors}),status.HTTP_400_BAD_REQUEST
    
    record = MedicalHistory.query.filter_by(user_id=user.id).first()

    record.allergy_description = data.get('allergy_description',record.allergy_description)
    record.general_medical_condition = data.get('general_medical_condition',record.general_medical_condition)
    record.blood_type = data.get('blood_type',record.blood_type)
    record.genotype = data.get('genotype',record.genotype)
    record.height = data.get('height',record.height)
    record.weight = data.get('weight',record.weight)
    record.blood_pressure = data.get('blood_pressure',record.blood_pressure)


    db.session.commit()
    return jsonify({
        "status": "success",
        "message": "Medical history updated successfully",
        "data": {
            "allergies": record.allergy_description,
            "general_medical_condition": record.general_medical_condition,
            "blood_type": record.blood_type,
            "genotype": record.genotype,
            "height": record.height,
            "weight": record.weight,
            "blood_pressure": record.blood_pressure
        }
    }), status.HTTP_200_OK


@user.patch('/profile')
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    data = request.json

    user.full_name = data.get('full_name',user.full_name)
    user.preferred_language = data.get('preferred_language',user.preferred_language)
    user.country = data.get('country',user.country)

    db.session.commit()

    return jsonify(
        {
            "status":"success",
            "message":"Profile updated successfully",
            "data":{
                "full_name":user.full_name,
                "preferred_language":user.preferred_language,
                "country":user.country
            }
        }
    ),status.HTTP_200_OK

















