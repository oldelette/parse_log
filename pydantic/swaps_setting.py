import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    tftp_server: str
    tftp_path: str
    dhcp_server: str
    dhcp_path: str

    class Config:
        env_file = '.env'

class Production(Settings):
    # tftp_path= '/var/log/atftpd.log'
    tftp_server= 'isc-dhcp'

class Testing(Settings):
    # tftp_path= '/tmp/atftpd.log'
    tftp_server= 'kea-dhcp'

    class Config:
        env_file = '.test.env'

def get_settings():
    env = os.getenv('ENV', 'TESTING')
    if env == 'PRODUCTION':
        return Production()
    return Testing()
settings = get_settings()

print('setting =', settings)