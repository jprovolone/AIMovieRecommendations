from utils import load_env_variables, setup_logging
from plex_history import get_plex_history
from openai import OpenAI
from ai_assistant import create_ai_assistant, create_thread, get_movie_recommendations, delete_ai_assistant
from email_sender import send_email

def main():
    # Setup logging
    logger = setup_logging()

    # Load environment variables
    env_vars = load_env_variables()

    try:
        # Get Plex watch history
        watch_history = get_plex_history(env_vars['PLEX_AUTH_TOKEN'])
        # print(watch_history)

        if not watch_history:
            logger.warning("No watch history found. Exiting.")
            return

        # In your main function:
        client = OpenAI(api_key=env_vars['OPENAI_API_KEY'])

        assistant, search_web_function = create_ai_assistant(client, env_vars['GOOGLE_API_KEY'], env_vars['GOOGLE_SEARCH_ENGINE_ID'])
        if not assistant:
            logger.error("Failed to create AI assistant. Exiting.")
            return

        thread = create_thread(client)
        if not thread:
            logger.error("Failed to create thread. Exiting.")
            return

        recommendations = get_movie_recommendations(client, assistant, thread, watch_history, search_web_function)
        # print(recommendations)

        if not recommendations:
            logger.warning("No recommendations generated. Exiting.")
            return

        # Send email
        subject = "AI Movie Recommendations"
        send_email(
            {k: env_vars[k] for k in env_vars if k.startswith('SMTP_')},
            subject,
            recommendations
        )

        # After sending email
        delete_ai_assistant(client, assistant.id)

        logger.info("Process completed successfully.")

    except Exception as e:
        logger.error(f"An error occurred in the main process: {str(e)}")

if __name__ == "__main__":
    main()
