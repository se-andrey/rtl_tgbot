import os
from dotenv import load_dotenv
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str


@dataclass
class DbUrl:
    url: str
    db_name: str
    db_collection: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbUrl


def load_config(path: str | None = None) -> Config:
    load_dotenv(path)
    return Config(
        tg_bot=TgBot(
            token=os.getenv('TG_TOKEN'),
        ),
        db=DbUrl(
            url=os.getenv('DB_URL'),
            db_name=os.getenv('DB_NAME'),
            db_collection=os.getenv('DB_COLLECTION')
        )
    )


