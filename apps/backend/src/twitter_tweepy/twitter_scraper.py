import os
from dotenv import load_dotenv
load_dotenv()
from twscrape import API


async def get_twitter_posts():
    """Get twitter posts."""
    api = API()
    user_name = os.getenv("USER")
    password = os.getenv("PASSWORD")
    email = os.getenv("EMAIL")
    await api.pool.add_account(user_name, password, email, password)
    await api.pool.login_all()
    user_name = os.getenv("USER")
    lst = []
    async for tweet in api.search(user_name):
        lst.append(tweet.rawContent)
    return lst

