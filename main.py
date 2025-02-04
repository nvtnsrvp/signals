import praw
import tickers

import config

def main():
    # Create a Reddit instance
    reddit = praw.Reddit(
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent=config.user_agent,
    )
    limit = 1
    subreddit = reddit.subreddit('wallstreetbets')
    print("Fetching hot {limit} posts from r/{subreddit.display_name}")

    tickers = tickers.Tickers()

    # TODO: Find the appropriate sort
    for submission in subreddit.hot(limit=limit):
        print(f"Title: {submission.title}")
        print(f"Score: {submission.score}")
        print(f"Id: {submission.id}")
        print(f"URL: {submission.url}")
        for top_level_comment in submission.comments:
            if isinstance(top_level_comment, praw.models.MoreComments):
                continue
            for comment in top_level_comment.replies:
                if isinstance(comment, praw.models.MoreComments):
                    continue
                tickers = []
                for word in comment.body.split():
                    if word.lower() in tickers.symbols:
                        tickers.append(word)
                print(f"Body: {comment.body} Ticker: {words}")

        submission.comments.replace_more(limit=None)
            
        
        

if __name__ == "__main__":
    main()
