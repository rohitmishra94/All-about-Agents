

import nest_asyncio
nest_asyncio.apply()


import asyncio
import os
from dataclasses import dataclass
from typing import Any

from devtools import debug
from httpx import AsyncClient
import datetime
from duckduckgo_search import DDGS
from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic import BaseModel, Field


@dataclass
class SearchDataclass:
    max_results: int
    todays_date: str

@dataclass
class ResearchDependencies:
    todays_date: str

class ResearchResult(BaseModel):
    research_title: str = Field(description='This is a top level Markdown heading that covers the topic of the query and answer prefix it with #')
    research_main: str = Field(description='This is a main section that provides answers for the query and research')
    research_bullets: str = Field(description='This is a set of bulletpoints that summarize the answers for query')

## Make the agent
search_agent = Agent('openai:gpt-4o',
                     deps_type=ResearchDependencies,
                     result_type=ResearchResult,
                     system_prompt='Your a helpful research assistant, you are an expert in research '
                     'If you are given a question you write strong keywords to do 3-5 searches in total '
                     '(each with a query_number) and then combine the results' )

@search_agent.tool # DDGS
async def get_search(search_data:RunContext[SearchDataclass],query: str) -> dict[str, Any]:
    """Get the search for a keyword query.

    Args:
        query: keywords to search.
    """
    print(f"Search query: {query}")
    max_results = search_data.deps.max_results
    results = DDGS().text(query, max_results=max_results)

    return results


@search_agent.system_prompt
async def add_current_date(ctx: RunContext[ResearchDependencies]) -> str:
    todays_date = ctx.deps.todays_date
    system_prompt=f'Your a helpful research assistant, you are an expert in research \
                If you are given a question you write strong keywords to do 10-15 searches in total \
                (each with a query_number) and then combine the results \
                if you need todays date it is {todays_date} Provide result in context of India'
    return system_prompt

# Get the current date
current_date = datetime.date.today()

# Convert the date to a string
date_string = current_date.strftime("%Y-%m-%d")


deps = SearchDataclass(max_results=3, todays_date=date_string)


async def main():
  topic = '''Year 2024 What top 5 mutual fund should i invest to get best return in 3 years?, if i have to invest 3 lac around these, what should be allocation ratio between these large, mid and small cap fund, answer in detail""")
  '''
  result = await search_agent.run(
    topic, deps=deps
)
  combined_markdown = "\n\n".join([result.data.research_title, result.data.research_main, result.data.research_bullets])

  print(combined_markdown)

if __name__ == "__main__":

  asyncio.run(main())
