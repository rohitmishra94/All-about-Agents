# %%writefile multiagent_test.py

import re
import requests
from markdownify import markdownify
from requests.exceptions import RequestException
from smolagents import tool
from dotenv import load_dotenv
print('env variable loaded: ',load_dotenv('env'))


@tool
def scrape_page_with_jina_ai(url: str) -> str:
    """Scrapes content from a webpage using Jina AI's web scraping service.

    Args:
        url: The URL of the webpage to scrape. Must be a valid web address to extract content from.

    Returns:
        str: The scraped content in markdown format.
    """
    print(f"Scraping Jina AI..: {url}")
    headers = {
    "Authorization": "Bearer jina_62808ae9263144f683110ea3fe305fe4Qan_BELZfG5VXuGdNDF3Gq6i3-ac"
}
    response = requests.get("https://r.jina.ai/" + url, headers=headers)
    
    markdown_content = response.text

    return markdown_content


from smolagents import (
    CodeAgent,
    ToolCallingAgent,
    HfApiModel,
    ManagedAgent,
    DuckDuckGoSearchTool,
    LiteLLMModel,
)


model_id = "Qwen/Qwen2.5-Coder-32B-Instruct"
# model = HfApiModel(model_id)
model = LiteLLMModel(model_id="gpt-4o-mini")


web_agent = ToolCallingAgent(
    tools=[DuckDuckGoSearchTool(), scrape_page_with_jina_ai],
    model=model,
    max_steps=5,
)

managed_web_agent = ManagedAgent(
    agent=web_agent,
    name="search",
    description="Runs web searches for you. Give it your query as an argument.",
)

checker_agent = ToolCallingAgent(
    tools=[],
    model=model
)

managed_checker_agent = ManagedAgent(
    agent=checker_agent,
    name="research_checker",
    description="Checks the research for relevance to the original task request. If the research is not relevant, it will ask for more research.",
)

answer_agent = ToolCallingAgent(
    tools=[],
    model=model,
)

managed_answer_agent = ManagedAgent(
    agent=answer_agent,
    name="answer",
    description="Provide answer in  with heading and pointers for searched topic",
)

manager_agent = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[managed_web_agent,managed_answer_agent,managed_checker_agent],
    additional_authorized_imports=["time", "numpy", "pandas"],
)

if __name__ == "__main__":
  # answer = manager_agent.run("""year 2024 What top 5 mutual fund should i invest to get best return in 3 years?, if i have to invest 3 lac around these, what should be allocation ration between these large, mid and small cap fund, answer in detail""")
  # print(answer)
    topic = '''Year 2024 What top 5 mutual fund should i invest to get best return in 3 years?, if i have to invest 3 lac around these, what should be allocation ratio between these large, mid and small cap fund, answer in detail""")
  '''
    answer = manager_agent.run(f"""Create a blog post about: {topic}
    1. First, research the topic thoroughly, focus on specific products and sources
    2. Then, write an engaging blog post""")
    print(answer)
