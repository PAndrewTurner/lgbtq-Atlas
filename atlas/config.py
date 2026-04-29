from pathlib import Path
from pydantic_settings import BaseSettings

ROOT = Path(__file__).parent.parent


class Settings(BaseSettings):
    data_raw_dir: Path = ROOT / "data" / "raw"
    data_processed_dir: Path = ROOT / "data" / "processed"
    data_exports_dir: Path = ROOT / "data" / "exports"
    anthropic_api_key: str = ""
    fbi_api_key: str = ""
    census_api_key: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
