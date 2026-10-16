from lol_mcp.config import Settings
import httpx
from urllib.parse import quote
from typing import Any


class RiotClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.http = httpx.AsyncClient(
            headers={
                "X-Riot-Token": settings.riot_api_key
            },
            timeout=settings.timeout_seconds,
        )

    async def get(
        self, base_url: str, path: str, **params
    ) -> Any:
        response = await self.http.get(
            f"{base_url}{path}",
            params=params or None,
        )
        response.raise_for_status()
        return response.json()

    async def get_account(
        self, game_name: str, tag_line: str
    ) -> dict:
        encoded_name = quote(game_name, safe="")
        encoded_tag = quote(tag_line, safe="")
        return await self.get(
            f"https://{self.settings.regional_region}.api.riotgames.com",
            f"/riot/account/v1/accounts/by-riot-id/{encoded_name}/{encoded_tag}",
        )

    async def get_ranked_entries(
        self, puuid: str
    ) -> list:
        return await self.get(
            f"https://{self.settings.platform_region}.api.riotgames.com",
            f"/lol/league/v4/entries/by-puuid/{puuid}",
        )

    async def get_champion_mastery(
        self, puuid: str
    ) -> list:
        return await self.get(
            f"https://{self.settings.platform_region}.api.riotgames.com",
            f"/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}",
        )

    async def get_match_ids(
        self, puuid: str, count: int = 20
    ) -> list:
        return await self.get(
            f"https://{self.settings.regional_region}.api.riotgames.com",
            f"/lol/match/v5/matches/by-puuid/{puuid}/ids",
            count=count,
        )

    async def get_match(
        self, match_id: str
    ) -> dict:
        return await self.get(
            f"https://{self.settings.regional_region}.api.riotgames.com",
            f"/lol/match/v5/matches/{match_id}",
        )

    async def close(self):
        await self.http.aclose()