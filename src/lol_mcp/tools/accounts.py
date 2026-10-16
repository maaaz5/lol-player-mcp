from mcp.server.fastmcp import FastMCP
from lol_mcp.riot_client import RiotClient

def register_account_tools(mcp: FastMCP, riot_client: RiotClient):
    @mcp.tool()
    async def get_player_profile(game_name: str, tag_line: str = "") -> dict:
        """Look up a League player using their Riot ID.

        Args:
            game_name: The player's Riot ID game name (e.g., 'MAAAZ5' or 'MAAAZ5#8371').
            tag_line: The player's tagline (e.g., '8371' or 'EUW'). Do NOT include '#'.
        """
        # If the model passes "Name#Tag" in game_name
        if "#" in game_name:
            parts = game_name.split("#", 1)
            game_name = parts[0]
            if not tag_line or "#" in tag_line:
                tag_line = parts[1]

        # Strip '#' or any duplicate name from tag_line
        if "#" in tag_line:
            tag_line = tag_line.split("#")[-1]

        game_name = game_name.strip()
        tag_line = tag_line.strip()

        account = await riot_client.get_account(game_name, tag_line)

        return {
            "game_name": account["gameName"],
            "tag_line": account["tagLine"],
            "puuid": account["puuid"],
        }

    @mcp.tool()
    async def get_player_mastery(puuid: str) -> list:
        """Fetches champion mastery details for a League of Legends player by their PUUID.

        Retrieves all champion mastery entries for the specified player, including champion
        IDs, mastery levels, total mastery points, and last played timestamps.

        Args:
            puuid: The Player Universally Unique Identifier (PUUID).
                Obtain this first using the `get_player_profile` tool.

        Returns:
            list[dict]: A list of champion mastery objects containing details such as
                championId, championLevel, championPoints, lastPlayTime,
                championPointsSinceLastLevel, and tokensEarned.
        """
        return await riot_client.get_champion_mastery(puuid)
