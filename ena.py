import asyncio
import discord
from discord.ext import commands
import traceback
from discord import ui, app_commands
import random

TOKEN = BOT_TOKEN
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)
tree = bot.tree
MAIN_GUILD = bot.get_guild(1400145776381919272)

@tree.command(name="gacha", guild=MAIN_GUILD, description="10連ガチャを回します。")
async def gacha(interaction: discord.Interaction):
    if interaction.channel_id != 1400194814624141392 or interaction.channel_id != 1048878265168842792:
        await interaction.response.send_message("このチャンネルでは使用できません。", ephemeral=True)
        return
    XXR = ["ボブ", "ジム", "えな"]
    SSR = ["ぶち殺すゾウ", "デスおぶし", "おふとん", "藤田ことね［雨上がりのアイリス］", "ぽっぽちゃん", "くるぶし"]
    SR = ["田中 オイ太郎", "歩きエナガ", "ヒトデマン", "メスガキ", "ムキムキエナガ", "プリン", "ずんちゃ", "お寿司（サーモン）"]
    R = ["オフロスキー", "栗きんとん", "カニンジャ", "ラーメン", "ぐんぐんグルト", "強奪王ブンドルド", "立つドン", "デカハリル", "作品4"]
    N = ["キウイマン", "舞う！！！！馬", "マイバチ（1本）", "たこ焼き", "ミ=ゴス", "ポッピンクッキン ホイップケーキやさん", "縦連", "オタマトーン", "3ヶ月目のカレー", "パピコ", "お寿司（たまご）", "肩幅うさぎ", "ネギ", "15円玉", "雪降り、メソクソ", "イーロン・マスク", "アメリカセンダングサ", "Dutedimpianekepusaan-分散的絶望夢-", "判定線抱き枕"]
    result = "## ガチャ結果\n"
    for i in range(10):
        f = random.randint(0, 100)
        if f == 0:
            result += "**[XXR] " + random.choice(XXR) + "**\n"
        elif f <= 5:
            result += "[SSR] " + random.choice(SSR) + "\n"
        elif f <= 15:
            result += "[SR] " + random.choice(SR) + "\n"
        elif f <= 40:
            result += "[R] " + random.choice(R) + "\n"
        else:
            result += "[N] " + random.choice(N) + "\n"
    await interaction.response.send_message(result)

@bot.command()
async def s(ctx: commands.context):
    if not ctx.author.id in admin_id:
        await interaction.response.send_message("このコマンドの使用は制限されています。", ephemeral = True)
        return
    await interaction.response.send_message("強制終了します。", ephemeral = True)
    await bot.close()

@bot.event
async def on_ready():
    await tree.sync(guild=MAIN_GUILD)

bot.run(TOKEN)
