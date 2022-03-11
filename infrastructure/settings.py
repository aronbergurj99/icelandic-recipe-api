from enum import Enum
from pydantic import BaseSettings

class ContainerSettingsEnum(Enum):
    def get(self, *argv):
        return self.value

class Environment(ContainerSettingsEnum):
    DEV= 'dev'
    PROD= 'prod'

class Settings(BaseSettings):

    environment: Environment
    dev_mongo_db_connection: str
    database: str
    
    secret: str
    algorithm: str

    class Config:
        env_file='.env'
        env_file_encoding='utf-8'