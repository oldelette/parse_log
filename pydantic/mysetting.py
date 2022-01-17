import os
from dotenv import load_dotenv
from pydantic import BaseModel, BaseSettings

class SwitchInfo(BaseModel):
    DEFAULT_USER: str
    DEFAULT_PWD: str
    DEFAULT_PORT: int

class LoginConfig(BaseModel):
    """base setting"""
    RETRY_INTERVAL: int
    RETRY: int
    SWITCH: SwitchInfo

class ScpConfig(LoginConfig):
    """scp setting"""

class SshConfig(LoginConfig):
    """ssh setting"""


class Settings(BaseSettings):
    SSH: SshConfig
    SCP: ScpConfig

    
    class Config:
        env_nested_delimiter = '__'
        env_file = '.env'

# print(Settings().dict())
settings = Settings()
print(settings)
print(settings.SSH.SWITCH.DEFAULT_USER)
