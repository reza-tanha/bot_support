from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from .telMethod import Telegram
from asgiref.sync import async_to_sync, sync_to_async



def sendMessage(chat_id, text):
    url  = 'https://api.telegram.org/bot5050400232:AAEeEApl-0geyNvmjfvW0ciInIubAiNS8Ck/'
    method = 'sendMessage?'
    url = url+method+f'chat_id={chat_id}&text={text}'
    requests.get(url)

# @sync_to_async
@csrf_exempt
@async_to_sync
async def update(request):
    bot = Telegram()
    try:
        json_message = json.loads(request.body)
        text = json_message['message']['text'] if "text" in json_message['message'] else None

        if "message" in json_message:
            # return json_message
            if "chat" in json_message['message']: chat_id = json_message['message']['chat']['id']
            text = json_message['message']['text'] if "text" in json_message['message'] else None
            
            # if "text" in json_message['message']:text=json_message['message']['text']
            # else:text=None

        elif "callback_query" in json_message:
            pass
        
        print("="*100)
        print(json_message)
        print("="*100)
        print(text) 
        await bot.send_Message(chat_id, text='<b>hello </b>', parse_mode="HTML")
        # await bot.forward_Message(chat_id, -1001586217111 ,40)
        # file = open('/root/Desktop/Code/python/django/bot/A/telegram/vi.mp4', 'rb').read()
        file = "BAACAgQAAxkBAAIN62KUi_hDI7mGh2hvH7V1pDN-RePeAAJYCwACC8OoUAutQ02J7gGnJAQ"
        await bot.send_Video(chat_id, file)

        return HttpResponse('status 200')
    except json.decoder.JSONDecodeError as err:
        return HttpResponse(str(err))



@csrf_exempt
@async_to_sync
async def mesages_normal(request):
    pass
