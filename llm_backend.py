from groq import Groq
from dotenv import load_dotenv
from tools.search_tool import web_search  # your custom tool
from tools.google_search_tool import google_search #custom tool

load_dotenv()

def run_agent(messages: list):
    """
    messages: a list of dicts like [{"role": "user", "content": "Find the latest AI news"}]
    """

    client = Groq()
    search_keywords = ['latest', 'find', 'news', 'updated','today', 'search','recent' ]

    try:
        # Get the latest user message
        user_message = messages[-1]["content"]

        # Check if any search keyword is present
        if any(word in user_message.lower().split() for word in search_keywords):
            # Run the web search
            search_result = google_search(user_message)

        return search_result
    
    except Exception as e:
        print(f"Error occurred: {e}")

        # Fallback completion in case of an error
        completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            max_tokens=300,
            temperature=0.2
        )
        return completion.choices[0].message.content


































# # Initialize LLM
# llm = HuggingFaceEndpoint(
#     repo_id='openai/gpt-oss-safeguard-20b',
#     max_new_tokens=100
# )

# model=ChatHuggingFace(llm=llm)

# Initialize tools
# search_tool = DuckDuckGoSearchRun()
# tools = [search_tool]

# # # Define prompt template
# # prompt = ChatPromptTemplate.from_messages([
# #     ("system", "You are a helpful AI assistant."),
# #     ("human", "{'input'}")
# # ])

# # Create agent (new location for create_openai_functions_agent)
# agent = create_agent(
#     model=model,
#     tools=tools
# )

# Function for running the agent
# def run_agent(query: str):
#     response = agent.invoke(
#         {"messages": [{"role": "user", "content": query}]},
#         context={"user_role": "expert"}
#     )
#     return response['messages'][1].content