import discord
from make_bot import make_bot
from discord.ext import commands
import asyncio
import sys

bot = commands.Bot(command_prefix='reg ')
bot.remove_command('help')

@bot.command(name='help')
async def _help(ctx, *args):
    await ctx.send('```reg add <bot mention> <owner mention>``` Need to replace a current token or change owner? Do ```reg add <bot mention> <owner mention> [current token]``` Admin and need to fix a mistake yourself? Do ```reg add <bot mention> <owner mention> --force```')

@bot.command()
async def add(ctx, bot : discord.Member, owner : discord.Member, current_token=None):
    with open('guilds', 'r') as f:
        if ctx.guild.id not in [int(x) for x in f.read().split('\n') if x]:
            raise Exception('Bot only designed for Fusion Discord Bots guild. Want an API for your own server? Contact me @JellyWX on Fusion Bots guild.')

    if not bot.bot:
        raise Exception('First mention must be a bot')

    elif owner.bot:
        raise Exception('Second mention must not be a bot')

    if current_token in ('--force', '-f') and not ctx.author.guild_permissions.administrator:
        ctx.send('Only admins may override')

    else:
        token, error = make_bot(bot.id, owner.id, current_token, current_token in ('--force', '-f'))

        try:
            await ctx.author.send(embed=discord.Embed(description='''
Token:
```{}```
Notes:
```{}```
'''.format(token, error)))

        except discord.errors.Forbidden:
            await ctx.send('Please enable direct messaging in your settings.')

@add.error
async def add_error(ctx, error):
    await ctx.send(error)
    await ctx.send('```reg add <bot mention> <owner mention>``` Need to replace a current token or change owner? Do ```reg add <bot mention> <owner mention> [current token]``` Admin and need to fix a mistake yourself? Do ```reg add <bot mention> <owner mention> --force```')


async def search():
    await bot.wait_until_ready()
    print('Ready!')
    print(bot.user.id)

    channel = bot.get_channel(443439662959296523)

    roles = {
        'soundfx' : 443426944210698250,
        'membercount' : 443427010124054530,
        'loxantibadword' : 443426980210409472,
        'applicationbot' : 443438462499291146,
        'remindme' : None
    }

    while not bot.is_closed():
        message = await channel.history(limit=1).next()

        for r in message.reactions:

            if isinstance(r.emoji, str) or (r.emoji.name not in roles.keys() or r.emoji.name == 'remindme'):
                users = await r.users().flatten()
                for user in users:
                    await message.remove_reaction(r, user)

                continue

            role = [rol for rol in channel.guild.roles if rol.id == roles[r.emoji.name]][0]

            users = await r.users().flatten()

            for member in channel.guild.members:
                if member in users and role not in member.roles:
                    await member.add_roles(role)
                elif member not in users and role in member.roles:
                    await member.remove_roles(role)
                else:
                    continue


bot.loop.create_task(search())

with open('token', 'r') as f:
    try:
        bot.run(f.read().strip())
    except Exception as e:
        print('Error detected. Restarting in 15 seconds.')
        print(sys.exc_info()[0])
        time.sleep(15)

        os.execl(sys.executable, sys.executable, *sys.argv)
