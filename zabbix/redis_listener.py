#!/usr/bin/python3
from pyrogram import Client
import redis

TELEGRAM_API_TOKEN = '345345345345:0000000000000000000000000000000000'
API_HASH = '0000000000000000000000000000000000'
API_ID = 3123123123
CHAT_ID = -123123123123


app = Client("notify_bot", API_ID, API_HASH, bot_token=TELEGRAM_API_TOKEN, ipv6=True)
app.start()

redis_client = redis.Redis(host='localhost', port=6379, db=0, password='oozee4ad')
pubsub = redis_client.pubsub()
pubsub.subscribe('zabbix')
for message in pubsub.listen():
    if message['data'] != 1:
        app.send_message(CHAT_ID, message["data"].decode("utf-8"), parse_mode="markdown")
