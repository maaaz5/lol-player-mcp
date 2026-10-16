from dotenv import load_dotenv
import os 

load_dotenv()

ACCOUNT_EUW_RIOT_API = "https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id"
RANKED_EUW_RIOT_API = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid"
MATCHES_EUW_RIOT_API = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid"
MATCH_EUW_RIOT_API = "https://europe.api.riotgames.com/lol/match/v5/matches"
CHAMPION_MASTERY_EUW_RIOT_API = "https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid"



headers = {
    "X-Riot-Token": os.environ["RIOT_API_KEY"]
}
