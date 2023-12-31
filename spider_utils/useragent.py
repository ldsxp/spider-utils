version = '0.0.2'

import os
import random

from . import BASE_DIR

from fake_useragent import UserAgent

ua = UserAgent()

with open(os.path.join(BASE_DIR, 'data', 'mobile_user_agents.txt')) as f:
    mobile_user_agents = [i.strip() for i in f.readlines()]


def get_user_agent(is_mobile=False):
    """
    随机获取 User Agent
    """
    return random.choice(mobile_user_agents) if is_mobile else ua.random
