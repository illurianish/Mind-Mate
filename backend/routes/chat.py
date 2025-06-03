from flask import Blueprint, request, jsonify
from models.chat import ChatHistory
from datetime import datetime
from extensions import db
from openai import OpenAI
import os
from dotenv import load_dotenv
from config import Config

# Load environment variables
load_dotenv()

chat_bp = Blueprint('chat', __name__)

def get_openai_client():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OpenAI API key not found")
    return OpenAI(api_key=api_key)

# System message for the AI
SYSTEM_MESSAGE = """You are MindMate, a compassionate AI companion focused on mental well-being. Format your responses in a clean, easy-to-read way:

1. Always start with a warm greeting and acknowledgment using emojis
2. Use line breaks between paragraphs for better readability
3. Format lists and steps with emojis and proper spacing
4. End with an encouraging message

Style guidelines:
• Use relevant emojis to make the text friendly and engaging
• Keep paragraphs short and well-spaced
• Use bullet points or numbered lists when providing steps
• Bold important points using **asterisks**
• Add line breaks between sections

Example format:
Hi there! 👋 I understand how you're feeling...

Here are some helpful techniques you can try:

1. 🫁 **Deep Breathing**:
   • Inhale slowly for 4 counts
   • Hold for 4 counts
   • Exhale gently for 4 counts

2. 🧘‍♀️ **Mindful Moment**:
   • Find a quiet space
   • Close your eyes
   • Focus on your breath

Remember to be gentle with yourself! 💚 You're taking positive steps, and that's what matters.

Voice and Tone:
- Warm and empathetic
- Clear and structured
- Professional yet friendly
- Encouraging and supportive
- Use inclusive language

Important:
- Never diagnose conditions
- Don't prescribe medications
- Always encourage professional help when needed
- Keep responses focused and practical
- Provide specific, actionable advice"""

def get_response(message):
    """Get response from OpenAI API"""
    try:
        client = get_openai_client()
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": message}
            ],
            max_tokens=400,
            temperature=0.7,
        )
        return completion.choices[0].message.content
    except ValueError as e:
        print(f"OpenAI configuration error: {str(e)}")
        return "I apologize, but the service is not properly configured. Please contact the administrator."
    except Exception as e:
        print(f"OpenAI API error: {str(e)}")
        return "I apologize, but I'm having trouble processing your message right now. Could you try again in a moment?"

@chat_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400

        user_message = data['message']
        bot_response = get_response(user_message)
        
        # Store chat history
        chat_history = ChatHistory(
            user_message=user_message,
            bot_response=bot_response,
            timestamp=datetime.utcnow()
        )
        db.session.add(chat_history)
        db.session.commit()

        return jsonify({
            'response': bot_response
        })

    except Exception as e:
        print(f"Chat endpoint error: {str(e)}")
        return jsonify({
            'error': 'An error occurred while processing your message'
        }), 500

@chat_bp.route('/chat/history', methods=['GET'])
def get_chat_history():
    try:
        history = ChatHistory.query.order_by(ChatHistory.timestamp.desc()).limit(50).all()
        return jsonify({
            'history': [entry.to_dict() for entry in history]
        })
    except Exception as e:
        print(f"Error fetching chat history: {str(e)}")
        return jsonify({'error': 'Failed to fetch chat history'}), 500
