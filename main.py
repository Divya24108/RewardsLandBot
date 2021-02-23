import discord
from discord.ext import commands
import datetime
from replit import db
import asyncio
import keep_alive
import os

client = commands.Bot(command_prefix = "$", intents = discord.Intents.all())



@client.event
async def on_ready():
  client.load_extension("Mod")
  print("Ready")

@client.command()
async def claimed(ctx, member:discord.Member):
  await ctx.message.delete()
  await ctx.send(f"╭ <a:WhiteCrown:813274897546608640> GG [{member.mention}] won! ask him if legit or not. \n <:line:807185741737492520><:line:807185741737492520><:line:807185741737492520><:line:807185741737492520><:line:807185741737492520><:line:807185741737492520><:line:807185741737492520><:line:807185741737492520><:line:807185741737492520><:line:807185741737492520><:line:807185741737492520><:line:807185741737492520><:line:807185741737492520><:line:807185741737492520><:line:807185741737492520><:line:807185741737492520> \n <a:EG_aExclamationBlue:807501880589549578> **TIP**: \n  <:GG_bluedot:813274989997850654> Be fast coming to giveaway channels Putting as above all other servers will help you see the pings easily! \n  <:GG_bluedot:813274989997850654> Make sure to #:ribbon:・support-us and get +3s claim time! \n <:GG_bluedot:813274989997850654>  Boost us for extra claim time and less Cooldown  \n<:line:807185741737492520><:line:807185741737492520><:line:807185741737492520><:line:807185741737492520><:line:807185741737492520><:line:807185741737492520><:line:807185741737492520><:line:807185741737492520><:line:807185741737492520><:line:807185741737492520><:line:807185741737492520><:line:807185741737492520><:line:807185741737492520><:line:807185741737492520><:line:807185741737492520><:line:807185741737492520> \n ╰ <a:WhiteCrown:813274897546608640> Stay in ***__Rewards Land__*** for more!")



@client.command()
async def userinfo(ctx, member:discord.Member = None):
  try:
    async def strfdelta(tdelta, fmt):
      d = {"days": tdelta.days}
      d["hours"], rem = divmod(tdelta.seconds, 3600)
      d["minutes"], d["seconds"] = divmod(rem, 60)
      return fmt.format(**d)
    
    if member == None:
      member = ctx.author
    roles = [role for role in member.roles]
    today = datetime.datetime.now()
    joined = member.joined_at
    c = today - joined
    o = await strfdelta(c, "{days} Days {hours} Hours, {minutes} Minutes and {seconds} Seconds ago!")
    created = member.created_at
    d = today - created
    e = await strfdelta(d, "{days} Days {hours} Hours, {minutes} Minutes and {seconds} Seconds ago!")
    embed = discord.Embed(title = member.name, description = f"Information on {member.mention}", color = discord.Color.from_rgb(255,0,255))
    embed.add_field(name="Created Account On", value=member.created_at.strftime(f"%a, %#d %B %Y, %I:%M %p UTC ({e})"), inline = False)
    embed.add_field(name="Joined Server On", value=member.joined_at.strftime(f"%a, %#d %B %Y, %I:%M %p UTC ({o})"), inline = False)
    embed.add_field(name="Roles", value="".join([role.mention for role in roles]), inline = False)
    embed.add_field(name="Highest Role", value=member.top_role.mention, inline = False)
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url = "https://media.discordapp.net/attachments/800939035627225091/805119292223258685/unknown.png")
    await ctx.send(embed = embed)
  except Exception as e:
    await ctx.send(e)



  
@client.command()
async def server(ctx):
  guild = ctx.guild
  embed = discord.Embed(title = ctx.guild.name, decription = f"Information on {ctx.guild}", color = discord.Colour.from_rgb(255,0,255))
  embed.add_field(name = "Members", value = guild.member_count, inline = False)
  embed.add_field(name = "Channels", value = f"All channels: {len(guild.channels)} \n Text Chanels: {len(guild.text_channels)} \n Voice Channels: {len(guild.voice_channels)}", inline = False)
  embed.add_field(name = "ID", value = guild.id, inline = False)
  embed.add_field(name = "Owner", value = guild.owner, inline = False)
  embed.add_field(name = "Roles", value = len(ctx.guild.roles), inline = False)
  embed.set_thumbnail(url = ctx.guild.icon_url)
  await ctx.send(embed = embed)

@client.command()
async def snowflake(ctx, win_id:int, dm_id:int ):
  win_time = discord.utils.snowflake_time(win_id)
  dm_time = discord.utils.snowflake_time(dm_id)
  diff = dm_time - win_time
  seconds = diff.total_seconds()
  await ctx.send(f"Difference between the two message ID's is **{seconds}** seconds!")

@client.command()
@commands.has_permissions(administrator = True)
async def nukeclaim(ctx, user:discord.Member):
  try:
    pos = ctx.channel.position
    def check(message):
      return message.author == ctx.author and message.channel == ctx.channel
    await ctx.send(f" {ctx.author.mention}, You sure about that? Reply with a 'yes' or 'no'")
    try:
      confirm = await client.wait_for('message', check = check, timeout = 30)
    except asyncio.TimeoutError:
      await ctx.send("Okay no nuking today")
    if confirm.content == "yes":
      new_channel = await ctx.channel.clone()
      await ctx.channel.delete()
      await new_channel.edit(position = pos)
      await new_channel.send(f"╭ <a:WhiteCrown:794769961889169420> GG [{user.mention}] won! ask him if legit or not.")
  except:
    pass


@client.event
async def on_command_error(ctx,error):
  if hasattr(ctx.command, 'on_error'):
    return

  cog = ctx.cog
  if cog:
    if cog._get_overridden_method(cog.cog_command_error) is not None:
      return

  ignored = (commands.CommandNotFound, )
  error = getattr(error, 'original', error)

  if isinstance(error, ignored):
    return
  
  elif isinstance(error, commands.MissingAnyRole):
    return
  elif isinstance(error, commands.MissingPermissions):
    return
  elif isinstance(error, commands.CommandNotFound):
    await ctx.send("<:mostusedemoji:807851770927382529>")
  else:
    await ctx.send(error)

@client.command()
async def greet(ctx, channel:discord.TextChannel, *, msg):
  db["greet_channel"] = channel.id
  db["greet_msg"] = msg
  await ctx.send(f"OK sample msg in {channel.mention} is: [member.mention],{msg}")
  
@client.command()
async def greetdel(ctx):
  del db["greet_channel"]
  del db["greet_msg"]
  await ctx.send("Deleted")

@client.command()
async def delafter(ctx, amt:int):
  db["greet_delete_after"] = amt
  await ctx.send(f"Okay Greet messages will now be deleted in {amt} seconds")

@client.event
async def on_member_join(member):
  try:
    channel = client.get_channel(db["greet_channel"])
    await channel.send(f"{member.mention}," + db["greet_msg"], delete_after = db["greet_delete_after"])
  except KeyError:
    pass

@client.command()
async def simjoin(ctx,member:discord.Member):
  try:
    channel = client.get_channel(db["greet_channel"])
    await channel.send(f"{member.mention}," + db["greet_msg"], delete_after = db["greet_delete_after"])
  except KeyError:
    pass

keep_alive.keep_alive()

client.run(os.getenv("TOKEN"))
