import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
  riot_api_key: str
  platform_region: str = "euw1"
  regional_region: str = "europe"
  timeout_seconds: float = 10.0

def load_settings() -> Settings:
  api_key = os.getenv("RIOT_API_KEY")

  if not api_key:
      raise RuntimeError(
          "RIOT_API_KEY environment variable is required"
      )

  return Settings(riot_api_key=api_key)
