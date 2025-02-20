import discord
import asyncio
from discord.ext import commands
import openai
import yt_dlp as youtube_dl

TOKEN = "NzkwMTA0MTU4MzI1NDQwNTQz.GRnXyK.nl1CcCgnGZXos1d0oegaJf-AcC9bm-OjMBtibQ"  # Botのトークン
CHANNEL_ID = 1340872102391189554  # メッセージを送るチャンネルのID

intents = discord.Intents.default()
intents.message_content = True  # これを有効化しないとコマンドを受け付けない
bot = commands.Bot(command_prefix="!", intents=intents)  # コマンドを受け付けるようにする
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'ログインしました: {client.user}')
    await send_message()

#####コマンド操作実装
@bot.event
async def on_ready():
    print(f'ログインしました: {bot.user}')
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("📢 Botが起動しました！")

@bot.command()
async def send(ctx):
    """コマンド"""
    await ctx.send("なまむぎなまごめなまたまご")

@bot.command()
async def play(ctx, url: str):
    # ボイスチャンネルに接続
    if ctx.author.voice is None:
        await ctx.send("ボイスチャンネルに入ってからコマンドを使ってね！")
        return
    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()

    # YouTubeの音源を取得
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['url']
    # 音楽を再生
    voice_client.play(discord.FFmpegPCMAudio(audio_url), after=lambda e: print("再生終了"))

    await ctx.send(f"🎶 **{info['title']}** を再生するよ！")



@bot.command()
async def shutdown(ctx):
    """Botを停止するコマンド"""
    await ctx.send("🔴 Botを停止します...")
    await bot.close()  # Botをシャットダウン

    

async def send_message():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("📢 データ共有しました！")
    else:
        print("チャンネルが見つかりません")



if __name__ == "__main__":
    bot.run(TOKEN)