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
num_of_day = 1


def print_next(message):
    global num_of_day
    await message.channel.send(schedule.strftime('%Y/%m/%d %H:%M') + ' - Day' + str(num_of_day))


client = discord.Client()


@tasks.loop(minutes=1)
async def loop():
    global schedule
    if channel is not None and datetime.datetime.now() >= schedule:
        await channel.send('@everyone のんだ？ - Day' + str(num_of_day))
        schedule += datetime.timedelta(minutes=INTERVAL)


@client.event
async def on_ready():
    print('ログインしました')


@client.event
async def on_message(message):
    global schedule
    global tomorrow_schedule
    global num_of_day
    global channel

    if message.content == '/help':
        await message.channel.send('(のんだ | すてた) : その日の通知を消します\n'
                                   'のむよ (mins) : その日の通知を延長します\n'
                                   '/init : Botを起動してから最初だけうつコマンド\n'
                                   '/next : 次に通知する時間\n'
                                   '/stop (days) : 指定した日数だけ通知を止める\n'
                                   '/reset : 通知を今日からする\n'
                                   '/day (day) : 次の通知日は何日目かをセットする')
    elif message.content == 'のんだ' or message.content == 'すてた':
        # 1時間以内かの判定
        margin = datetime.datetime.now()
        margin += datetime.timedelta(hours=1)
        if margin > schedule:
            schedule = tomorrow_schedule
            tomorrow_schedule += datetime.timedelta(days=1)
            await message.channel.send('Good! :)')

            num_of_day += 1
            if num_of_day > 28:
                num_of_day = 1
        else:
            await message.channel.send('Error')
    elif message.content == '/init':
        channel = message.channel
        await message.channel.send('何日目かをセットしてください. See help.')
    elif message.content == '/next':
        print_next(message)
    elif message.content.startswith('/stop '):
        days = message.content
        days = days[6:7]
        if days.isdecimal():
            schedule += datetime.timedelta(days=int(days))
            tomorrow_schedule += datetime.timedelta(days=int(days))
            print_next(message)
        else:
            await message.channel.send('Error')
    elif message.content == '/reset':
        schedule = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month,
                                     datetime.datetime.now().day, HOUR, MINUTE)
        tomorrow_schedule = schedule + datetime.timedelta(days=1)
        print_next(message)
    elif message.content.startswith('のむよ '):
        mins = message.content
        mins = mins[4:7]
        if mins.isdecimal():
            schedule += datetime.timedelta(minutes=int(mins))
            print_next(message)
        else:
            await message.channel.send('Error')
    elif message.content == '/day ':
        day = message.content
        day = day[5:7]
        if day.isdecimal():
            num_of_day = int(day)
        else:
            await message.channel.send('Error')


loop.start()
# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
