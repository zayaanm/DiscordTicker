import discord
from discord.ext import commands
import asyncio
import time
from datetime import datetime, timedelta


bot = commands.Bot(command_prefix="!")
bot.remove_command('help')

#

@bot.event
async def on_ready():
    print ("Ready When Your Are.")
    #print ("Im running " + bot.user.name)
    #print ("With the id " + bot.user.id)
    print ("---------------------------")

@bot.command(passcontext = True)
async def help(ctx):
    embed = discord.Embed(title = "__COMMANDS_:", description = "Use !timer to check the time until the next Event (displayed in [days] [hours] [minutes] [seconds])")
    embed.set_footer(text = "Send a private message to Moderators for personal support")
    await ctx.send(embed = embed)

@bot.command(pass_context = True)
@commands.has_role("")
async def settimer(ctx, day = None, hour = None, mins = None, secs = None):
    '''
    [days] [hours] [mins] [secs]
    '''
    if day or hour or mins or secs != None:
        day = int(day)
        hour = int(hour)
        mins = int(mins)
        secs = int(secs)
        global time
        time = (day * 86400) + (hour * 3600) + (mins * 60) + secs
        while time >= 0:
            time -= 1
            await bot.change_presence(game=discord.Game(name = str(timedelta(seconds= time))[:-3]))
            await asyncio.sleep(1)
        embed = discord.Embed(title = "TIMER STOPPED_", description = "@everyone PREPARE FOR BATTLE")
        await bot.ctx.send(embed = embed)

    else:
        embed = discord.Embed(title = "how to use__:", description = "!settimer [days] [hours] [mins] [secs]")
        await bot.ctx.send(embed = embed)


@bot.command(pass_context = True)
async def timer(ctx):
    embed = discord.Embed(title = "*Event Timer:", description = str(timedelta(seconds= time)))
    await ctx.send(embed = embed)

#error handerling
async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        error = getattr(error, 'original', error)

        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(title = "oops", description = 'This command cannot be found')
            await ctx.author.send(embed = embed)
            await self.send_command_help(ctx)

        if isinstance(error, commands.NoPrivateMessage):
            try:
                embed = discord.Embed(title = "oops", description = 'This command cannot be used in direct messages.')
                await ctx.author.send(embed = embed)
            except discord.Forbidden:
                pass
            return

        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(title = "oops", description = "You do not have permission to use this command.")
            await ctx.author.send(embed = embed)
            return
        #prints errors to the log
        print(f'Ignoring exception in command {ctx.command}:')



bot.run("ODA4NDExMTg2NjM4NzQ5Njk2.YCGJlg.Sy1GGA70HO0N0rIEqOHLrbZ1C2k")
