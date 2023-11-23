from marshmallow import Schema, fields,validates,ValidationError,validate
from src.database.models import User



class RegisterUserSchema(Schema):
    full_name = fields.Str(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    preferred_language = fields.Str(required=True, validate=validate.OneOf(['en', 'fr', 'es']))
    country = fields.Str(required=False, validate=validate.Length(min=3))
    allergy_description = fields.Str(required=False)
    general_medical_condition = fields.Str(required=False)

    @validates('email')
    def validate_email(self, value):
        if User.query.filter_by(email=value).first():
            raise ValidationError('Email already exists')
        return value
    


class LoginUserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))

    @validates('email')
    def validate_email(self, value):
        if not User.query.filter_by(email=value).first():
            raise ValidationError('Email not found')
        return value
    
class UpdateUserSchema(Schema):
    pass



class UpdateMedicalHistorySchema(Schema):
    allergy_description = fields.Str(required=False)
    general_medical_condition = fields.Str(required=False)
    blood_type = fields.Str(required=False)
    genotype = fields.Str(required=False)
    height = fields.Str(required=False)
    weight = fields.Str(required=False)
    blood_pressure = fields.Str(required=False)
    user_id = fields.Str(required=True)

    @validates('user_id')
    def validate_user_id(self, value):
        if not User.query.filter_by(id=value).first():
            raise ValidationError('User does not exist')
        return value
    
