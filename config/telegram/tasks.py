from config.celery import app
from telegram.instagram import Post_Download, Story_Download

@app.task(name="Post_Download_task")
def Post_Download_Task(link, user_id, message_id):
    return Post_Download(link, user_id, message_id)


@app.task(name="Story_Download_task")
def Story_Download_Task(link, user_id, message_id):
    return Story_Download(link, user_id, message_id)
