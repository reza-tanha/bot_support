from .telMethod import Telegram
import json
from .models import UserBot
from .config import *

def MainMenuUser():
    markup = {
        'keyboard':[
                ['⬇️ دانلود از اینستا ⬇️', '☎️ تماس با ما ☎️']
            ],
            'resize_keyboard':True
    }
    
    return json.dumps(markup)
    
def MainMenuAdmin():
    markup = {
        'keyboard':[
                ['users', 'sponser'],
                ['tabliq',],
                
            ],
            'resize_keyboard':True
    }
    
    return json.dumps(markup)
    

def Back():
    markup = {
        'keyboard':[
                ['بازگشت🏛']
            ],
            'resize_keyboard':True
    }
    
    return json.dumps(markup)
    

def ButtomInline_isJoin(user_id):
    markup = {
        'inline_keyboard':[
                [
                    {'text': 'عضو شدم', 'callback_data':f'IS_JOIN_{user_id}'},
                    {'text': 'کانال  ما', 'url':f'https://t.me/{CHANNEL_SPONSER}'}
                ]
            ]
        }
    
    return json.dumps(markup)

def ButtomInline_UserBlock_unblock(user_id):
    markup = {
        'inline_keyboard':[
                [
                    {'text': 'Block ❌', 'callback_data':f'USER_SENDMSG_BLOCK_{user_id}'},
                    {'text': 'UnBlock ✅', 'callback_data':f'USER_SENDMSG_UNBLOCK_{user_id}'}
                ]
            ]
        }
    
    return json.dumps(markup)

def AddUser_db(user_id, name=None,lastname=None, username=None):
    # try:
        user = UserBot.objects.create(
            user_id=user_id,
            name=name,
            lastname=lastname,
            username=username,
            isblock=False,
            step='home',
            tab=False
        )
        user.save()
        # print(user)
        return user
    # except:
    #     return False

def GetUser_db(user_id):
    user = UserBot.objects.filter(user_id=user_id).first()
    if user:
        return user
    return False

def Set_Step(user_id, step):
    user = UserBot.objects.filter(user_id=user_id).first()
    user.step = step
    user.save()
    return user