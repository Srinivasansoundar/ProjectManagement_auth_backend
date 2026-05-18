from pydantic_settings import BaseSettings
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# print(Path(__file__).resolve())

class Settings(BaseSettings):
    DATABASE_URI:str
    SECRET_KEY:str
    ACCESS_TOKEN_EXPIRE_SECONDS:int
    REFRESH_TOKEN_EXPIRE_DAYS:int
    ALGORITHM:str
    
    
    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"

settings=Settings()