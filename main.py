import praw

import config
import models
import postgres
import tickers

class Reddit:
    def __init__(self, database: postgres.PostgresConnection, limit: int):
        # Create a Reddit instance
        self.reddit = praw.Reddit(
            client_id=config.client_id,
            client_secret=config.client_secret,
            user_agent=config.user_agent,
        )
        self.submission_limit = limit
        self.db = database
        self.ticker_db = tickers.Tickers()

    def extract_symbols(self, text: str):
        for word in text.split():
            if word.upper() in self.ticker_db.symbols:
                print(f"Text: {text} Tickers: {word}")
                yield word.upper()

    def run(self):
        subreddit = self.reddit.subreddit('wallstreetbets')
        run_id = self.db.insert_run(self.submission_limit)
        print("Fetching new {self.submission_limit} posts from r/{subreddit.display_name} run id {run_id}")

        mentions = []
        # TODO: Find the appropriate sort
        for submission in subreddit.new(limit=self.submission_limit):
            for symbol in self.extract_symbols(submission.title):
                mentions.append(models.Mention.from_submission(submission, run_id, symbol))

            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                if isinstance(comment, praw.models.MoreComments):
                    # TODO: Handle MoreComments
                    raise Exception("MoreComments not handled")
                for symbol in self.extract_symbols(comment.body):
                    mentions.append(models.Mention.from_comment(comment, run_id, symbol))
        print(f"Found {len(mentions)} mentions")

        # TODO: When each batch of posts is fetched, asynchronously insert mentions.
        self.db.insert_mentions(mentions)


def main():
    postgre = postgres.PostgresConnection()
    postgre.init_database()

    reddit = Reddit(postgre, config.limit)
    reddit.run()


if __name__ == "__main__":
    main()
