from flask import Blueprint,jsonify,request
from src.database.models import User,MedicalHistory
from src.schema import RegisterUserSchema,LoginUserSchema,UpdateUserSchema
from src.database.config import db
from src.constants import status
from werkzeug.security import generate_password_hash,check_password_hash
from src.utils import get_country_from_ip,send_verification_email,generate_confirmation_token,confirm_token
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity,create_refresh_token

auth = Blueprint('auth',__name__,url_prefix='/auth')


registration_schema = RegisterUserSchema()
login_schema = LoginUserSchema()

@auth.post('/register')
def register():
    data = request.json

    errors = registration_schema.validate(data)
    if errors:
        return jsonify(
            {
                "status":"Failed",
                "errors":errors
            }
        ),status.HTTP_400_BAD_REQUEST
    
    password_hash = generate_password_hash(data['password'])

    ip_address = request.remote_addr
    print(ip_address)

    country = get_country_from_ip(ip_address)


    user = User(
        full_name=data['full_name'],
        email=data['email'],
        password=password_hash,
        preferred_language=data['preferred_language'],
        country=country
    )


    db.session.add(user)

    token = generate_confirmation_token(user.id)
    verification_link = f"{request.url_root}auth/verify/{token}"

    send_verification_email(email=user.email,verification_link=verification_link,full_name=user.full_name)


    medical_history = MedicalHistory(
        user_id=user.id,
        allergy_description=data.get('allergy_description',None),
        general_medical_condition=data.get('general_medical_condition',None),

    )

    db.session.add(medical_history)
    db.session.commit()
    return jsonify(
        {
            "status":"Success",
            "message":"User created successfully",
            "user_info":{
                "full_name":user.full_name,
                "email":user.email,
                "preferred_language":user.preferred_language,
                "country":user.country,
            }
        }
    ),status.HTTP_201_CREATED


@auth.post('/login')
def login():
    data = request.json
    errors = login_schema.validate(data)
    if errors:
        return jsonify(
            {
                "status":"Failed",
                "errors":errors
            }
        ),status.HTTP_400_BAD_REQUEST
    

    user = User.query.filter_by(email=data['email']).first()
    
    if check_password_hash(password=data['password'],pwhash=user.password):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        if user.is_verified:
            return jsonify(
                {
                    "status":"Success",
                    "message":"User logged in successfully",
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "user_info":{
                        "full_name":user.full_name,
                        "email":user.email,
                        "preferred_language":user.preferred_language,
                        "country":user.country,
                    }
                }
            ),status.HTTP_200_OK
        else:
            return jsonify(
                {
                    "status":"Failed",
                    "message":"User not verified,vetify your account to login"
                }
            ),status.HTTP_401_UNAUTHORIZED
    else:
        return jsonify(
            {
                "status":"Failed",
                "message":"Invalid credentials"
            }
        ),status.HTTP_401_UNAUTHORIZED

       
    


@auth.post('/refresh')
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    return jsonify(
        {
            "status":"Success",
            "message":"Access token refreshed successfully",
            "access_token":access_token
        }
    ),status.HTTP_200_OK



@auth.get('/user')
@jwt_required()
def user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify(
        {
            "status":"Success",
            "user_info":{
                "full_name":user.full_name,
                "email":user.email,
                "preferred_language":user.preferred_language,
                "country":user.country,
            }
        }
    ),status.HTTP_200_OK


@auth.get('/verify/<token>')
def verify_user(token):
    user_id = confirm_token(token)
    if user_id:
        user = User.query.get(user_id)
        user.is_verified = True
        db.session.commit()
        return jsonify(
            {
                "status":"Success",
                "message":"User verified successfully"
            }
        ),status.HTTP_200_OK
    else:
        return jsonify(
            {
                "status":"Failed",
                "message":"Invalid token/Token expired, Try again"
            }
        ),status.HTTP_400_BAD_REQUEST
        
        


            




    
    
