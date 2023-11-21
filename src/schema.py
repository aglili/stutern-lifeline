from marshmallow import Schema, fields,validates,ValidationError,validate
from src.database.models import User



class RegisterUserSchema(Schema):
    full_name = fields.Str(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    preferred_language = fields.Str(required=True, validate=validate.OneOf(['en', 'fr', 'es']))

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

    
