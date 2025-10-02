import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import describe
import os
import random

TOKEN = os.environ.get("BOT_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)
tree = bot.tree

admin_id = [447551013763678208]
q_id = [736041262288863314, 1146920779695542282, 325699632036446212, 743312946955812946, 748104554456940545, 935384717971312660, 830582346767400971, 165918545975181312, 451040362094526490, 847816792932220938, 506825535272386581, 316906181174099970, 595811416351703101, 871743426620706847, 720937043328368680, 834389536510443540, 937539245415997471, 256690534582714368, 341211236496572428, 893874919878836294, 969227021345492992, 344004546504425473, 596886848605913098, 955087114859589702, 740956031625986199, 467064272212590602, 690852174267416646, 784973409654276126, 982236550161125398, 461725672658698267, 557485522344214529, 708298047184044122, 703431721483370518, 400864007507935240, 848596266094559313, 237711240632336384, 733977065627320361]
LOG_GUILD_ID = 1400145776381919272
LOG_CHANNEL_ID = 1048878265168842792

@tree.command(name="gacha", description="10連ガチャを回します。")
async def gacha(interaction: discord.Interaction):
    if interaction.channel_id not in (1400194814624141392, 1048878265168842792):
        await interaction.response.send_message("このチャンネルでは使用できません。", ephemeral=True)
        return

    Q = ["ベリーベリーベリーロングボブ", "ビッグジム"]
    XXR = ["ボブ", "ジム", "えな"]
    SSR = ["ぶち殺すゾウ", "デスおぶし", "おふとん", "藤田ことね［雨上がりのアイリス］", "ぽっぽちゃん", "くるぶし", "ダイナマイトボディエナガ"]
    SR = ["痣　少焼", "歩きエナガ", "ヒトデマン", "メスガキ", "ムキムキエナガ", "プリン", "ずんちゃ", "お寿司（サーモン）", "高速黙りモード移行男", "ドダイにしてみせるお姉さん", "横幅エナガ"]
    R = ["オフロスキー", "栗きんとん", "カニンジャ", "ラーメン", "ぐんぐんグルト", "強奪王ブンドルド", "立つドン", "デカハリル", "作品4", "ツャツャエナガ", "沖ノ鳥島"]
    N = ["キウイマン", "舞う！！！！馬", "マイバチ（1本）", "たこ焼き", "ミ＝ゴス", "ポッピンクッキン ホイップケーキやさん", "縦連", "オタマトーン", "3ヶ月目のカレー", "パピコ", "お寿司（たまご）", "肩幅うさぎ", "ネギ", "15円玉", "雪降り、メソクソ", "イーロン・マスク", "アメリカセンダングサ","醤油", "Dutedimpianekepusaan-分散的絶望夢-", "判定線抱き枕"]

    result = ["## ガチャ結果"]
    for _ in range(10):
        f = random.randint(0, 999)
        if f == 0:
            result.append(f"**[XXR] {random.choice(Q)}**")
        elif f <= 9:
            result.append(f"**[XXR] {random.choice(XXR)}**")
        elif f <= 49:
            result.append(f"[SSR] {random.choice(SSR)}")
        elif f <= 149:
            result.append(f"[SR] {random.choice(SR)}")
        elif f <= 399:
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

@tree.command(name="puki", description="プキプキガチャを回します。")
async def puki(interaction: discord.Interaction):
    if interaction.channel_id not in (1400194814624141392, 1048878265168842792):
        await interaction.response.send_message("このチャンネルでは使用できません。", ephemeral=True)
        return

    await interaction.response.defer()
    
    l = 10000
    choices = ["プ", "キ"]
    s = []

    s.append(random.choice(["プ", "キ"]))

    p = 0.88

    for _ in range(1, l):
        prev = s[-1]
        if random.random() < p:
            next_char = "キ" if prev == "プ" else "プ"
        else:
            next_char = prev
        s.append(next_char)

    s = "".join(s)

    max_len = 0
    max_start = 0
    max_end = 0

    current_start = None
    expected_char = "プ"
    current_len = 0

    for i, ch in enumerate(s):
        if current_len == 0:
            if ch == "プ":
                current_start = i
                current_len = 1
                expected_char = "キ"
        else:
            if ch == expected_char:
                current_len += 1
                expected_char = "プ" if expected_char == "キ" else "キ"
            else:
                if current_len >= 2 and s[i-1] == "キ":
                    if current_len > max_len:
                        max_len = current_len
                        max_start = current_start
                        max_end = i - 1
                if ch == "プ":
                    current_start = i
                    current_len = 1
                    expected_char = "キ"
                else:
                    current_len = 0
                    expected_char = "プ"

    if current_len >= 2 and s[-1] == "キ":
        if current_len > max_len:
            max_len = current_len
            max_start = current_start
            max_end = l - 1

    with open("result.txt", "w", encoding="utf-8") as f:
        f.write(s)

    max = s[max_start:max_end+1]

    if max_len < 100:
        await interaction.followup.send(f"{max_len}文字のプキプキが完成しました！({max_start}~{max_end}文字目)\n{'<:muscle_puku:1400271171093659658>'*(max_len//2)}",file=discord.File("result.txt"))
    else:
        await interaction.followup.send(f"{max_len}文字のプキプキが完成しました！({max_start}~{max_end}文字目)\n# <:muscle_puku:1400271171093659658> × {max_len//2}",file=discord.File("result.txt"))

@bot.command()
async def s(ctx: commands.Context):
    if ctx.author.id not in admin_id:
        await ctx.send("このコマンドの使用は制限されています。", ephemeral=True)
        return
    await ctx.send("強制終了します", ephemeral=True)
    await bot.close()

@bot.listen()
async def on_message(message):
    if message.content != "filetest":
        return
    print("c1")
    if message.attachments:
        print("c2")
        if len(message.attachments) == 4 and message.attachments[0].filename == "image.png":
            print("c3")
            await message.reply("**Coo-coo!** suspicious images detected.\nPlease try sending the images in separate messages.\n-# This feature is under testing.")
            await message.delete()
            guild = bot.get_guild(LOG_GUILD_ID)
            channel = guild.get_channel(LOG_CHANNEL_ID)
            await channel.send("Deleted suspicious images.\n" + message.attachments[0].url)
        else:
            print("c4")
            await message.reply(str(len(message.attachments)) +"/"+ message.attachments[0].filename)

@bot.event
async def on_ready():
    await tree.sync()

bot.run(TOKEN)
