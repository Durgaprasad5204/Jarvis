import logging
from livekit.agents import function_tool, RunContext
import requests
from langchain_community.tools import DuckDuckGoSearchRun

@function_tool()
async def get_weather(
        context: RunContext,
        city: str) -> str:
    
    """Fetches the current weather for a given city using a weather API"""

    try:
        response = requests.get(f"http://wttr.in/{city}?format=3")
        if response.status_code == 200:
            weather = response.text.strip()
            logging.info(f"Weather for {city}: {weather}")
            return weather
        else:
            logging.error(f"Failed to get weather for {city}: {response.text.strip()}")
            return f"Could not retrieve weather for {city}."
    except Exception as e:
        logging.error(f"Error retrieving weather for {city}: {str(e)}")
        return f"An error occurred while retrieving weather for {city}."

@function_tool()
async def search_web(
        context: RunContext,
        query: str) -> str:
    
    """Performs a web search using DuckDuckGo and returns the top result"""

    try:
        results = DuckDuckGoSearchRun().run(tool_input=query)
        logging.info(f"Search results for '{query}': {results}")
        return results
    except Exception as e:
        logging.error(f"Error performing web search for '{query}': {e}")
        return f"An error occurred while searching the web for '{query}'."
    
