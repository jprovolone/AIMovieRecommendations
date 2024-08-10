from plexapi.myplex import MyPlexAccount
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def get_plex_history(auth_token, days=365):
    try:
        # Initialize the Plex account
        account = MyPlexAccount(token=auth_token)

        # Get the first available Plex server
        plex = account.resource(account.resources()[0].name).connect()

        # Calculate the date 30 days ago
        thirty_days_ago = datetime.now() - timedelta(days=days)

        # Get watch history
        history = plex.library.history()

        # Filter the history to only include movies from the last 30 days
        recent_history = [
            item for item in history
            if item.type == 'movie' and item.viewedAt > thirty_days_ago
        ]

        # Extract movie titles
        movie_titles = [item.title for item in recent_history]

        logger.info(f"Retrieved {len(movie_titles)} movies from Plex history")
        return movie_titles

    except Exception as e:
        logger.error(f"Error fetching Plex history: {str(e)}")
        return []
