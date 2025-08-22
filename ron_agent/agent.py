from google.adk.agents import Agent
import os
from gnews import GNews

def get_news(event: str) -> str:
    """
    Retrieves the top 5 current news headlines for a specified topic using GNews.

    Args:
        event (str): The topic or keyword for which to retrieve news.
                     For general top stories, you can pass an empty string.

    Returns:
        str: A formatted string containing the top 5 headlines,
             or an error message if the request fails.
    """
    try:
        # Initialize the GNews client
        # You can specify language, country, and number of results
        gnews = GNews(language='en', country='US', max_results=5)

        # Fetch news for the given event/topic
        # If 'event' is empty, it will fetch top stories.
        if not event:
            articles = gnews.get_top_news()
        else:
            articles = gnews.get_news(event)

        # Check if articles were found
        if articles:
            # Format the articles into a single string
            formatted_news = "Here are the top 5 news stories:\n"
            for i, article in enumerate(articles):
                formatted_news += f"{i+1}. {article['title']}\n"
            return formatted_news
        else:
            return f"No news articles found for '{event}'."

    except Exception as e:
        # Handle potential errors like network issues
        return f"An error occurred while fetching news: {e}"


root_agent = Agent(
    name="Joke_Agent",
    model="gemini-2.0-flash",
    description=(
        "Provides jokes and witty insights to users regarding a their inquiry about current events."
    ),
    instruction=(
    """
    You are a funny agent with the personality of Ron Burgundy thats purpose is to make jokes and funny comments about current events in the news.

    If a user asks about a specific current event, you will respond in a Ron Burgundy way, by answering with some sort of accuracy, but a lot of nonsense thrown in there. You can retrieve information about the current state of the world with the 'get_news' tool.

    If a user asks about the news in general, you will respond in the same Ron Burgundy manner, but include all of the top stories not just the one they mentioned. Use the 'get_news' to retrieve the news.

    If you were not able to find any news, then just spew some nonsensical stories.

    Remember, your purpose is to provide a funny twist on the current news, in the same way that Ron Burgundy does.
    """
    ),
    tools=[get_news],
)