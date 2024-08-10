from openai import OpenAI
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging
import json
from time import sleep

logger = logging.getLogger(__name__)

def create_web_search_function(google_api_key, google_search_engine_id):
    def search_web(query):
        try:
            service = build("customsearch", "v1", developerKey=google_api_key, cache_discovery=False)
            result = service.cse().list(q=query, cx=google_search_engine_id).execute()
            return json.dumps(result.get('items', []))
        except HttpError as e:
            logger.error(f"An error occurred: {e}")
            return json.dumps([])
        except Exception as e:
            logger.error(f"Error in web search: {str(e)}")
            return json.dumps([])

    return search_web


def create_ai_assistant(client, google_api_key, google_search_engine_id):
    try:
        search_web = create_web_search_function(google_api_key, google_search_engine_id)
        
        assistant = client.beta.assistants.create(
            instructions="You are a helpful AI assistant that can search the web and provide movie recommendations.",
            name="Movie Recommender",
            tools=[{
                "type": "function",
                "function": {
                    "name": "search_web",
                    "description": "Search the web for information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query"
                            }
                        },
                        "required": ["query"]
                    }
                }
            }],
            model="gpt-4o"
        )
        
        logger.info(f"AI Assistant created with ID: {assistant.id}")
        return assistant, search_web
    except Exception as e:
        logger.error(f"Error creating AI assistant: {str(e)}")
        return None, None


def create_thread(client):
    try:
        thread = client.beta.threads.create()
        logger.info(f"Thread created with ID: {thread.id}")
        return thread
    except Exception as e:
        logger.error(f"Error creating thread: {str(e)}")
        return None

def get_movie_recommendations(client, assistant, thread, watch_history, search_web):
    try:
        # Add a message to the thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=f"Based on this watch history: {', '.join(watch_history)}, can you recommend 10 movies? For each movie, provide a short summary without any spoilers. Format your response as a numbered list."
        )

        # Create a run
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        # Wait for the run to complete or require action
        while True:
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if run.status in ["completed", "requires_action"]:
                break
            sleep(1)  # Wait for a second before checking again

        # If the run requires action (i.e., needs to use the web search function)
        if run.status == "requires_action":
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []

            for tool_call in tool_calls:
                if tool_call.function.name == "search_web":
                    arguments = json.loads(tool_call.function.arguments)
                    query = arguments.get("query")
                    try:
                        search_results = search_web(query)
                    except Exception as e:
                        logger.error(f"Error calling search_web function: {str(e)}")
                        search_results = json.dumps([])
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": search_results
                    })


            # Submit the tool outputs
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

            # Wait for the run to complete after submitting tool outputs
            while True:
                run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
                if run.status == "completed":
                    break
                sleep(1)

        # Retrieve the assistant's response
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        assistant_responses = [msg for msg in messages if msg.role == "assistant"]
        
        # Get the latest assistant response
        if assistant_responses:
            latest_response = assistant_responses[0]
            return latest_response.content[0].text.value
        else:
            logger.warning("No assistant response found")
            return ""

    except Exception as e:
        logger.error(f"Error getting movie recommendations: {str(e)}")
        try:
            delete_ai_assistant(client, assistant.id)
        except Exception:
            logger.error("Unable to delete assistant.")
        return ""
    
def delete_ai_assistant(client, assistant_id):
    try:
        response = client.beta.assistants.delete(assistant_id)
        logger.info(f"AI Assistant deleted: {response}")
    except Exception as e:
        logger.error(f"Error deleting AI assistant: {str(e)}")
