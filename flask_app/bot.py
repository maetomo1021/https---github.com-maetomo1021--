import discord
import asyncio

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




if __name__ == "__main__":
    asyncio.run(client.start(TOKEN))
