version = '0.0.2'

import os
import random

from fake_useragent import UserAgent

# fake-useragent fake_useragent.json 下载： https://fake-useragent.herokuapp.com/browsers/0.1.11
ua = UserAgent(path=os.path.join('data', 'fake_useragent_0.1.11.json'))

with open(os.path.join('data', 'mobile_user_agents.txt')) as f:
    mobile_user_agents = [i.strip() for i in f.readlines()]


def get_user_agent(is_mobile=False):
    """
    随机获取 User Agent
    """
    return random.choice(mobile_user_agents) if is_mobile else ua.random
