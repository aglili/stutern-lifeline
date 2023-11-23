from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.constants import status
from src.database.models import MedicalHistory, User, Conversation, ConversationInteraction
import requests
import os
from dotenv import load_dotenv
from src.database.config import db

from openai import OpenAI

load_dotenv()

chat = Blueprint('chat', __name__, url_prefix='/chat')

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))



@chat.post('/create-conversation')
@jwt_required()
def create_conversation():
    user_id = get_jwt_identity()

    conversation = Conversation(user_id=user_id)

    db.session.add(conversation)
    db.session.commit()


    return jsonify({
        "status": "success",
        "message": "Conversation created successfully",
        "conversation_id": conversation.id
    }), 200


@chat.post('/send-message')
@jwt_required()
def send_message():
    data = request.json
    user_id = get_jwt_identity()




    # Fetch the conversation
    conversation = Conversation.query.get(data['conversation_id'])

    if not conversation:
        return jsonify({
            "status": "error",
            "message": "Conversation does not exist"
        }), 404

    # Add user's message to the conversation
    user_message = data['message']
    conversation_interaction_user = ConversationInteraction(
        conversation_id=conversation.id,
        user_id=user_id,
        message=user_message,
        is_user=True,
        title=user_message
    )
    conversation.interactions.append(conversation_interaction_user)

    # Fetch conversation history for context
    conversation_history = ConversationInteraction.query.filter_by(conversation_id=conversation.id).order_by(ConversationInteraction.timestamp.desc()).all()

    # Construct context for the bot using conversation history
    context_messages = []
    for interaction in conversation_history:
        if interaction.is_user:
            context_messages.append(f"User: {interaction.message}")
        else:
            context_messages.append(f"Bot: {interaction.message}")

    context_for_bot = "\n".join(context_messages)


    print(context_for_bot)

    # Construct prompt for the AI with conversation history as context
    formatted_prompt = f"{context_for_bot}\n" 

    # Fetch user information
    user = User.query.get(user_id)
    medical_history = MedicalHistory.query.filter_by(user_id=user_id).first()

    user_info_string = f"""
    user's name is {user.full_name}
    user's country is {user.country}
    user's preferred language is {user.preferred_language}
    user's allergies are {medical_history.allergy_description}
    user's blood type is {medical_history.blood_type}
    user's genotype is {medical_history.genotype}
    user's height is {medical_history.height}
    user's weight is {medical_history.weight}
    user's blood pressure is {medical_history.blood_pressure}
    user's medical condition is {medical_history.general_medical_condition}
    """

    formatted_prompt += f"""
    Your Name is Stutern Lifeline AI. You Help With Providing Symptom Diagnosis.
    User's name is {user.full_name}
    User's country is {user.country}
    User's preferred language is {user.preferred_language}
    User's allergies are {medical_history.allergy_description}
    User's blood type is {medical_history.blood_type}
    User's genotype is {medical_history.genotype}
    User's height is {medical_history.height}
    User's weight is {medical_history.weight}
    User's blood pressure is {medical_history.blood_pressure}
    User's medical condition is {medical_history.general_medical_condition}

    If the preferred language is English, you ask the questions in English.
    If the preferred language is French, you ask the questions in French.
    If the preferred language is Spanish, you ask the questions in Spanish.
    When the questions asked are not enough, you ask the user to provide more information.
    When the questions asked are not in your scope, you deny having an answer to the question.
    You categorize the diagnosis into 3 categories: mild, moderate, and severe.
    If the diagnosis is mild, you ask the user to take some drugs or give drug recommendations.
    If severe, you give the diagnosis and also provide the user with emergency numbers to call based on their country.

    So, your response should be based on the information provided.

    """

    # Get AI response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": formatted_prompt}],
        max_tokens=500,
        temperature=0.9,
        stop=["\n"]
    )

    # Extract bot's response from AI completion
    bot_response = response.choices[0].message.content

    # Add bot's response to the conversation
    conversation_interaction_bot = ConversationInteraction(
        conversation_id=conversation.id,
        user_id=user_id,
        message=bot_response,
        is_user=False,
        title=bot_response
    )
    conversation.interactions.append(conversation_interaction_bot)

    # Save to the database
    db.session.add_all([conversation_interaction_user, conversation_interaction_bot])
    db.session.commit()

    return jsonify({
        "status": "success",
        "user_message": user_message,
        "bot_response": bot_response
    }), 200




@chat.route('/conversation/<conversation_id>', methods=['GET'])
def get_chat_history(conversation_id):

    if not conversation_id:
        return jsonify({"error": "Conversation ID not provided"}), 400

    # Fetch conversation title using conversation ID
    conversation = Conversation.query.get(conversation_id)

    if not conversation:
        return jsonify({"error": "Conversation not found"}), 404

    # Fetch conversation history based on the conversation ID
    conversation_history = ConversationInteraction.query.filter_by(conversation_id=conversation_id).order_by(ConversationInteraction.timestamp).all()

    # Initialize conversation history JSON structure
    chat_history_json = {
        "conversation_title": conversation.title,
        "messages": []
    }

    # Parse conversation history and construct the JSON format
    for interaction in conversation_history:
        message_entry = {
            "user_message": interaction.user_message,
            "bot_response": interaction.bot_response,
            "timestamp": str(interaction.timestamp)  # Convert timestamp to string format
        }
        chat_history_json["messages"].append(message_entry)

    return jsonify(chat_history_json), 200

