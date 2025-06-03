from flask import Blueprint, request, jsonify
from models.chat import ChatHistory
from datetime import datetime
from extensions import db
from openai import OpenAI
import os
from dotenv import load_dotenv
from config import Config

# Load up our environment variables
load_dotenv()

chat_bp = Blueprint('chat', __name__)

def get_openai_client():
    """
    Sets up our connection to OpenAI
    If we don't have an API key, we're pretty much screwed
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("Whoops! No OpenAI API key found - check your .env file")
    return OpenAI(api_key=api_key)

# This is the personality we give to our AI - think of it as the AI's training manual
SYSTEM_MESSAGE = """You are MindMate, a compassionate AI companion focused on mental well-being. 

You're like a really good friend who also happens to know a lot about mental health. Your job is to:

🌟 **Be genuinely supportive** - not fake or robotic
💬 **Format your responses nicely** - use emojis, line breaks, and clear structure
🎯 **Give practical advice** - stuff people can actually do right now
💚 **Stay positive but realistic** - acknowledge struggles without being preachy

Here's how to format your responses:
1. Start with a warm greeting using emojis
2. Break up text with line breaks (nobody likes walls of text)
3. Use bullet points and numbered lists for steps
4. End with something encouraging

Example style:
Hey there! 👋 I can hear that you're going through a tough time...

Here are some things that might help:

🫁 **Try some deep breathing**:
   • Breathe in slowly for 4 counts
   • Hold it for 4 counts  
   • Let it out gently for 4 counts

Remember - you're being really brave by reaching out! 💪

Important stuff to remember:
- Don't try to diagnose anything (you're not a doctor!)
- Don't recommend specific medications
- Always suggest professional help when things seem serious
- Keep it real but hopeful
- Actually be helpful, not just say nice things"""

def get_response(message):
    """
    This is where the magic happens - we send the user's message to OpenAI
    and hopefully get back something helpful and not weird
    """
    try:
        client = get_openai_client()
        
        # Send the message to OpenAI with our custom personality
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Good balance of smart and affordable
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": message}
            ],
            max_tokens=400,  # Keep responses reasonable length
            temperature=0.7,  # A bit creative but not too weird
        )
        return completion.choices[0].message.content
        
    except ValueError as e:
        # This happens when OpenAI isn't configured properly
        print(f"OpenAI setup problem: {str(e)}")
        return "Sorry, I'm having some technical difficulties right now. The admin needs to check the OpenAI configuration."
        
    except Exception as e:
        # Something else went wrong - network issues, API problems, etc.
        print(f"OpenAI had a moment: {str(e)}")
        return "Hmm, I'm having trouble connecting to my brain right now 🤔 Could you try asking me again in a minute?"

@chat_bp.route('/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint - this is where users send messages and get responses
    """
    try:
        # Get the JSON data from the request
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Hey, you need to actually send me a message!'}), 400

        user_message = data['message']
        
        # Get the AI response
        bot_response = get_response(user_message)
        
        # Save this conversation to our database for later
        # (Don't worry, we're not being creepy - just keeping track for the user)
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
        # If anything goes wrong, at least give a helpful error
        print(f"Chat broke somehow: {str(e)}")
        return jsonify({
            'error': 'Something went wrong while processing your message. Please try again!'
        }), 500

@chat_bp.route('/chat/history', methods=['GET'])
def get_chat_history():
    """
    Returns the last 50 chat messages - useful for showing conversation history
    """
    try:
        # Get the most recent 50 chat entries
        history = ChatHistory.query.order_by(ChatHistory.timestamp.desc()).limit(50).all()
        return jsonify({
            'history': [entry.to_dict() for entry in history]
        })
    except Exception as e:
        print(f"Couldn't fetch chat history: {str(e)}")
        return jsonify({'error': 'Unable to load chat history right now'}), 500
