import logging
from pathlib import Path

from reddit_relay.config import Config
from reddit_relay.poster import RedditPoster


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def main():
    setup_logging()
    config_path = Path(__file__).parent / "config.ini"
    config = Config(config_path)
    poster = RedditPoster(config)
    poster.post_to_subreddits()


if __name__ == "__main__":
    main()
