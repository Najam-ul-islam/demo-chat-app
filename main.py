import asyncio

from src.labs.L1_1_sync_chat import sync_chat
from src.labs.L1_2_async_chat import async_chat
from src.labs.L2_1_web_search_tool import web_search_tool
from src.labs.L2_2_code_interpreter_tool import code_interpreter_tool
from src.labs.L4_rag_hybrid_search import run_agent




def run(): 
    # sync_chat()
    # asyncio.run(async_chat())
    # web_search_tool()
    # code_interpreter_tool()
    run_agent()
if __name__ == '__main__': 
    run()