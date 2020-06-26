botversion = '1.0 Rabelo build'
prefix = '.'
print(f"""___________________________________________________
        ____       _    _____ _           _
       |  - | __ _| |__|  ___| |    ____ | |  
       |   < / _` | _  |  ___| |___|  _ ||_|
       |_|\_|\__,_|____|_____|_____|____|(_)   

                  {botversion}                  
___________________________________________________""")
import time
import os
import random
import aiohttp
import logging
import asyncio
import discord
from discord.ext import commands
import datetime
from datetime import *

bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')

logging.basicConfig(level='INFO')

async def status_task():
    while True:
        names = [f'{prefix}help all', f'with {len(bot.users)} users', f'on {len(bot.guilds)} servers']
        for name in names:
            await bot.change_presence(activity=discord.Game(name=name))
            await asyncio.sleep(300)

@bot.event
async def on_ready():
    print('Tout est bon !')
    bot.loop.create_task(status_task())

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('❌ Permissions insuffisantes')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.say('❌ Un argument requis est manquant')
    elif isinstance(error, commands.BadArgument):
        await ctx.say('❌ Un argument est incorrect')

@bot.listen()
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.add_reaction('❌')

def is_owner(ctx):
    if ctx.author.id == 720712460834963480:
        return True
    else :
        return False

@bot.group(invoke_without_command=True, aliases=['hlp', 'cmd', 'Help'])
async def help(ctx):
    e = discord.Embed(title='➡️ Catégories de commandes', color=0x33CC33, timestamp=datetime.utcnow())
    e.set_thumbnail(url="https://cdn.discordapp.com/icons/724765475900489828/2c2435cb5df00fe05296f615f88063c0.webp?size=2048")
    e.add_field(name='`fun`', value='Commandes amusantes')
    e.add_field(name='`mod`', value='Commandes de modération')
    e.add_field(name='`music`', value='Commandes pour la musique')
    e.add_field(name='`info`', value='Informations sur MOI :)')
    e.set_footer(text=f'Entrez {prefix}help <nom de la catégorie> pour accéder à une liste de commandes spécifique')
    await ctx.send(embed=e)

@help.command(name="info")
async def help_info(ctx):
    e = discord.Embed(title='📎 Commandes par défaut et d\'info', color=0x00FFC0, timestamp=datetime.utcnow())
    e.set_thumbnail(url="https://cdn.discordapp.com/icons/724765475900489828/2c2435cb5df00fe05296f615f88063c0.webp?size=2048")
    e.add_field(name='`infos`', value='Plus d\'infos sur moi')
    e.add_field(name='`ping`', value='Renvoie "ping"')
    await ctx.send(embed=e)

@help.command(name='all')
async def help_all(ctx):
    c = discord.Embed(description='📚 Toutes les commandes', color=0x003366, timestamp=datetime.utcnow())
    c.set_thumbnail(url="https://cdn.discordapp.com/icons/724765475900489828/2c2435cb5df00fe05296f615f88063c0.webp?size=2048")
    c.add_field(name="`help`, `info`, `ping`, `kick <membre/id>`,`ban <membre/id> <reason>`, `clear <amount of messages>`, `pp <user>`, `roll <number>`", value='Full commands list')
    c.add_field(name="`fun`, `mod`, `music`, `info`", value='Catégories d\'aide')
    await ctx.send(embed=c)

@help.command(name='music')
async def help_utilities(ctx):
    c = discord.Embed(description='⚒️ Utilitaires', color=0x003366, timestamp=datetime.utcnow())
    c.set_thumbnail(url="https://cdn.discordapp.com/icons/724765475900489828/2c2435cb5df00fe05296f615f88063c0.webp?size=2048")
    c.add_field(name='`play <link>`', value='Get the profile picture of some user')
    c.add_field(name='`stop`', value='Lol mdr')
    c.add_field(name='`skip`', value='Lol mdr')
    c.add_field(name='`leave`', value='Lol mdr')
    await ctx.send(embed=c)

@help.command(name="mod")
async def help_moderator(ctx):
    a = discord.Embed(description="🛡️ Modérateur", title='➡️Commands list', color=0xffff00, timestamp=datetime.utcnow()) 
    a.set_thumbnail(url="https://cdn.discordapp.com/icons/724765475900489828/2c2435cb5df00fe05296f615f88063c0.webp?size=2048")
    a.add_field(name='`kick <member/id>`', value='Exclue un membre du serveur')
    a.add_field(name='`ban <membre/id> <raison>`', value='Exclue définitivement un membre du serveur')
    a.add_field(name='`clear <nombre de messages>`', value='Supprime un nombre spécifique de messages')
    await ctx.send(embed=a)

