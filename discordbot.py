import os
from random import choice
import pya3rt

import discord

from settings import CHANNEL_ID, EMOJI, QUESTION_TXT, questions42, ignorelists

TOKEN = os.environ.get('TOKEN')

Apikey = os.environ.get('SECRET_TOKEN')
clients = pya3rt.TalkClient(Apikey)

client = discord.Client()


async def reply_nop(message):
    """
    返信とリアクションスタンプをランダムでをつける
    """
    emoji = discord.utils.get(message.guild.emojis, name=choice(EMOJI))
    reply = f'こんにちは。\n他の受講生に相談してみましょう！'
    await message.channel.send(reply)
    await message.add_reaction(emoji)


async def angry_nop(message):
    """
    返信とリアクションスタンプをランダムでをつける
    """
    emoji = discord.utils.get(message.guild.emojis, name=choice(EMOJI))
    reply = f'こんにちは。\n自分で考えてみましょう！\nわからない場合は不合格にします！'
    await message.channel.send(reply)
    await message.add_reaction(emoji)


async def nomal_reply(message):
    """
    返信とリアクションスタンプをランダムでをつける
    """
    emoji = discord.utils.get(message.guild.emojis, name=choice(EMOJI))
    reply_message = clients.talk(message)
    reply = reply_message['results'][0]['reply']
    await message.channel.send(reply)
    await message.add_reaction(emoji)


def is_question(text):
    """
    疑問文か判定
    :param text:    判定する文章
    :return:        bool
    """
    for question_txt in QUESTION_TXT:
        if text.find(question_txt) >= 0:
            return 1
        elif text.find(questions42) >= 0:
            return 2
        elif text.find(ignorelists) >= 0:
            return 3


@client.event
async def on_ready():
    """
    botのサーバログイン時に実行
    """
    print('ログインしました')


@client.event
async def on_message(message):
    """
    メッセージが送信されると起動
    :param message: 送信されたメッセージ
    """
    if message.author.bot:
        return
    if message.channel.id != CHANNEL_ID:
        return
    if client.user in message.mentions:
        await reply_nop(message)
    elif is_question(message.content) == 1:
        await nomal_reply(message)
    elif is_question(message.content) == 2:
        await reply_nop(message)
    elif is_question(message.content) == 3:
        await angry_nop(message)


client.run(TOKEN)
