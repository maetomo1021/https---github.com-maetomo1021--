import discord
import asyncio

# TOKEN = "NzkwMTA0MTU4MzI1NDQwNTQz.GRnXyK.nl1CcCgnGZXos1d0oegaJf-AcC9bm-OjMBtibQ"  # あなたのBotのトークン
# 1212817500547317793
TOKEN = "MTMzNTI3NjM4NDU1MzAwOTI0NA.Gzvrhh.A0cWeTXJOTmzQcisu_dvVaG2eic_kdcEoRiLy4"  # YuuYuuのBotのトークン
CHANNEL_ID = 1335258050747174942  # メッセージを送るチャンネルのID

intents = discord.Intents.default()
client = discord.Client(intents=intents)
@client.event
async def on_ready():
    print(f'ログインしました: {client.user}')
    
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("こんにちは！Pythonからメッセージを送っています 🎉")
        await channel.send("YuuYuuって天才だよね")
        
    else:
        print("チャンネルが見つかりません")

    await client.close()  # メッセージ送信後にBotを終了

client.run(TOKEN)
