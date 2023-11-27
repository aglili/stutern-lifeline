import requests,os
from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv
load_dotenv()
from trycourier import Courier



client = Courier(auth_token=os.getenv('COURIER_TOKEN'))


def get_country_from_ip(ip_address):
    """Get country from IP address using ipinfo.io API."""
    url = f"https://ipinfo.io/{ip_address}/country"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return "Unknown"


def send_verification_email(email:str, verification_link:str,full_name:str):
    """Send verification email to user."""

    client.send_message(
    message={
        "to": {
        "email": email,
        },
        "template": "ZNMXSVG73WMS5SM9M2WJ93FJKXEC",
        "data": {
        "UserName": full_name,
        "VerificationLink": verification_link,
        },
    }
    )




def generate_confirmation_token(user_id):
    serializer = URLSafeTimedSerializer(secret_key=os.getenv('SECRET_KEY'))
    return serializer.dumps(user_id)


def confirm_token(token,expiration=3600):
    serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
    try:
        user_id = serializer.loads(token,max_age=expiration)
        return user_id
    except Exception as e:
        return None
    


def send_reminder_email(email:str, reminder_title:str,reminder_description:str):
    """Send reminder email to user."""

    client.send_message(
  message={
    "to": {
      "email": email,
    },
    "template": "KXD3H695DR4J4EKQGRTBHDZMYMA3",
    "data": {
      "title": reminder_title,
      "description": reminder_description,
    },
  }
    )