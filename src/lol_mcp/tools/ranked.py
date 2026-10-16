from mcp.server.fastmcp import FastMCP
from lol_mcp.riot_client import RiotClient


QUEUE_NAMES = {
    "RANKED_SOLO_5x5": "Ranked Solo/Duo",
    "RANKED_FLEX_SR": "Ranked Flex",
    "RANKED_TFT_DOUBLE_UP": "TFT Double Up",
}


def register_ranked_tools(
    mcp: FastMCP,
    riot_client: RiotClient,
):
    @mcp.tool()
    async def get_ranked_stats(puuid: str) -> list:
        """Get current ranked entries and stats for a League player by their PUUID.

        Args:
            puuid: The Player Universally Unique Identifier (PUUID).
                Obtain this first using the `get_player_profile` tool.

        Returns:
            list[dict]: A list of ranked stats per queue (e.g., Solo/Duo, Flex)
                including tier, rank division, LP, wins, losses, win rate, streaks, and activity flags.
                If the player has no ranked games, returns an unranked status indicator.
        """
        entries = await riot_client.get_ranked_entries(puuid)

        # Edge case: Player has no ranked games / unranked
        if not entries:
            return [
                {
                    "status": "UNRANKED",
                    "message": "Player has not completed placements or played ranked games this season.",
                }
            ]

        results = []
        for entry in entries:
            queue_type = entry.get("queueType", "UNKNOWN")
            wins = entry.get("wins", 0)
            losses = entry.get("losses", 0)
            total_games = wins + losses
            win_rate = (
                round(100 * wins / total_games, 1)
                if total_games > 0
                else 0.0
            )

            results.append(
                {
                    "status": "RANKED",
                    "queue": queue_type,
                    "queue_name": QUEUE_NAMES.get(queue_type, queue_type),
                    "tier": entry.get("tier", "UNRANKED"),
                    "division": entry.get("rank", ""),
                    "lp": entry.get("leaguePoints", 0),
                    "wins": wins,
                    "losses": losses,
                    "total_games": total_games,
                    "win_rate": win_rate,
                    "hot_streak": entry.get("hotStreak", False),
                    "veteran": entry.get("veteran", False),
                    "fresh_blood": entry.get("freshBlood", False),
                    "inactive": entry.get("inactive", False),
                }
            )

        return results
