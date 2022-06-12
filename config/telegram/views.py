from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from .telMethod import Telegram
# from asgiref.sync import async_to_sync, sync_to_async
from .functions import *
from .messages import MESSAGES
from .config import *
import re
from .instagram import Post_Download
from .tasks import *

@csrf_exempt
def MessegeCallback(request, update):
    print(update)
    bot = Telegram()
    callback_id = update['callback_query']['id'] if "id" in update['callback_query'] else None
    callback_data = update['callback_query']['data'] if "data" in update['callback_query'] else None
    callback_message_message_id = update['callback_query']['message']['message_id'] if "message" in update['callback_query'] else None
    callback_user_id = update['callback_query']['message']['from']['id'] if "message" in update['callback_query'] else None
    callback_chat_id = update['callback_query']['message']['chat']['id'] if "message" in update['callback_query'] else None

    # user_id_in = (array_key_exists('id',$update['callback_query']['from']))?$update['callback_query']['from']['id']:null;
    # user_id_from_replay_in = (array_key_exists('id',$update['callback_query']['message']['reply_to_message']['from']))?$update['callback_query']['message']['reply_to_message']['from']['id']:null;
    # chat_id_in = (array_key_exists('id',$update['callback_query']['message']['chat']))?$update['callback_query']['message']['chat']['id']:null;
    # text_in = (array_key_exists('text',$update['callback_query']['message']))?$update['callback_query']['message']['text']:null;
    # first_name_in = (array_key_exists('first_name',$update['callback_query']['from']))?$update['callback_query']['from']['first_name']:null;
    # lastname_in  = (array_key_exists('last_name',$update['callback_query']['from']))?$update['callback_query']['from']['last_name']:null;
    # username_in =  (array_key_exists('username',$update['callback_query']['from']))?$update['callback_query']['from']['username']:null;
    # message_id_in = (array_key_exists('message_id',$update['callback_query']['message']))?$update['callback_query']['message']['message_id']:null;
    # callback_in = (array_key_exists('data',$update['callback_query']))?$update['callback_query']['data']:null;
    # callback_id_in = (array_key_exists('id',$update['callback_query']))?$update['callback_query']['id']:null;
    # callback_text_in = (array_key_exists('text',$update['callback_query']['message']))?$update['callback_query']['message']['text']:null;
    # callback_text_from_replay_in = (array_key_exists('text',$update['callback_query']['message']['reply_to_message']))?$update['callback_query']['message']['reply_to_message']['text']:null;
    # callback_id_from_replay_in = (array_key_exists('id',$update['callback_query']['message']['reply_to_message']['from']))?$update['callback_query']['message']['reply_to_message']['from']['id']:null;


    if "IS_JOIN_" in callback_data:
        user_id_join = str(callback_data).split("_")[-1]
        is_join = bot.user_Joined(f'@{CHANNEL_SPONSER}', user_id_join)
        if is_join['result']['status'] == 'left':
            print(is_join['result']['status'])
            bot.send_AnswerCallbackQuery(callback_id, MESSAGES['MSG_CALLBACK_IS_JOIN'])
            return
        bot.send_Message(user_id_join, MESSAGES['HOME_STEP_USER'], reply_markup=MainMenuUser())
        bot.delete_Message(user_id_join, callback_message_message_id)
        Set_Step(user_id_join, 'home')
        return

    if "USER_SENDMSG_" in callback_data:
        data = str(callback_data).split("_")
        user = GetUser_db(data[-1])
        if data[2] == 'BLOCK':
            user.isblock=True
            user.save()
            bot.send_AnswerCallbackQuery(callback_id, MESSAGES['MSG_CALLBACK_USER_BLOCKED'].format(data[-1]) )
        else:
            user.isblock=False
            user.save()
            bot.send_AnswerCallbackQuery(callback_id, MESSAGES['MSG_CALLBACK_USER_BLOCKED'].format(data[-1]) )
        return

