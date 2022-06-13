from ast import Try
from time import sleep

from .messages import MESSAGES
from .telMethod import Telegram
import json
from .models import UserBot, SponserChannel
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
    
def SponserMenuAdmin():
    markup = {
        'keyboard':[
                ['Add', 'Del'], 
                ['بازگشت🏛',]               
            ],
            'resize_keyboard':True
    }
    
    return json.dumps(markup)
    

def TabliqMenuAdmin():
    markup = {
        'keyboard':[
                ['Forward', 'Normal'], 
                ['بازگشت🏛',]               
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



def Send_Tabliq_Forward(chat_id, from_chat_id, message_id):
    bot = Telegram()
    users = UserBot.objects.all()
    for user in users:
        bot.forward_Message(user.user_id, from_chat_id, message_id)
        sleep(3.5)
    bot.send_Message(chat_id, MESSAGES['MSG_TABLIQ_SENDEID_SUCCESS_ADMIN']) 
    return True

def Send_Tabliq_Normal(chat_id, from_chat_id, message_id):
    bot = Telegram()
    users = UserBot.objects.all()
    for user in users:
        bot.copy_Message(user.user_id, from_chat_id, message_id)
        sleep(3.5)
    bot.send_Message(chat_id, MESSAGES['MSG_TABLIQ_SENDEID_SUCCESS_ADMIN']) 
    return True


#==========
#Database Function
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


def UsersBot_count():
    return UserBot.objects.all().count()


def GetSponsers():
    sponsers =  SponserChannel.objects.all()
    return [sponser.username for sponser in sponsers ]


def AddSponsers(username):
    try:
        new = SponserChannel.objects.create(username=username)
        new.save()
        return True
    except:
        return 

def DelSponsers(username):
    try:
        SponserChannel.objects.filter(username=username).first().delete()
        return True
    except:
        return 


def UserCheckSponsers(user_id):
    bot = Telegram()
    sponsers = GetSponsers()
    for sponser in sponsers:
        # print(sponser)
        is_join = bot.user_Joined("@"+sponser, user_id)
        if is_join['result']['status'] == 'left':
            return False
    return True

