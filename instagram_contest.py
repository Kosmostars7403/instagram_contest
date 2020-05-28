from instabot import Bot
import os
import re
from dotenv import load_dotenv
import argparse


def get_marked_users(comment):
    marked_users = re.findall(r'@(\w*)', comment)
    return marked_users


def is_user_exist(username):
    user_id = bot.get_user_id_from_username(username)
    if user_id:
        return True
    else:
        return False


if __name__ == '__main__':
    load_dotenv()
    instagram_login = os.getenv('INSTAGRAM_LOGIN')
    instagram_password = os.getenv('INSTAGRAM_PASSWORD')
    post_owner = os.getenv('POST_OWNER')

    parser = argparse.ArgumentParser(description='Проводим конкурс в инстаграмм ')
    parser.add_argument('url', help='Ссылка на пост')
    args = parser.parse_args()
    post_url = args.url

    bot = Bot()
    bot.login(username=instagram_login, password=instagram_password)

    competing_users = set()

    media_id = bot.get_media_id_from_link(post_url)
    comments = bot.get_media_comments_all(media_id)
    likers = bot.get_media_likers(media_id)
    followers = bot.get_user_followers(post_owner)

    for comment in comments:
        marked_users = get_marked_users(comment['text'])
        for marked_user in marked_users:
            if is_user_exist(marked_user):
                if str(comment['user_id']) in likers:
                    if str(comment['user_id']) in followers:
                        match_user = (comment['user_id'], comment['user']['username'])
                        competing_users.add(match_user)
                        break

    for user in competing_users:
        print(user[1])