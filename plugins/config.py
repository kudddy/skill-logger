import yaml
from typing import Dict, Any

from pydantic import BaseModel


def yaml_config_settings_source() -> Dict[str, Any]:
    """
    A simple settings source that loads variables from a JSON file
    at the project's root.

    Here we happen to choose to use the `env_file_encoding` from Config
    when reading `config.json`
    """
    try:
        with open("config/prod.yaml", 'r') as stream:
            config = yaml.safe_load(stream)
    except:
        with open("function/config/prod.yaml", 'r') as stream:
            config = yaml.safe_load(stream)
    return config


class Main(BaseModel):
    host: str
    port: int
    use_graph_ql: bool
    update_cache_every: int


class Url(BaseModel):
    tlg: str


class Auth(BaseModel):
    token_for_reg_bots: str
    url: str
    key: str
    secret: str


class TokenMap(BaseModel):
    sberauto: str


class App(BaseModel):
    main: Main
    url: Url
    auth: Auth
    token_map: TokenMap


class Settings(BaseModel):
    app: App


setting = Settings(**yaml_config_settings_source())


