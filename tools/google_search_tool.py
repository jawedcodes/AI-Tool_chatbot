from langchain_google_community import GoogleSearchAPIWrapper, GoogleSearchRun
from dotenv import load_dotenv
import os

load_dotenv()


def google_search(message : str):
    # Initialize the API wrapper with your keys
    api_wrapper = GoogleSearchAPIWrapper(
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        google_cse_id=os.getenv("GOOGLE_CSE_ID")
    )

    # Pass wrapper into the tool
    search = GoogleSearchRun(api_wrapper=api_wrapper)

    # Run a search query
    results = search.run(message)
    return results
