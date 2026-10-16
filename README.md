# lol-player-mcp

A **Model Context Protocol (MCP)** server for **League of Legends**, built with Python, FastMCP, and Riot Games API. 

This server allows AI assistants (Claude Desktop, Cursor, LangChain agents, Ollama, etc.) to query player accounts, retrieve ranked statistics, check champion masteries, and inspect match histories in real time.

---

## Features & Tools

The server registers 5 dedicated tools that AI models can invoke:

| Tool | Description |
| :--- | :--- |
| **`get_player_profile`** | Resolves a player's Riot ID (e.g. `GameName#TAG`) into their global PUUID. Built-in defensive parsing handles variations with or without `#`. |
| **`get_ranked_stats`** | Fetches active ranked league entries (Solo/Duo, Flex), calculating win rates, LP, divisions, streak status, and inactivity flags. Handles unranked players gracefully. |
| **`get_player_mastery`** | Fetches champion mastery entries, levels, points, and play timestamps by PUUID. |
| **`get_player_matches_ids`** | Retrieves recent match IDs for a player by their PUUID (supports custom `count`). |
| **`get_match_by_id`** | Retrieves detailed match statistics (kills, deaths, assists, items, objectives, game duration). |

---

## Quick Start

### 1. Prerequisites
- **Python 3.13+**
- [**uv**](https://docs.astral.sh/uv/) (recommended fast package manager)
- A **Riot Games API Key** from the [Riot Developer Portal](https://developer.riotgames.com/)

### 2. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/maaaz5/lol-player-mcp.git
cd lol-player-mcp
uv sync
```

### 3. Configuration
Copy the example environment file and add your Riot API key:
```bash
cp .env.example .env
```

Edit `.env`:
```env
RIOT_API_KEY=RGAPI-your-api-key-here
```

*(Optional config defaults in `Settings`: `platform_region="euw1"`, `regional_region="europe"`, `timeout_seconds=10.0`)*

### 4. Running the Server
Run the MCP server directly using the project script:
```bash
uv run lol-mcp
```
*(The server starts over `stdio` transport and listens for JSON-RPC messages from MCP clients).*

---

## Using with Claude Desktop or Cursor

Add the server to your `claude_desktop_config.json` (or Cursor MCP settings):

```json
{
  "mcpServers": {
    "lol-player-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/lol-player-mcp",
        "run",
        "lol-mcp"
      ],
      "env": {
        "RIOT_API_KEY": "RGAPI-your-api-key-here"
      }
    }
  }
}
```

---

## LangChain + Local Ollama Example

An end-to-end example is provided in [`src/examples/langchain_client.py`](src/examples/langchain_client.py) using `langchain-mcp-adapters` and a local `ChatOllama` model (e.g., `qwen3:1.7b`).

### Code:
```python
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
            tools = await load_mcp_tools(session)
            agent = create_agent(llm, tools)

            result = await agent.ainvoke({
                "messages": [
                    HumanMessage(content=(
                        "Find the League player, MAAAZ5#8371 and tell me their "
                        "current ranked stats. Give me a review about their playstyle "
                        "and their potential"
                    ))
                ]
            })
            print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
```

### Output:
```text
Here's a review of MAAAZ5#8371's ranked stats and playstyle:

---

### Ranked Stats Summary
Solo/Duo (EMERALD, IV):
Win Rate: 54.4% (86 wins, 72 losses)
LP: 25 | Total Games: 158
Flex (PLATINUM, I):
Win Rate: 60.9% (84 wins, 54 losses)
LP: 63 | Total Games: 138

Overall:
Consistent performance across both queues with a 54.4% win rate in Solo/Duo and 60.9% in Flex.
No hot streaks, veterans, or inactive status, indicating a balanced, active gameplay profile.

---

### Playstyle Analysis
Strengths:
Reliable performance in both ranked formats.
Strong win rate (60.9% in Flex) suggests effective playstyle with a focus on consistency.
No significant issues in game management or team strategies.

Potential Areas for Growth:
Flex Queue: The 60.9% win rate is slightly above the 54.4% in Solo/Duo, but could be improved by refining specific champions or playstyles.
Game Management: While LP numbers are low (25 and 63), maintaining a high win rate requires careful attention to game management and team strategy.
Champion Selection: Experimenting with different champions or playstyles might help optimize performance in specific queues.

---

### Conclusion
MAAAZ5#8371 is a skilled player with a solid ranked performance, particularly in Flex. Their consistency and low losses highlight a strong foundation, but opportunities to refine specific aspects of their game could elevate their ranked results further. Focus on balancing playstyles and game management to maximize win rates in both queues.
```

---

## Roadmap & Upcoming Features

- **Data Dragon Integration**: Integrate Riot's Data Dragon static asset CDN to resolve raw numeric IDs (champion IDs, item IDs, rune tree IDs, summoner spells) into human-readable champion names, item names, descriptions, and icon asset URLs.
- **Match Timeline Analysis**: Add tools to inspect objective bounties, gold differentials, and kill heatmaps.
- **Multi-region Routing Switcher**: Allow dynamically specifying platform and regional routing values directly in tool calls for multi-server player lookups.

---

## License

This project is licensed under the MIT License.
