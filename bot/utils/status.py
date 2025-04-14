import discord
import asyncio

custom_statuses = [
    {"type": "listening", "message": "-help"},
    {"type": "game", "message": "-ask to talk with AI"},
    {"type": "watching", "message": "{members} members"},
]

async def update_status(bot):
    while True:
        for status in custom_statuses:
            message = status["message"].format(
                prefix=bot.command_prefix,
                guilds=len(bot.guilds),
                users=sum(g.member_count for g in bot.guilds),
                members=sum(g.member_count for g in bot.guilds)  # for watching members
            )
            if status["type"] == "game" or status["type"] == "playing":
                activity = discord.Game(name=message)
            elif status["type"] == "watching":
                activity = discord.Activity(type=discord.ActivityType.watching, name=message)
            elif status["type"] == "listening":
                activity = discord.Activity(type=discord.ActivityType.listening, name=message)
            else:
                continue
            await bot.change_presence(activity=activity)
            await asyncio.sleep(20)
