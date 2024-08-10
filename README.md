# AI Movie Recommender

## 🎬 Description

AI Movie Recommender is a Python application that leverages your Plex watch history and OpenAI's GPT model to generate personalized movie recommendations. It retrieves your recent watch history from Plex, uses an AI to analyze your preferences, and sends you an email with 10 tailored movie recommendations, complete with brief, spoiler-free summaries.

## 🚀 Features

- 📺 Fetches your recent Plex watch history
- 🤖 Utilizes OpenAI's GPT model for intelligent movie recommendations
- 🔍 Incorporates web search capabilities for up-to-date information
- 📧 Sends recommendations via email in a beautifully formatted HTML format
- 🔐 Secure handling of API keys and sensitive information

## 🛠 Installation

1. Clone the repository
2. Install the required dependencies
pip install -r requirements.txt
3. Set up your environment variables by creating a `.env` file in the project root:
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key
GOOGLE_SEARCH_ENGINE_ID=your_google_search_engine_id
SMTP_HOST=your_smtp_host
SMTP_FROM=your_email@example.com
SMTP_FROM_NAME="AI Movie Recommendations"
SMTP_PORT=465
SMTP_USERNAME=your_email@example.com
SMTP_PASSWORD=your_email_password
SMTP_SECURITY=ssl
SMTP_AUTH_MECHANISM=Plain
PLEX_AUTH_TOKEN=your_plex_auth_token
PLEX_USER_ID=your_plex_user_id


## 🖥 Usage

Run the main script:
python main.py


The application will:
1. Fetch your recent Plex watch history
2. Generate movie recommendations based on your history
3. Send an email with the recommendations

## 📁 Project Structure

- `main.py`: The entry point of the application
- `plex_history.py`: Handles fetching the Plex watch history
- `ai_assistant.py`: Manages the AI assistant for generating recommendations
- `email_sender.py`: Handles formatting and sending the email
- `utils.py`: Contains utility functions for logging and environment variable management

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

