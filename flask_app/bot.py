import discord
import asyncio

TOKEN = "NzkwMTA0MTU4MzI1NDQwNTQz.GRnXyK.nl1CcCgnGZXos1d0oegaJf-AcC9bm-OjMBtibQ"  # Botのトークン
CHANNEL_ID = 1034696952333488188  # メッセージを送るチャンネルのID

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def send_message():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("📢 データ共有しました！")
        await channel.send("YuuYuuって天才だよね")
    else:
        print("チャンネルが見つかりません")

@client.event
async def on_ready():
    print(f'ログインしました: {client.user}')
    await send_message()

if __name__ == "__main__":
    asyncio.run(client.start(TOKEN))
