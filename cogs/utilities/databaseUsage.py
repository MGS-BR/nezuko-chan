import disnake
import json

from pymongo import MongoClient
from disnake.ext import commands

with open("config.json") as w:
    infos = json.load(w)
    connection_url = infos["mongo"]

cluster = MongoClient(connection_url)
cluster_guilds = cluster["discord"]["guilds"]
cluster_users = cluster["discord"]["users"]
cluster_guilds_xp = cluster["discord"]["guilds_xp"]

class database():

    async def guild(ctx, guild = None):

        if not guild:

            guild = ctx.guild

        guild_db = cluster_guilds.find_one(
            {"id": guild.id}
        )

        if not guild_db:

            cluster_guilds.insert_one(
                {
                    "id": guild.id,
                    "language": "english",
                    "alerts": {
                        "command_usage": {
                            "stats": False,
                            "message": "It is not possible to use commands in this chat"
                        }
                    },
                    "logs": {
                        "message_deleted": False,
                        "message_edited": False,
                        "user_join": {
                            "stats": False,
                            "message": "{user} joined the server"
                        },
                        "user_leave": {
                            "stats": False,
                            "message": "{user} left the server"
                        }
                    },
                    "mute": {
                        "role": 0,
                        "discord_mute": False
                    },
                    "ch_command": [],
                    "ch_xp": []
                }
            )

        guild_db = cluster_guilds.find_one(
            {"id": guild.id}
        )

        return guild_db

    async def user(ctx, user = None):

        if not user:

            user = ctx.author

        user_db = cluster_users.find_one(
            {"id": user.id}
        )

        if not user_db:

            cluster_users.insert_one(
                {
                    "id": user.id,
                    "marry": {
                        "stats": False,
                        "user": None
                    },
                    "status": "Use '/profilechange description' to change your profile description.",
                    "reps": {},
                    "reps_send": {},
                    "xp": 10,
                    "coins": 0,
                    "transactions": {},
                    "xp_boost": 0,
                    "wallpaper": "bg_profile_1.png",
                    "wallpapers": [],
                    "ban": False,
                    "reps_cooldown": 0,
                    "daily_cooldown": 0
                }
            )

        user_db = cluster_users.find_one(
            {"id": user.id}
        )

        return user_db

    async def level_guild(ctx, guild = None, user = None):

        if not guild:

            guild = ctx.guild

        if not user:

            user = ctx.author

        guild_xp_db = cluster_guilds_xp.find_one(
            {
                "guild": guild.id,
                "user": user.id
            }
        )

        if not guild_xp_db:

            cluster_guilds_xp.insert_one(
                {
                    "guild": guild.id,
                    "user": user.id,
                    "xp": 10
                }
            )

        guild_xp_db = cluster_guilds_xp.find_one(
            {
                "guild": guild.id,
                "user": user.id
            }
        )

        return guild_xp_db

