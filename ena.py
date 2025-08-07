import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import describe
import os
import random

TOKEN = os.environ.get("BOT_TOKEN")
intents = discord.Intents.default()
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)
tree = bot.tree

admin_id = [447551013763678208]

@tree.command(name="gacha", description="10連ガチャを回します。")
async def gacha(interaction: discord.Interaction):
    if interaction.channel_id not in (1400194814624141392, 1048878265168842792):
        await interaction.response.send_message("このチャンネルでは使用できません。", ephemeral=True)
        return

    XXR = ["ボブ", "ジム", "えな"]
    SSR = ["ぶち殺すゾウ", "デスおぶし", "おふとん", "藤田ことね［雨上がりのアイリス］", "ぽっぽちゃん", "くるぶし", "ダイナマイトボディエナガ"]
    SR = ["田中 オイ太郎", "歩きエナガ", "ヒトデマン", "メスガキ", "ムキムキエナガ", "プリン", "ずんちゃ", "お寿司（サーモン）", "高速黙りモード移行男"]
    R = ["オフロスキー", "栗きんとん", "カニンジャ", "ラーメン", "ぐんぐんグルト", "強奪王ブンドルド", "立つドン", "デカハリル", "作品4", "ツャツャエナガ"]
    N = ["キウイマン", "舞う！！！！馬", "マイバチ（1本）", "たこ焼き", "ミ＝ゴス", "ポッピンクッキン ホイップケーキやさん", "縦連", "オタマトーン", "3ヶ月目のカレー", "パピコ", "お寿司（たまご）", "肩幅うさぎ", "ネギ", "15円玉", "雪降り、メソクソ", "イーロン・マスク", "アメリカセンダングサ","醤油", "Dutedimpianekepusaan-分散的絶望夢-", "判定線抱き枕"]

    result = ["## ガチャ結果"]
    for _ in range(10):
        f = random.randint(0, 100)
        if f == 0:
            result.append(f"**[XXR] {random.choice(XXR)}**")
        elif f <= 5:
            result.append(f"[SSR] {random.choice(SSR)}")
        elif f <= 15:
            result.append(f"[SR] {random.choice(SR)}")
        elif f <= 40:
            result.append(f"[R] {random.choice(R)}")
        else:
            result.append(f"[N] {random.choice(N)}")

    await interaction.response.send_message("\n".join(result))

@tree.command(name="ieo", description="インエナガチャを回します。")
@describe(n="試行回数を指定してください。", write_log="ログファイルを出力するかどうか（true/false）")
async def ieo(interaction: discord.Interaction, n: int, write_log: bool = False):
    if interaction.channel_id not in (1400194814624141392, 1048878265168842792):
        await interaction.response.send_message("このチャンネルでは使用できません。", ephemeral=True)
        return

    if not (1 <= n <= 30000) and not (interaction.user.id in admin_id and n <= 10000000):
        await interaction.response.send_message("試行回数は1回から30000回までで指定してください。", ephemeral=True)
        return

    await interaction.response.defer()

    TARGET = "INFiNiTE ENERZY -Overdoze-"
    PARTS = ["INFiNiTE", "ENERZY", "-Overdoze-"]
    OUTPUT_FILE = "ieo_log.txt"
    log = [] if write_log else None
    max_similarity = -1
    closest_string = ""
    closest_index = -1
    closest_match_counts = [0, 0, 0]
    closest_group_lengths = [8, 6, 8]

    for i in range(1, n + 1):
        shuffled_parts = [
            ''.join(random.sample(PARTS[0], 8)),
            ''.join(random.sample(PARTS[1], 6)),
            "-" + ''.join(random.sample(PARTS[2][1:-1], 8)) + "-"
        ]
        result = ' '.join(shuffled_parts)
        if write_log:
            log.append(result)

        if result == TARGET:
            if write_log:
                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                    f.write("\n".join(log))
                await interaction.followup.send(
                    f"{i}回目でINFiNiTE ENERZY -Overdoze-が出現しました！\n```一致数: 8/8 | 6/6 | 8/8\n一致率: 22/22 (100.0%, -0)```",
                    file=discord.File(OUTPUT_FILE)
                )
            else:
                await interaction.followup.send(
                    f"{i}回目でINFiNiTE ENERZY -Overdoze-が出現しました！\n```一致数: 8/8 | 6/6 | 8/8\n一致率: 22/22 (100.0%, -0)```"
                )
            return

        similarity = sum(result[j] == TARGET[j] for j in range(22))
        if similarity > max_similarity:
            max_similarity = similarity
            closest_string = result
            closest_index = i
            parts_res = result.split(' ')
            closest_match_counts[0] = sum(a == b for a, b in zip(PARTS[0], parts_res[0]))
            closest_match_counts[1] = sum(a == b for a, b in zip(PARTS[1], parts_res[1]))
            closest_match_counts[2] = sum(a == b for a, b in zip(PARTS[2][1:-1], parts_res[2][1:-1]))

    total_match = sum(closest_match_counts)
    total_length = sum(closest_group_lengths)
    total_rate = total_match / total_length * 100
    total_mismatch = total_length - total_match
    group_rates = [
        f"{closest_match_counts[i]}/{closest_group_lengths[i]}"
        for i in range(3)
    ]

    if write_log:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(log))
        await interaction.followup.send(
            f"{n}回の試行中にINFiNiTE ENERZY -Overdoze-は出現しませんでした。\n"
            f"最も近かったのは{closest_index}回目の {closest_string} でした。\n"
            f"```一致数: {'| '.join(group_rates)}\n一致率: {total_match}/{total_length} ({total_rate:.1f}%, -{total_mismatch})```",
            file=discord.File(OUTPUT_FILE)
        )
    else:
        await interaction.followup.send(
            f"{n}回の試行中にINFiNiTE ENERZY -Overdoze-は出現しませんでした。\n"
            f"最も近かったのは{closest_index}回目の {closest_string} でした。\n"
            f"```一致数: {'| '.join(group_rates)}\n一致率: {total_match}/{total_length} ({total_rate:.1f}%, -{total_mismatch})```"
        )

@bot.command()
async def s(ctx: commands.Context):
    if ctx.author.id not in admin_id:
        await ctx.send("このコマンドの使用は制限されています。", ephemeral=True)
        return
    await ctx.send("強制終了します。", ephemeral=True)
    await bot.close()

@bot.event
async def on_ready():
    await tree.sync()

bot.run(TOKEN)
