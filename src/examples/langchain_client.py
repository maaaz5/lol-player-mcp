import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.tools import load_mcp_tools

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

llm = ChatOllama(model="qwen3:1.7b")

src_dir = str(Path(__file__).resolve().parents[1])
stdio_server_params = StdioServerParameters(
    command=sys.executable,
    args=["-m", "lol_mcp.server"],
    env={**os.environ, "PYTHONPATH": src_dir},
)

async def main():
  async with stdio_client(stdio_server_params) as (read, write):
    async with ClientSession(read_stream=read, write_stream=write) as session:
      await session.initialize()
      print("Session Initialize")
      tools = await load_mcp_tools(session)

      agent = create_agent(llm, tools)

      result = await agent.ainvoke({"messages":[HumanMessage(content= 
                    "Find the League player, MAAAZ5#8371 and tell me their current ranked stats. Give me a review about their playstyle and their potential")]})
      print(result["messages"][-1].content)


if __name__ == "__main__":
  asyncio.run(main())



