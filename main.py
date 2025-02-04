import praw

import config

def main():
    # Create a Reddit instance
    reddit = praw.Reddit(
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent=config.user_agent,
    )
    subreddit = reddit.subreddit('wallstreetbets')
    print(subreddit.display_name)

    # Get the top 5 posts from the Python subreddit
    for post in subreddit.top(limit=5):
        print(f"Title: {post.title}")
        print(f"Score: {post.score}")
        print(f"URL: {post.url}")

if __name__ == "__main__":
    main()
    