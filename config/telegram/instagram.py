from requests import get, post, session
import requests
import re
from .telMethod import Telegram
from .functions import *
from .messages import MESSAGES
from .config import *

def Post_Download(link, user_id, message_id):
    bot = Telegram()
    DATA = {
            'link':link,
            'downloader':'photo'
            }
    HEADER = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
            'referer': 'https://igdownloader.com/',
            'x-requested-with': 'XMLHttpRequest',
    }
    try:
        result = post('https://igdownloader.com/ajax', data=DATA, headers=HEADER, timeout=150).json()
        if result['error']:
            return False
        links = re.findall(r'href="(https:.*?)"\sclass="download-button">', result['html'])

        if len(links) == 0:
            bot.send_Message(user_id, MESSAGES['MSG_LINK_NOTVALID_BLOCKED'], reply_to_message_id=message_id)
            return
        for link in links:
            bot.send_Message(user_id, MESSAGES['MSG_LINKS_POSTS'].format(link),parse_mode="HTML", reply_to_message_id=message_id)
        return
        # return links
    except:
        return False

# Post_Download('https://www.instagram.com/p/CerGrsSuGxp/?utm_source=ig_web_copy_link')

counter = 0
def Story_Download(username, user_id, message_id):
    global counter
    bot = Telegram()
    request = session()
    HEADER = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'referer': 'https://www.instagramsave.com/instagram-story-downloader.php',
        'x-requested-with': 'XMLHttpRequest',
}
    result = request.get('https://www.instagramsave.com/instagram-story-downloader.php', headers=HEADER)
    token = re.findall(r'<input\stype="hidden"\sname="token"\sid="token"\svalue="(.*)">', result.text)

    DATA = {
            'url': f"https://www.instagram.com/{username}",
            "action":'story',
            "token":token[0],
            }
    try:
        result = request.post('https://www.instagramsave.com/system/action.php', data=DATA, headers=HEADER, timeout=150).json()
        links = []

        for item in result['medias']:
            links.append(item['url'])
        
        if len(links) == 0 and counter < 3:
            Story_Download(username)
            counter+=1
        # return links
        if len(links) == 0:
            bot.send_Message(user_id, MESSAGES['MSG_LINK_NOTVALID_BLOCKED'], reply_to_message_id=message_id)
            return
        for link in links:
            bot.send_Message(user_id, MESSAGES['MSG_LINKS_POSTS'].format(link),parse_mode="HTML", reply_to_message_id=message_id)
        return
        # return links
    except:
        pass

# print(Story_Download('online_shop_afkhami'))