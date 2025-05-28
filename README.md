# MindMate - AI Mental Health Companion 🧠💚

MindMate is an AI-powered mental health chatbot designed to provide emotional support and mental well-being resources. Built with React, TypeScript, and Flask, it offers a compassionate space for users to express their feelings and receive supportive responses.

## 🌟 Features

- 💬 Real-time chat interface with AI responses
- 🎨 Beautiful, responsive UI with dark/light mode
- 🔒 Secure message handling
- 📱 Mobile-friendly design
- 🎯 Quick access emotional prompts
- 🔗 Crisis resources integration
- 💾 Chat history persistence

## 🚀 Live Demo

Visit [https://illurianish.github.io/Mind-Mate](https://illurianish.github.io/Mind-Mate) to try out MindMate!

Backend API: [https://mindmate-backend-f35c.onrender.com](https://mindmate-backend-f35c.onrender.com)

## 🛠️ Tech Stack

- **Frontend:**
  - React with TypeScript
  - Material-UI (MUI)
  - Axios for API calls
  - GitHub Pages for hosting

- **Backend:**
  - Flask (Python)
  - OpenAI API
  - SQLite Database
  - Render.com for hosting

## 📋 Prerequisites

- Node.js (v14 or higher)
- Python 3.11
- OpenAI API key

## 🔧 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/illurianish/Mind-Mate.git
   cd Mind-Mate
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env     # Create your .env file
   ```

3. **Configure environment variables**
   - Open `.env` file
   - Add your OpenAI API key: `OPENAI_API_KEY=your-key-here`

4. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   ```

5. **Start the development servers**
   ```bash
   # Terminal 1 (Backend)
   cd backend
   flask run --port=5002

   # Terminal 2 (Frontend)
   cd frontend
   npm start
   ```

## 🚀 Deployment

### Frontend (GitHub Pages)
The frontend is automatically deployed to GitHub Pages when changes are pushed to the main branch. Visit [https://illurianish.github.io/Mind-Mate](https://illurianish.github.io/Mind-Mate)

### Backend (Render.com)
The backend is hosted on Render.com with automatic deployments from the main branch. The API is available at [https://mindmate-backend-f35c.onrender.com](https://mindmate-backend-f35c.onrender.com)

Note: The backend service may take up to 50 seconds to respond after periods of inactivity (free tier limitation).

## 🔒 Security Notes

1. Never commit your `.env` file
2. Keep your OpenAI API key secure
3. Use environment variables for sensitive data
4. Implement rate limiting in production

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Developer

Created by [Anish Reddy Illuri](https://illurianish.com/)

## ⚠️ Disclaimer

MindMate is not a replacement for professional mental health services. If you're experiencing a mental health crisis, please contact professional help or call 988 for immediate support.
