import asyncio

from src.labs.L1_1_sync_chat import sync_chat
from src.labs.L1_2_async_chat import async_chat
from src.labs.L2_1_web_search_tool import web_search_tool

def run(): 
    # chat()
    # asyncio.run(async_chat())
    web_search_tool()


if __name__ == '__main__': 
    run()