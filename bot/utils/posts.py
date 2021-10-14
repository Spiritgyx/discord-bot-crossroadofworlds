import os, sys
import json
from bot.mylogger import MyLogger

logger = MyLogger('utils', filename='utils.log')


def get_all_posts():
    """Function get all json files in ./custom/posts/*.json and insert it to dictionary
    @return: posts: dict
    """
    post_list = os.listdir(os.getcwd()+'/custom/posts/')
    posts: dict = {}
    for post_path in post_list:
        if post_path.startswith('_'):
            # Ignore posts files with starting name "_..."
            continue
        try:
            with open(os.getcwd()+'/custom/posts/'+post_path, mode="r") as post_file:
                data: dict = json.load(post_file)
            obj_name = data.get('object_name', None)
            if obj_name and obj_name not in posts.keys():
                posts[obj_name] = data
            else:
                raise Exception(f"Not exists param 'object_name' in {post_path}")
        except Exception as e:
            logger.error(e, exc_info=sys.exc_info())
            continue
    return posts


def get_post(objname: str):
    all_posts = get_all_posts()
    if objname in all_posts.keys():
        return all_posts[objname]
    else:
        return None


