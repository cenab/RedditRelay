import logging
import time
from typing import List
import praw
from praw.exceptions import APIException, PRAWException

from .config import Config


class RedditPoster:
    def __init__(self, config: Config):
        self.config = config
        self.reddit = praw.Reddit(
            client_id=config.reddit_credentials["client_id"],
            client_secret=config.reddit_credentials["client_secret"],
            username=config.reddit_credentials["username"],
            password=config.reddit_credentials["password"],
            user_agent=config.reddit_credentials["user_agent"],
        )
        self.title = config.post_content["title"]
        self.body = config.post_content["body"]
        self.subreddits = config.subreddits
        self.logger = logging.getLogger(__name__)

    def post_to_subreddits(self):
        for subreddit_name in self.subreddits:
            try:
                self.logger.info(f"Posting to r/{subreddit_name}...")
                subreddit = self.reddit.subreddit(subreddit_name)
                subreddit.submit(self.title, self.body)
                self.logger.info(f"Successfully posted to r/{subreddit_name}.")
                time.sleep(10)  # Delay to respect API rate limits
            except APIException as api_err:
                self.logger.error(f"APIException while posting to r/{subreddit_name}: {api_err}")
            except PRAWException as praw_err:
                self.logger.error(f"PRAWException while posting to r/{subreddit_name}: {praw_err}")
            except Exception as e:
                self.logger.error(f"Unexpected error while posting to r/{subreddit_name}: {e}")
