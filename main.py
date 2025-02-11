import praw

import tickers
import config
import models

def main():
    # Create a Reddit instance
    reddit = praw.Reddit(
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent=config.user_agent,
    )
    submission_limit = config.submission_limit

    # TODO: query run id from database
    run_id = 1

    subreddit = reddit.subreddit('wallstreetbets')
    print("Fetching new {submission_limit} posts from r/{subreddit.display_name} run id {run_id}")

    ticker_db = tickers.Tickers()

    mentions = []
    # TODO: Find the appropriate sort
    for submission in subreddit.new(limit=submission_limit):
        for word in submission.title.split():
            if word.upper() in ticker_db.symbols:
                print(f"Title: {submission.title} Tickers: {word}")
                mentions.append(models.Mention.from_submission(submission, run_id, word.upper()))

        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            if isinstance(comment, praw.models.MoreComments):
                # TODO: Handle MoreComments
                raise Exception("MoreComments not handled")
            for word in comment.body.split():
                if word.upper() in ticker_db.symbols:
                    print(f"Comment body: {comment.body} Tickers: {word}")
                    mentions.append(models.Mention.from_comment(comment, run_id, word.upper()))

    print(f"Found {len(mentions)} mentions")

    # TODO: If mentioned, store that in the database.


if __name__ == "__main__":
    main()
