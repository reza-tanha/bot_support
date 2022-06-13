from operator import imod
from config.celery import app
from telegram.instagram import Post_Download, Story_Download
from telegram.functions import *


@app.task(name="Post_Download_task")
def Post_Download_Task(link, user_id, message_id):
    return Post_Download(link, user_id, message_id)

@app.task(name="Story_Download_task")
def Story_Download_Task(link, user_id, message_id):
    return Story_Download(link, user_id, message_id)

@app.task(name="Story_Download_task")
def Story_Download_Task(link, user_id, message_id):
    return Story_Download(link, user_id, message_id)

@app.task(name="UsersBot_Count_Task")
def UsersBot_Count_Task():
    return UsersBot_count()

@app.task(name="GetSponserChannel_Task")
def GetSponserChannel_Task():
    return GetSponsers()


@app.task(name="AddSponserChannel_Task")
def AddSponserChannel_Task(username):
    return AddSponsers(username)

@app.task(name="DelSponserChannel_Task")
def DelSponserChannel_Task(username):
    return DelSponsers(username)

@app.task(name="Send_Tabliq_Forward_Task")
def Send_Tabliq_Forward_Task(chat_id, from_chat_id, message_id):
    return Send_Tabliq_Forward(chat_id, from_chat_id, message_id)

@app.task(name="Send_Tabliq_Normal_Task")
def Send_Tabliq_Normal_Task(chat_id, from_chat_id, message_id):
    return Send_Tabliq_Normal(chat_id, from_chat_id, message_id)


@app.task(name="UserCheckSponsers_Task")
def UserCheckSponsers_Task(user_id):
    return UserCheckSponsers(user_id)

