#utility.py
from discord.ext import commands
import discord
import time
import asyncio
from datetime import datetime, timedelta

# Store the start time for uptime tracking
start_time = time.time()

def setup_utility(bot):
    # Add Custom Emoji
    @bot.hybrid_command(name="addemoji")
    async def addemoji(ctx: commands.Context, name: str, url: str):
        try:
            emoji = await ctx.guild.create_custom_emoji(name=name, image=requests.get(url).content)
            await ctx.send(f"Added new emoji: {emoji}")
        except Exception as e:
            await ctx.send(f"Error adding emoji: {e}")

    # Assign a Role to a User
    @bot.hybrid_command(name="addrole")
    async def addrole(ctx: commands.Context, member: discord.Member, role: discord.Role):
        await member.add_roles(role)
        await ctx.send(f"Assigned role {role.name} to {member.name}")

    # Set AFK Status
    @bot.hybrid_command(name="afk")
    async def afk(ctx: commands.Context, *, reason: str = "No reason provided"):
        # Set the AFK status
        await ctx.author.edit(nick=f"[AFK] {ctx.author.name}")
        await ctx.send(f"{ctx.author.mention} is now AFK: {reason}")

    # Show User Avatar
    @bot.hybrid_command(name="avatar")
    async def avatar(ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"{member.name}'s Avatar", color=0x4682B4)
        embed.set_image(url=member.avatar.url)
        await ctx.send(embed=embed)

    # View Bot Info
    @bot.hybrid_command(name="botinfo")
    async def botinfo(ctx: commands.Context):
        uptime = int(time.time() - start_time)
        hours, remainder = divmod(uptime, 3600)
        minutes, seconds = divmod(remainder, 60)

        embed = discord.Embed(
            title="Bot Info",
            description="Detailed stats about the bot.",
            color=0x4682B4
        )
        embed.add_field(name="Name", value=bot.user.name, inline=False)
        embed.add_field(name="ID", value=str(bot.user.id), inline=False)
        embed.add_field(name="Uptime", value=f"{hours}h {minutes}m {seconds}s", inline=False)
        embed.add_field(name="Servers", value=len(bot.guilds), inline=False)
        embed.add_field(name="Users", value=sum(guild.member_count for guild in bot.guilds), inline=False)
        embed.add_field(name="Latency", value=f"{round(bot.latency * 1000)}ms", inline=False)
        embed.add_field(name="Creator", value="Ayanokouji", inline=False)
        embed.set_thumbnail(url=bot.user.avatar.url)
        await ctx.send(embed=embed)

    # View Channel Info
    @bot.hybrid_command(name="channelinfo")
    async def channelinfo(ctx: commands.Context, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        embed = discord.Embed(
            title="Channel Info",
            description=f"Details about {channel.name}",
            color=0x4682B4
        )
        embed.add_field(name="ID", value=str(channel.id), inline=False)
        embed.add_field(name="Type", value=str(channel.type).capitalize(), inline=False)
        embed.add_field(name="Created At", value=channel.created_at.strftime("%Y-%m-%d %H:%M UTC"), inline=False)
        embed.add_field(name="Position", value=channel.position, inline=False)
        embed.add_field(name="Category", value=channel.category.name if channel.category else "None", inline=False)
        embed.add_field(name="NSFW", value="Yes" if channel.is_nsfw() else "No", inline=False)
        await ctx.send(embed=embed)

    # Clear AFK Status
    @bot.hybrid_command(name="clearafk")
    async def clearafk(ctx: commands.Context):
        await ctx.author.edit(nick=ctx.author.name)
        await ctx.send(f"{ctx.author.mention} is no longer AFK.")

    # Create a New Role
    @bot.hybrid_command(name="createrole")
    async def createrole(ctx: commands.Context, name: str, color: str = "0x000000"):
        try:
            color = discord.Color(int(color, 16))
            role = await ctx.guild.create_role(name=name, color=color)
            await ctx.send(f"Created new role: {role.name}")
        except Exception as e:
            await ctx.send(f"Error creating role: {e}")

    # Remove Custom Emoji
    @bot.hybrid_command(name="deleteemoji")
    async def deleteemoji(ctx: commands.Context, emoji: discord.Emoji):
        await emoji.delete()
        await ctx.send(f"Deleted emoji: {emoji.name}")

    # Delete a Role
    @bot.hybrid_command(name="deleterole")
    async def deleterole(ctx: commands.Context, role: discord.Role):
        await role.delete()
        await ctx.send(f"Deleted role: {role.name}")

    # Edit Nickname
    @bot.hybrid_command(name="editnickname")
    async def editnickname(ctx: commands.Context, member: discord.Member, nickname: str):
        await member.edit(nick=nickname)
        await ctx.send(f"Changed {member.name}'s nickname to {nickname}")

    # List Server Emojis
    @bot.hybrid_command(name="emotes")
    async def emotes(ctx: commands.Context):
        emojis = [str(emoji) for emoji in ctx.guild.emojis]
        await ctx.send("Emojis in this server:\n" + "\n".join(emojis))

    # List Server Roles
    @bot.hybrid_command(name="listroles")
    async def listroles(ctx: commands.Context):
        roles = [role.name for role in ctx.guild.roles]
        await ctx.send("Roles in this server:\n" + "\n".join(roles))

    # Ping the Bot
    @bot.hybrid_command(name="ping")
    async def ping(ctx: commands.Context):
        await ctx.send(f"Pong! Latency is {round(bot.latency * 1000)}ms")

    # Remove a Role from a User
    @bot.hybrid_command(name="removerole")
    async def removerole(ctx: commands.Context, member: discord.Member, role: discord.Role):
        await member.remove_roles(role)
        await ctx.send(f"Removed role {role.name} from {member.name}")

    # View Role Info
    @bot.hybrid_command(name="roleinfo")
    async def roleinfo(ctx: commands.Context, role: discord.Role = None):
        if not role:
            await ctx.send(embed=discord.Embed(title="Error", description="Specify a role to get information.", color=0xCD5C5C))
            return
        embed = discord.Embed(
            title="Role Info",
            description=f"Details about the role: {role.name}",
            color=role.color
        )
        embed.add_field(name="ID", value=str(role.id), inline=False)
        embed.add_field(name="Created At", value=role.created_at.strftime("%Y-%m-%d %H:%M UTC"), inline=False)
        embed.add_field(name="Members", value=len(role.members), inline=False)
        embed.add_field(name="Permissions", value=", ".join([perm[0].replace("_", " ").title() for perm in role.permissions if perm[1]]), inline=False)
        await ctx.send(embed=embed)

    # Show Server Icon
    @bot.hybrid_command(name="servericon")
    async def servericon(ctx: commands.Context):
        embed = discord.Embed(title="Server Icon", color=0x4682B4)
        embed.set_image(url=ctx.guild.icon.url)
        await ctx.send(embed=embed)

    # View Server Info
    @bot.hybrid_command(name="serverinfo")
    async def serverinfo(ctx: commands.Context):
        guild = ctx.guild
        embed = discord.Embed(
            title="Server Info",
            description=f"Information about the server **{guild.name}**.",
            color=0x4682B4
        )
        embed.add_field(name="ID", value=str(guild.id), inline=False)
        embed.add_field(name="Owner", value=guild.owner.name, inline=False)
        embed.add_field(name="Region", value=str(guild.region), inline=False)
        embed.add_field(name="Member Count", value=guild.member_count, inline=False)
        embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M UTC"), inline=False)
        embed.add_field(name="Text Channels", value=len(guild.text_channels), inline=False)
        embed.add_field(name="Voice Channels", value=len(guild.voice_channels), inline=False)
        embed.add_field(name="Roles", value=len(guild.roles), inline=False)
        await ctx.send(embed=embed)

    # View User Info
    @bot.hybrid_command(name="userinfo")
    async def userinfo(ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(
            title="User Info",
            description=f"Information about the user {member.name}#{member.discriminator}",
            color=0x4682B4
        )
        embed.add_field(name="Username", value=f"{member.name}#{member.discriminator}", inline=False)
        embed.add_field(name="ID", value=str(member.id), inline=False)
        embed.add_field(name="Nickname", value=member.nick or "None", inline=False)
        embed.add_field(name="Status", value=str(member.status).capitalize(), inline=False)
        embed.add_field(name="Created At", value=member.created_at.strftime("%Y-%m-%d %H:%M UTC"), inline=False)
        embed.add_field(name="Joined At", value=member.joined_at.strftime("%Y-%m-%d %H:%M UTC"), inline=False)
        embed.add_field(name="Roles", value=", ".join([role.name for role in member.roles]), inline=False)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        await ctx.send(embed=embed)

    # Remind Me (Ping in Same Channel)
    @bot.hybrid_command(name="remindme")
    async def remindme(ctx: commands.Context, time_str: str, *, reminder: str):
        time_match = re.match(r"(\d+)([smhd])", time_str)
        if not time_match:
            await ctx.send("Please use a valid time format. Example: `10m`, `2h`, `1d`")
            return

        time_value, time_unit = time_match.groups()
        time_value = int(time_value)

        time_map = {
            's': 'seconds',
            'm': 'minutes',
            'h': 'hours',
            'd': 'days'
        }

        delta_kwargs = {time_map[time_unit]: time_value}
        remind_time = datetime.now() + timedelta(**delta_kwargs)

        await ctx.send(f"Reminder set for {remind_time.strftime('%Y-%m-%d %H:%M:%S')}")

        await asyncio.sleep(time_value * {"s": 1, "m": 60, "h": 3600, "d": 86400}[time_unit])
        await ctx.send(f"{ctx.author.mention}, Reminder: {reminder}")

    # Set a Timer
    @bot.hybrid_command(name="timer")
    async def timer(ctx: commands.Context, seconds: int):
        await ctx.send(f"Timer set for {seconds} seconds.")
        await asyncio.sleep(seconds)
        await ctx.send(f"{ctx.author.mention}, Time's up!")

    # Uptime Command
    @bot.hybrid_command(name="uptime")
    async def uptime(ctx: commands.Context):
        uptime_seconds = int(time.time() - start_time)
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.send(f"Bot uptime: {hours}h {minutes}m {seconds}s")
