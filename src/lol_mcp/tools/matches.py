from mcp.server.fastmcp import FastMCP
from lol_mcp.riot_client import RiotClient

def register_match_tools(mcp: FastMCP, riot_client: RiotClient):
    @mcp.tool()
    async def get_player_matches_ids(puuid: str, count: int = 20) -> list:
        """Fetches a list of recent match IDs for a player by their PUUID.

        Retrieves the match history ID list (e.g., 'EUW1_1234567890') for the player.
        These match IDs can then be passed to `get_match_by_id` to retrieve detailed
        statistics for individual games.

        Args:
            puuid: The Player Universally Unique Identifier (PUUID).
                Obtain this first using the `get_player_profile` tool.
            count: Number of match IDs to return (default: 20).

        Returns:
            list[str]: A list of match ID strings for recent matches.
        """
        return await riot_client.get_match_ids(puuid, count=count)

    @mcp.tool()
    async def get_match_by_id(match_id: str) -> dict:
        """Fetches detailed match data and statistics for a specific match ID.

        Retrieves comprehensive game information including game duration, mode, participants'
        stats (kills, deaths, assists, items, damage, runes), team objectives (barons, dragons, towers),
        and win/loss results.

        Args:
            match_id: The unique match identifier (e.g., 'EUW1_7123456789').
                Obtain this from the `get_player_matches_ids` tool.

        Returns:
            dict: A dictionary containing match metadata and info payload with detailed participant
                stats and timeline information.
        """
        return await riot_client.get_match(match_id)


