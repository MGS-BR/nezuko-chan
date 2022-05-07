import disnake
import json
import datetime
import calendar

from pymongo import MongoClient
from disnake.ext import commands

from cogs.utilities.commandChannel import commandChannel
from cogs.utilities.databaseUsage import database

with open("config.json") as w:
    infos = json.load(w)
    connection_url = infos["mongo"]

cluster = MongoClient(connection_url)
cluster_mute_time_db = cluster["discord"]["guilds_mutes"]

class Mute(commands.Cog):
    """Comandos de mute"""

    def __init__(self, client):
        self.client = client

def setup(client):
    client.add_cog(Mute(client))