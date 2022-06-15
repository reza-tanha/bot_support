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


@app.task(name="Send_Tabliq_Forward_Task")
def Send_Tabliq_Forward_Task(chat_id, from_chat_id, message_id):
    return Send_Tabliq_Forward(chat_id, from_chat_id, message_id)

@app.task(name="Send_Tabliq_Normal_Task")
def Send_Tabliq_Normal_Task(chat_id, from_chat_id, message_id):
    return Send_Tabliq_Normal(chat_id, from_chat_id, message_id)

