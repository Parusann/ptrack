"""Application settings, loaded from environment variables or a .env file."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=("../.env", ".env"), extra="ignore")

    database_url: str = ""

    fedex_api_url: str = "https://apis-sandbox.fedex.com"
    fedex_api_key: str = ""
    fedex_secret_key: str = ""

    ups_api_url: str = "https://wwwcie.ups.com"
    ups_client_id: str = ""
    ups_client_secret: str = ""

    dhl_api_key: str = ""

    canadapost_customer_number: str = ""
    canadapost_api_key: str = ""
    canadapost_api_secret: str = ""

    seventeentrack_api_key: str = ""
    geoapify_api_key: str = ""

    telegram_bot_token: str = ""
    telegram_chat_id: str = ""

    jwt_secret: str = "change-me"

    def configured_carriers(self) -> list[str]:
        """Carriers that have credentials set, without exposing the values."""
        carriers = {
            "fedex": bool(self.fedex_api_key and self.fedex_secret_key),
            "ups": bool(self.ups_client_id and self.ups_client_secret),
            "dhl": bool(self.dhl_api_key),
            "canadapost": bool(self.canadapost_api_key and self.canadapost_api_secret),
            "17track": bool(self.seventeentrack_api_key),
        }
        return [name for name, ready in carriers.items() if ready]


@lru_cache
def get_settings() -> Settings:
    return Settings()
