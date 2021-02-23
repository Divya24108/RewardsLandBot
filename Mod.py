import discord
from discord.ext import commands
import asyncio
import typing

class Mod(commands.Cog):
  
  def __init__(self, client):
    self.client = client
  
  @commands.command()
  @commands.guild_only()
  @commands.has_permissions(kick_members = True)
  async def kick(self, ctx, member: discord.Member,*, reason = None):
    await member.kick(reason = reason)
    embed = discord.Embed(title = "Kick Successful", description = f"{member} was successfully yeeted out of the server", color = discord.Color.from_rgb(255,0,255))
    embed.set_image(url = "https://media.tenor.com/images/27f16871c55a3376fa4bfdd76ac2ab5c/tenor.gif")
    embed.set_footer(text = f"Action taken by {ctx.author.display_name}")
    await ctx.send(embed = embed)
  
  @commands.command()
  @commands.guild_only()
  @commands.has_permissions(ban_members = True)
  async def ban(self, ctx, member: discord.Member = None, *, reason = None):
    if member == None:
      embed = discord.Embed(title = "Ban Hammer ready", description = "Who should I yeet?", color = discord.Color.from_rgb(255,0,255))
      embed.set_image(url = "https://media.tenor.com/images/7895bffb008b21f3e347ddbd4297697a/tenor.gif")
      embed.set_footer(icon_url = "https://media.discordapp.net/attachments/800939035627225091/805119292223258685/unknown.png")
      await ctx.send(embed = embed)
      return
    await member.ban(reason = reason)
    embed = discord.Embed(title = "Ban Successful", description = f"{member} was ban hammered", color = discord.Color.from_rgb(255,0,255))
    embed.set_footer(text = f"Action taken by {ctx.author.display_name}")
    embed.set_image(url = "https://media.tenor.com/images/7895bffb008b21f3e347ddbd4297697a/tenor.gif")
    await ctx.send(embed = embed)

  @commands.command()
  @commands.guild_only()
  @commands.has_permissions(manage_channels = True)
  async def nuke(self, ctx):
    positive = ["yes", "Yes"]
    pos = ctx.channel.position
    def check(message):
      return message.author == ctx.author and message.channel == ctx.channel
    await ctx.send(f" {ctx.author.mention}, You sure about that? Reply with a 'yes' or 'no'")
    try:
      confirm = await self.client.wait_for('message', check = check, timeout = 30)
    except asyncio.TimeoutError:
      await ctx.send("Okay no nuking today")
    if confirm.content in positive:
      new_channel = await ctx.channel.clone()
      await ctx.channel.delete()
      await new_channel.edit(position = pos)
      await new_channel.send("Nuked this channel!")
      return
  

  @commands.command()
  @commands.has_permissions(kick_members = True)
  async def slowmode(self, ctx, channel:typing.Optional[discord.TextChannel] = None, sec:int = 0):
    if channel == None:
      channel = ctx.channel
    await channel.edit(slowmode_delay = sec)
    await ctx.send(f"Slowmode in {channel.mention} has been set to {sec} seconds")

  @commands.command()
  @commands.guild_only()
  @commands.has_permissions(manage_messages = True)
  async def purge(self, ctx,target: typing.Optional[discord.Member] = None, amount: int = 10):
      if not target:
        deleted = await ctx.channel.purge(limit = amount+1)
        await ctx.send(f"Deleted **{len(deleted)}** messages", delete_after = 5)
      else:
        def check(message):
          return message.author == target
        deleted = await ctx.channel.purge(limit = amount, check = check)
        await ctx.send(f"Deleted **{len(deleted)}** messages from {target.name}", delete_after = 5)

      

  @commands.command()
  @commands.guild_only()
  @commands.has_permissions(kick_members = True)
  async def mute(self, ctx, member:discord.Member):
    muted_role = ctx.guild.get_role(787979560200962078)
    await member.add_roles(muted_role)
    embed = discord.Embed(title = "Mute Successful", description = f"Added the role {muted_role.mention} to {member.mention}", colour = discord.Colour.from_rgb(255,0,255))
    embed.set_footer(icon_url = "https://media.discordapp.net/attachments/800939035627225091/805119292223258685/unknown.png")
    await ctx.send(embed = embed)

  @commands.command()
  @commands.guild_only()
  @commands.has_permissions(kick_members = True)
  async def unmute(self, ctx, member:discord.Member):
      muted_role = ctx.guild.get_role(787979560200962078)
      if muted_role in member.roles:
        await member.remove_roles(muted_role)
        embed = discord.Embed(title = "Unmute Successful", description = f"Removed the role {muted_role.mention} from {member.mention}", colour = discord.Colour.from_rgb(255,0,255))
        await ctx.send(embed = embed)
      else:
        await ctx.send("That member is not muted!")
  
  @commands.command()
  @commands.guild_only()
  @commands.has_permissions(manage_channels = True)
  async def lock(self, ctx, channel: discord.TextChannel = None):
    if channel == None:
      channel = ctx.channel
    await channel.set_permissions(ctx.guild.default_role,read_messages=True, send_messages=False)
    embed = discord.Embed(title = "Locked the channel", description = f"{channel.mention} is locked down", colour = discord.Colour.from_rgb(255,0,255))
    embed.set_footer(icon_url = "https://media.discordapp.net/attachments/800939035627225091/805119292223258685/unknown.png")
    await ctx.send(embed = embed)
    if channel != ctx.channel:
      await channel.send(embed = embed)
  
  @commands.command()
  @commands.guild_only()
  @commands.has_permissions(manage_channels = True)
  async def unlock(self, ctx, channel: discord.TextChannel = None):
    if channel == None:
      channel = ctx.channel
    await channel.set_permissions(ctx.guild.default_role,read_messages=True, send_messages=True)
    embed = discord.Embed(title = "Unlocked the channel", description = f"{channel.mention} is unlocked", colour = discord.Colour.from_rgb(255,0,255))
    await ctx.send(embed = embed)
    if channel != ctx.channel:
      await channel.send(embed = embed)

  @commands.command()
  @commands.has_permissions(administrator = True)
  async def lockdown(self, ctx,*,reason=None):
    for channel in ctx.guild.text_channels:
      await channel.set_permissions(ctx.guild.default_role, send_messages = False)
      embed = discord.Embed(title = "Server Locked Down", description = reason, color = discord.Color.from_rgb(255,0,255))
      embed.set_footer(text = f"Action by {ctx.author.name}")
      await channel.send(embed = embed)

  



def setup(client):
  client.add_cog(Mod(client))