@help.command(name="fun")
async def help_fun(ctx):
    d = discord.Embed(description='🎀 Fun', title='➡️Commands list', color=0xFFA2DD, timestamp=datetime.utcnow())
    d.set_thumbnail(url="https://cdn.discordapp.com/icons/724765475900489828/2c2435cb5df00fe05296f615f88063c0.webp?size=2048")
    d.add_field(name='`Wiki <sujet>`', value="Fait une recherche wikipedia")
    d.add_field(name='`8ball <question>`', value="Pose une question, je te répondrait")
    d.add_field(name='`pp <user>`', value="Affiche la photo de profil de @user")
    await ctx.send(embed=d)

@bot.command(aliases=['info', 'mod', 'all', 'music'])
async def fun(ctx):
    await ctx.send(f"Entrez `{prefix}help <catégorie>` pour afficher toutes les commandes de'une catégorie & leur aide.")

@bot.command(aliases=['add', 'invitelink'])
async def invite(ctx):
    await ctx.send("""Voici mon lien d'invite ♥
<https://discordapp.com/oauth2/authorize?client_id=721449967851536447&scope=bot&permissions=2146958591>""")

@bot.command(aliases=['profilepic', 'ppic', 'avatar'])
async def pp(ctx, usr: discord.User):
    e = discord.Embed(description=f'👤 Photo de profil de {usr.name}', title='➡️Avatar', color=0x5D5DFF, timestamp=datetime.utcnow())
    e.set_image(url=usr.avatar_url)
    await ctx.send(embed=e)

@commands.has_permissions(ban_members=True)
@bot.command()
async def ban(ctx, member: discord.Member, *, reason: str = None):
    try:
        if reason==None:
            await member.ban()
            await ctx.send(f'{member} a bien été banni')
        else:
            await member.ban(reason=reason)
            await ctx.send(f'{member} a bien été banni pour la raison suivante : {reason}')
    except Exception as e:
        print(e.args)
        await ctx.send('❌ Une erreur est survenue')

@commands.has_permissions(kick_members=True)
@bot.command()
async def kick(ctx, *, member: discord.Member):
    try:
        await member.kick()
        await ctx.send(f'{member} a bien été exclu')
    except Exception as e:
        print(e.args)
        await ctx.send('❌ Une erreur est survenue')

@commands.has_permissions(manage_messages=True)
@bot.command()
async def clear(ctx, amount: int):
    amount=amount+1
    try:
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"`{len(deleted)}` messages supprimés avec succès !", delete_after = 5)
    except:
        await ctx.send('❌ Une erreur est survenue')

@bot.command()
async def infos(ctx):
    a = """Créé par Ligrade & Miowski
[M'inviter]( #link )
[Serveur de support](https://discord.gg/zVms5sF)"""
    e = discord.Embed(title = "À propos", description = a, color=0xF4A2FF, timestamp=datetime.utcnow())
    e.set_thumbnail(url="https://cdn.discordapp.com/icons/724765475900489828/2c2435cb5df00fe05296f615f88063c0.webp?size=2048")
    e.set_footer(text=botversion)
    e.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    await ctx.send(embed=e)

@bot.command(aliases=['pingg', 'Ping'])
async def ping(ctx):
    await ctx.send(f'🏓 Pong! `{round(bot.latency * 1000)}`ms')

@bot.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
  responses = [
            "Oui.",
            "Non.",
            "Sans aucun doute.",
            "Biensûr.",
            "Je ne pense pas."]
  await ctx.send(f'**Question :** {question}\n**Réponce :** {random.choice(responses)}')

# @bot.command(aliases=['Wiki', 'wikipedia', 'Wikipedia')
# async def wiki(ctx, wiki):
#     a=f"""**Wikipedia Search**
# 🔀 *More info* https://en.wikipedia.org/wiki/{wiki}"""
#     await ctx.send(a)

@bot.command()
async def ms(ctx):
	await ctx.send("Envoyez le plat que vous voulez cuisiner")

	def checkMessage(message):
		return message.author == ctx.message.author and ctx.message.channel == message.channel

	try:
		recette = await bot.wait_for("message", timeout = 10, check = checkMessage)
	except:
		await ctx.send("Veuillez réitérer la commande.")
		return
	message = await ctx.send(f"La préparation de {recette.content} va commencer. Veuillez valider en réagissant avec ✅. Sinon réagissez avec ❌")
	await message.add_reaction("✅")
	await message.add_reaction("❌")


	def checkEmoji(reaction, user):
		return ctx.message.author == user and message.id == reaction.message.id and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌")

	try:
		reaction, user = await bot.wait_for("reaction_add", timeout = 10, check = checkEmoji)
		if reaction.emoji == "✅":
			await ctx.send("La recette a démarré.")
		else:
			await ctx.send("La recette a bien été annulé.")
	except:
		await ctx.send("La recette a bien été annulé.")

bot.run(bot.run(os.environ['TOKEN']))