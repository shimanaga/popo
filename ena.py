import asyncio
import traceback
import discord
from discord.ext import commands
from discord import ui, app_commands
from discord.app_commands import describe
import os
import random

TOKEN = os.environ.get("BOT_TOKEN")
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)
tree = bot.tree
MAIN_GUILD = bot.get_guild(1400145776381919272)

admin_id = [447551013763678208]

@tree.command(name="gacha", guild=MAIN_GUILD, description="10連ガチャを回します。")
async def gacha(interaction: discord.Interaction):
    if interaction.channel_id != 1400194814624141392 and interaction.channel_id != 1048878265168842792:
        await interaction.response.send_message("このチャンネルでは使用できません。", ephemeral=True)
        return
    XXR = ["ボブ", "ジム", "えな"]
    SSR = ["ぶち殺すゾウ", "デスおぶし", "おふとん", "藤田ことね［雨上がりのアイリス］", "ぽっぽちゃん", "くるぶし", "ダイナマイトボディエナガ"]
    SR = ["田中 オイ太郎", "歩きエナガ", "ヒトデマン", "メスガキ", "ムキムキエナガ", "プリン", "ずんちゃ", "お寿司（サーモン）", "高速黙りモード移行男"]
    R = ["オフロスキー", "栗きんとん", "カニンジャ", "ラーメン", "ぐんぐんグルト", "強奪王ブンドルド", "立つドン", "デカハリル", "作品4", "ツャツャエナガ"]
    N = ["キウイマン", "舞う！！！！馬", "マイバチ（1本）", "たこ焼き", "ミ＝ゴス", "ポッピンクッキン ホイップケーキやさん", "縦連", "オタマトーン", "3ヶ月目のカレー", "パピコ", "お寿司（たまご）", "肩幅うさぎ", "ネギ", "15円玉", "雪降り、メソクソ", "イーロン・マスク", "アメリカセンダングサ","醤油", "Dutedimpianekepusaan-分散的絶望夢-", "判定線抱き枕"]
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

@tree.command(name="ieo", guild=MAIN_GUILD, description="インエナガチャを回します。")
@describe(n='試行回数を指定してください。')
async def ieo(interaction: discord.Interaction, n: int):
    if interaction.channel_id != 1400194814624141392 and interaction.channel_id != 1048878265168842792:
        await interaction.response.send_message("このチャンネルでは使用できません。", ephemeral=True)
        return
    if n < 1 or n > 30000:
        if interaction.user.id in admin_id and n <= 500000:
            pass
        else:
            await interaction.response.send_message("試行回数は1回から30000回までで指定してください。", ephemeral=True)
            return
    TARGET = "INFiNiTE ENERZY -Overdoze-"
    PARTS = ["INFiNiTE", "ENERZY", "-Overdoze-"]
    OUTPUT_FILE = "ieo_log.txt"
    log = []
    max_similarity = -1
    closest_string = ""
    closest_index = -1
    closest_match_counts = []
    closest_group_lengths = []

    for i in range(1, n + 1):
        shuffled_parts = []
        for part in PARTS:
            if part == "-Overdoze-":
                middle = part[1:-1]
                shuffled = "-" + ''.join(random.sample(middle, len(middle))) + "-"
            else:
                shuffled = ''.join(random.sample(part, len(part)))
            shuffled_parts.append(shuffled)

        result = ' '.join(shuffled_parts)
        log.append(result)
        if result == TARGET:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                for line in log:
                    f.write(line + "\n")
            await interaction.response.send_message(f"{i}回目でINFiNiTE ENERZY -Overdoze-が出現しました！",file=discord.File(OUTPUT_FILE))
            return
        similarity = sum(result[j] == TARGET[j] for j in range(len(TARGET)))
        if similarity > max_similarity:
            max_similarity = similarity
            closest_string = result
            closest_index = i
            target_parts = TARGET.split(' ')
            result_parts = result.split(' ')
            closest_match_counts = []
            closest_group_lengths = []
            for idx in range(3):
                target = target_parts[idx]
                res = result_parts[idx]
                match_count = sum(1 for a, b in zip(target, res) if a == b)
                closest_match_counts.append(match_count)
                closest_group_lengths.append(len(target))
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for line in log:
            f.write(line + "\n")
    group_rates = [
        f"{closest_match_counts[i]}/{closest_group_lengths[i]} "
        for i in range(3)
    ]
    total_match = sum(closest_match_counts)
    total_length = sum(closest_group_lengths)
    total_mismatch = total_length - total_match
    total_rate = total_match / total_length * 100
    await interaction.response.send_message(f"{n}回の試行中にINFiNiTE ENERZY -Overdoze-は出現しませんでした。\n最も近かったのは{closest_index}回目の {closest_string} でした。\n一致数: {' | '.join(group_rates)}\n一致率: {total_match}/{total_length} ({total_rate:.1f}%, -{total_mismatch})",file=discord.File(OUTPUT_FILE))

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