@csrf_exempt
def MessegeNormal(request, update):
    bot = Telegram()
    text = update['message']['text'] if "text" in update['message'] else None
    print(update)
    photo_file_id = update['message']['photo'][0]['file_id'] if "photo" in update['message'] else None
    document_file_id = update['message']['document']['file_id'] if "document" in update['message'] else None
    video_file_id = update['message']['video']['file_id'] if "video" in update['message'] else None
    audio_file_id = update['message']['audio']['file_id'] if "audio" in update['message'] else None
    voice_file_id = update['message']['voice']['file_id'] if "voice" in update['message'] else None
    reply_to_message_message_id = update['message']['reply_to_message']['message_id'] if "reply_to_message" in update['message'] else None
    user_id = update['message']['from']['id'] if "id" in update['message']['from'] else None
    username = update['message']['from']['username'] if "username" in update['message']['from'] else None
    name = update['message']['from']['first_name'] if "first_name" in update['message']['from'] else None
    chat_id = update['message']['chat']['id'] if "id" in update['message']['chat'] else None
    chat_type = update['message']['chat']['type'] if "type" in update['message']['chat'] else None
    message_id = update['message']['message_id'] if "message_id" in update['message'] else None




    try:
        reply_to_message_text = update['message']['reply_to_message']['text'] if "reply_to_message" in update['message'] else None
    except:
        reply_to_message_text = None

    user_info = GetUser_db(user_id)

    if not user_info:
        user_info = AddUser_db(
            user_id=user_id,
            name=update['message']['from']['first_name'],
            username=update['message']['from']['username'],        
        )

    is_join = bot.user_Joined("@"+CHANNEL_SPONSER, user_id)
    if is_join['result']['status'] == 'left' and user_id not in ADMINS_LIST:
        bot.send_Message(chat_id, MESSAGES['MSG_JOIN_MY_CHANNEL'], reply_markup=ButtomInline_isJoin(user_id))
        return 

    
    if text == '/start' and chat_type == 'private':
        bot.send_Message(chat_id, MESSAGES['HOME_STEP_USER'], reply_markup=MainMenuUser())
        Set_Step(user_id, 'home')
        return

    if text == '/admin' and chat_type == 'private' and user_id in ADMINS_LIST:
        bot.send_Message(chat_id, MESSAGES['MSG_HOME_STEP_ADMIN'], reply_markup=MainMenuAdmin())
        Set_Step(user_id, 'admin_home')
        return

    if reply_to_message_message_id:
        user_id_sender_msg = re.findall(r'user\sid\s:\s(\d*)\nname\s:\s.*', reply_to_message_text)
        if text:
            bot.send_Message(user_id_sender_msg[0], text, disable_web_page_preview=True)

        elif photo_file_id:
            bot.send_Photo(user_id_sender_msg[0], photo_file_id, disable_web_page_preview=True)

        elif document_file_id:
            bot.send_Document(user_id_sender_msg[0], document_file_id, disable_web_page_preview=True)
        
        elif document_file_id:
            bot.send_Document(user_id_sender_msg[0], document_file_id, disable_web_page_preview=True)
        
        elif video_file_id:
            bot.send_Video(user_id_sender_msg[0], video_file_id, disable_web_page_preview=True)
        
        elif audio_file_id:
            bot.send_Audio(user_id_sender_msg[0], audio_file_id, disable_web_page_preview=True)

        elif voice_file_id:
            bot.send_Voice(user_id_sender_msg[0], voice_file_id, disable_web_page_preview=True)

        else :
            return
        return

    step = user_info.step
    match step:
        case 'home':
            if text == '⬇️ دانلود از اینستا ⬇️':
                bot.send_Message(chat_id, MESSAGES['MSG_INSTA_DOWNLOAD_HOME'], reply_markup=Back())
                Set_Step(user_id, 'INSTA_DOWNLOAD')
                return

            elif text == '☎️ تماس با ما ☎️':
                bot.send_Message(chat_id, MESSAGES['MSG_CUNTACT_US'], reply_markup=Back())
                Set_Step(user_id, 'COUNTUCT_US')
                return
            

        case 'INSTA_DOWNLOAD':
            if text == 'بازگشت🏛':
                Set_Step(user_id, 'home')
                bot.send_Message(chat_id, MESSAGES['HOME_STEP_USER'], reply_markup=MainMenuUser())
                return
            elif '@' in text:
                Story_Download_Task.delay(text.replace('@', ''), user_id, message_id)
                return
            
            else:
                if 'instagram.com' in text:
                    Post_Download_Task.delay(text, user_id, message_id)
                    return

                    





        case 'COUNTUCT_US':
            if text == 'بازگشت🏛':
                Set_Step(user_id, 'home')
                bot.send_Message(chat_id, MESSAGES['HOME_STEP_USER'], reply_markup=MainMenuUser())
                return
            else:
                if user_info.isblock:
                    return
                bot.forward_Message(ADMINS_LIST[0], user_id, message_id)
                bot.send_Message(user_id,'ارسال شد')
                bot.send_Message(ADMINS_LIST[0],
                        MESSAGES['MSG_SUPPORTED_FORWARD_ADMIN'].format(user_id,name, username),
                        parse_mode='HTML',
                        reply_markup=ButtomInline_UserBlock_unblock(user_id),
                        )
                return

        
    match step:
        case 'admin_home':
            pass


            
                







    # if text == '/admin':
    #     bot = Telegram()
    #     bot.send_Message(user_id, 'wellcom admin', reply_markup=MainMenuAdmin())
    #     bot.send_Message(user_id, 'join', reply_markup=ButtomInline())
        

    # if text == '/start':
    #     pass
    #     # user = AddUser_db()


        



    #     user_info = GetUser_db(user_id)
        

    #     bot.send_Message(user_id, 'wellcom admin', reply_markup=MainMenuAdmin())
    #     bot.send_Message(user_id, 'join', reply_markup=ButtomInline())
        


 

# @sync_to_async
@csrf_exempt
def update(request):
    bot = Telegram()
    try:
        json_message = json.loads(request.body)
        if "message" in json_message:
            MessegeNormal(request, json_message)

        elif "callback_query" in json_message:
            MessegeCallback(request, json_message)

        return HttpResponse('status 200')
    except json.decoder.JSONDecodeError as err:
        return HttpResponse(str(err))

