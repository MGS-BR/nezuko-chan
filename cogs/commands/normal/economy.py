import disnake
import datetime
import calendar
import pytz
import random
import json

from disnake.ext import commands
from pymongo import MongoClient

from cogs.utilities.commandChannel import commandChannel
from cogs.utilities.databaseUsage import database

with open("config.json") as w:
    infos = json.load(w)
    connection_url = infos["mongo"]

cluster = MongoClient(connection_url)
cluster_users = cluster["discord"]["users"]

def human_format(num):
    num = float("{:.3g}".format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return "{}{}".format("{:f}".format(num).rstrip("0").rstrip("."), ["", "K", "M", "B", "T"][magnitude])

class Economy(commands.Cog):
    """Sistema de economia"""

    def __init__(self, client):
        self.client = client

    @commands.slash_command()
    async def coins(self, ctx):

        pass

    @commands.slash_command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def daily(self, ctx):

        """
        [Economy] Get your daily coins
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        user_db = await database.user(ctx)

        date = datetime.datetime.today().astimezone(pytz.timezone('America/Sao_Paulo'))

        next_date = date + datetime.timedelta(days=1)

        remove_hours, remove_minutes  = int(next_date.strftime("%H"))*3600, int(next_date.strftime("%M"))*60

        actual_timestamp = calendar.timegm(date.utctimetuple())

        new_timestamp = calendar.timegm(next_date.utctimetuple()) - (remove_hours+remove_minutes+int(next_date.strftime("%S")))

        if user_db["daily_cooldown"] > actual_timestamp:

            delta = datetime.datetime.fromtimestamp(user_db["daily_cooldown"]) - datetime.datetime.fromtimestamp(actual_timestamp)

            hours, remainder = divmod(int(delta.total_seconds()), 3600)

            minutes, seconds = divmod(remainder, 60)

            days, hours = divmod(hours, 24)

            if days:
                time_format = "**{d}d**, **{h}h**, **{m}m**, e **{s}s**."
            else:
                time_format = "**{h}h**, **{m}m**, e **{s}s**"

            daily_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)

            if guild_db["language"] == "portugues":

                return await ctx.send(
                    embed = disnake.Embed(
                        description = f"<:x_:956703878395625472> Você já pegou o seu daily hoje!\nVocê vai poder pegar o seu daily novamente em: {daily_stamp}",
                        color = disnake.Color.red()
                    )
                )

            else:

                return await ctx.send(
                    embed = disnake.Embed(
                        description = f"<:x_:956703878395625472> You already got your daily today!\nYou will be able to get your daily again at: {daily_stamp}",
                        color = disnake.Color.red()
                    )
                )

        else:

            earn_coins = random.randint(1000, 3000)

            cluster_users.update_one(
                {
                    "id": ctx.author.id
                },
                {
                    "$set": {"daily_cooldown": new_timestamp}
                }
            )

            cluster_users.update_one(
                {
                    "id": ctx.author.id
                },
                {
                    "$inc": {"coins": earn_coins}
                }
            )

            if guild_db["language"] == "portugues":

                await ctx.send(
                    embed = disnake.Embed(
                        description = f"🪙 Hoje você ganhou **{human_format(earn_coins)} coins**!",
                        color = disnake.Color.gold()
                    )
                )

            else:

                await ctx.send(
                    embed = disnake.Embed(
                        description = f"🪙 Today you won **{human_format(earn_coins)} coins**!",
                        color = disnake.Color.gold()
                    )
                )       

    @coins.sub_command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def leaderboard(self, ctx):

        """
        [Economy] Coins leadboard
        """   

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        user_db = await database.user(ctx)

        global_coins = cluster_users.find().sort("coins", -1)

        num = 1

        user_rank = 1

        embed = disnake.Embed(
            title = "💰 Coins leaderboard",
            color = disnake.Color.gold(),
            timestamp = datetime.datetime.utcnow()
        )

        for user_rk in global_coins:

            if num == 1:
                position = f"🥇 {num}" # primeiro lugar
            elif num == 2:
                position = f"🥈 {num}" # segundo lugar
            elif num == 3:
                position = f"🥉 {num}" # terceiro lugar
            else:
                position = num

            user_rk_object = self.client.get_user(user_rk["id"])
            user_rk_coin = user_rk["coins"]

            embed.add_field(
                name = f"{position}º {user_rk_object.name}",
                value = f"Coins: {human_format(user_rk_coin)}",
                inline = False
            )

            num += 1

            if num == 1:

                break

        for user_rk in global_coins:

            if user_rk["id"] == ctx.author.id:

                break

            else:

                user_rank += 1

        if guild_db["language"] == "portugues":

            embed.set_footer(text=f"Seu ranking: {user_rank}º \u200b")

        else:

            embed.set_footer(text=f"Your ranking: {user_rank}º \u200b")

        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/326/326887.png")
        await ctx.send(embed=embed)

    @commands.slash_command(
        options = [
            disnake.Option(
                name = "user",
                description = "user you want to see the balance",
                type = disnake.OptionType.user,
                required = False
            )
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def balance(self, ctx, user: disnake.User = None):

        """
        [Economy] See your balance or someone else's
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        text = ""

        if not user:

            user = ctx.author

            all_xp = cluster_users.find().sort("coins", -1)

            user_rank = 1

            for user_rk in all_xp:

                if user_rk["id"] == ctx.author.id:

                    break

                else:

                    user_rank += 1

            if guild_db["language"] == "portugues":

                text = f" Você está na posicão **#{user_rank}** do ranking!"

            else:

                text = f" You are in position **#{user_rank}** of the ranking!"

        user_db = await database.user(ctx, user)

        user_coins = human_format(user_db["coins"])

        if guild_db["language"] == "portugues":

            await ctx.send(
                embed = disnake.Embed(
                    description = f"🪙 {user.mention} tem **{user_coins} coins**!{text}",
                    color = disnake.Color.gold()
                )
            )

        else:

            await ctx.send(
                embed = disnake.Embed(
                    description = f"🪙 {user.mention} have **{user_coins} coins**!{text}",
                    color = disnake.Color.gold()
                )
            )            

def setup(client):
    client.add_cog(Economy(client))