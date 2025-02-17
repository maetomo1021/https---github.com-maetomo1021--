import discord
import asyncio
import requests
import json
from bs4 import BeautifulSoup

TOKEN = "NzkwMTA0MTU4MzI1NDQwNTQz.GRnXyK.nl1CcCgnGZXos1d0oegaJf-AcC9bm-OjMBtibQ"  # Botのトークン
CHANNEL_ID = 1337546857919938700  # メッセージを送るチャンネルのID

intents = discord.Intents.default()
intents.messages = True  # メッセージの取得を有効化
client = discord.Client(intents=intents)

async def send_message():
    # await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("📢 データ共有しました！")
    else:
        print("チャンネルが見つかりません")

@client.event
async def on_ready():
    print(f'ログインしました: {client.user}')
    asyncio.create_task(send_message())  # 非同期でメッセージ送信

async def hello(ctx):
    await ctx.send("こんにちは！")

# async def ShareJson(ctx,channel:discord.TextChannel,*,message):
#     await channel.send(message)
#     # !send #general で、generalチャンネルにメッセージを送信する　らしい


async def fetch_and_send():
    url = "http://127.0.0.1:5000/"  # FlaskのURL
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 必要なデータを取得
        title = soup.find("li").text
        content = soup.find("p", {"id": "content"}).text

        # JSONデータに加工
        data = {
            "title": title,
            "content": content,
            "url":url
        }
        json_data = json.dumps(data, indent=4, ensure_ascii=False)

        # Discordに送信
        channel = client.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(f"📢 データを取得しました！\n```json\n{json_data}\n```")
        else:
            print("チャンネルが見つかりません")
    else:
        print("Webページの取得に失敗しました")

if __name__ == "__main__":
    asyncio.run(client.start(TOKEN))
