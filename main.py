import discord
from discord.ext import tasks
import datetime

TOKEN = ''  # TOKENを入力する
HOUR = 22
MINUTE = 10
INTERVAL = 3

schedule = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, HOUR, MINUTE)
tomorrow_schedule = schedule + datetime.timedelta(days=1)
channel = None

client = discord.Client()


@tasks.loop(minutes=1)
async def loop():
    global schedule
    if channel is not None and datetime.datetime.now() >= schedule:
        await channel.send('@everyone のんだ？')
        schedule += datetime.timedelta(minutes=INTERVAL)


@client.event
async def on_ready():
    print('ログインしました')


@client.event
async def on_message(message):
    global schedule
    global tomorrow_schedule
    if message.content == '/help':
        await message.channel.send('のんだ : その日の通知を消します\n'
                                   '/init : Botを起動してから最初だけうつコマンド\n'
                                   '/next : 次に通知する時間\n'
                                   '/stop [days] : 指定した日数だけ通知を止める\n'
                                   '/reset : 通知を今日からする')
    if message.content == 'のんだ':
        margin = datetime.datetime.now()
        margin += datetime.timedelta(hours=1)
        if margin > schedule:
            schedule = tomorrow_schedule
            tomorrow_schedule += datetime.timedelta(days=1)
            await message.channel.send('Good! :)')
        else:
            await message.channel.send('Error')
    elif message.content == '/init':
        global channel
        channel = message.channel
    elif message.content == '/next':
        await message.channel.send(schedule.strftime('%Y/%m/%d %H:%M'))
    elif message.content.startswith('/stop '):
        days = message.content
        days = days[6:8]
        if days.isdecimal():
            schedule += datetime.timedelta(days=int(days))
            tomorrow_schedule += datetime.timedelta(days=int(days))
            await message.channel.send(schedule.strftime('%Y/%m/%d %H:%M'))
        else:
            await message.channel.send('Error')
    elif message.content == '/reset':
        schedule = datetime.datetime.now()
        schedule -= datetime.timedelta(seconds=schedule.second)
        tomorrow_schedule = schedule + datetime.timedelta(days=1)
        await message.channel.send(schedule.strftime('%Y/%m/%d %H:%M'))


loop.start()
# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
