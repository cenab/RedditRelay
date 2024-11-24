import configparser
from pathlib import Path
import re


class Config:
    def __init__(self, config_file: Path):
        self.parser = configparser.ConfigParser(allow_no_value=True)
        # Enable raw string reading to preserve formatting
        self.parser.optionxform = str
        
        # Read the file content
        with open(config_file, 'r') as f:
            content = f.read()
        
        # Process triple-quoted strings
        processed_content = self._process_triple_quotes(content)
        
        # Read the processed content
        self.parser.read_string(processed_content)

    def _process_triple_quotes(self, content: str) -> str:
        """Process triple-quoted strings in config content."""
        # Find all triple-quoted blocks
        pattern = r'(\w+)\s*=\s*"""(.*?)"""'
        
        def replace_quotes(match):
            key = match.group(1)
            value = match.group(2).strip()
            # Preserve newlines but escape them properly for configparser
            value = value.replace('\n', '\\n')
            return f'{key} = {value}'
        
        # Replace triple-quoted blocks with properly formatted strings
        return re.sub(pattern, replace_quotes, content, flags=re.DOTALL)

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
