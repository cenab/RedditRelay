import configparser
from pathlib import Path


class Config:
    def __init__(self, config_file: Path):
        self.parser = configparser.ConfigParser()
        self.parser.read(config_file)

    @property
    def reddit_credentials(self) -> dict:
        return {
            "client_id": self.parser.get("reddit", "client_id"),
            "client_secret": self.parser.get("reddit", "client_secret"),
            "username": self.parser.get("reddit", "username"),
            "password": self.parser.get("reddit", "password"),
            "user_agent": self.parser.get("reddit", "user_agent"),
        }

    @property
    def post_content(self) -> dict:
        return {
            "title": self.parser.get("post", "title"),
            "body": self.parser.get("post", "body"),
        }

    @property
    def subreddits(self) -> list:
        subreddits = self.parser.get("subreddits", "list")
        return [sub.strip() for sub in subreddits.split(",")]
