import discord
from discord import Embed
from discord.ext import commands
from discord.utils import get
import random
import asyncio
import config
from discord import Activity, ActivityType
import datetime
import locale
import json
import sqlite3
from Cybernator import Paginator
import os

#=====================================================
#					Setings
#=====================================================

locale.setlocale(locale.LC_TIME, 'ru')
bot = commands.Bot(command_prefix = config.PREFIX)
bot.remove_command('help')

connection = sqlite3.connect('mysqldata.db')
cursor = connection.cursor()

#=====================================================
#					Functions
#=====================================================

def randcol():
	return random.randint(0, 0xFFFFFF)

def is_not_onotoliy(ctx):
	return ctx.author.id != 469018523583250433

#=====================================================
#					Litst
#=====================================================

hello_words = ['Hello', 'Hi', 'Привет', 'Hola', 'Hei','Nǐ hǎo',
				'Kon\'nichiwa', 'Hallo', 'Olá', 'Bonjour']
compliment_words = ['Have a nice day!',
					'You look great!',
					'How do you like the weather today?',
					'Good luck to you!',
					'Have a good mood',
					'You are lucky today']
smile_list = ['😀', '😃', '😄', '😁', '😊', '😇', '😉', '😍', '😎', '🤩', '🤗', '🙃', '😘', '😏']

#=====================================================
#					Event
#=====================================================

#Bor ready
@bot.event
async def on_ready():
	print(f'{bot.user.name} is ready!')
	await bot.change_presence(activity = discord.Streaming(type = discord.ActivityType.streaming,
		name = 'RenaissanceBot eSports', url = 'https://www.twitch.tv/renaissance_esports%27'))

	cursor.execute('''CREATE TABLE IF NOT EXISTS users(
	name TEXT,
	id INT,
	warn INT,
	repq INT
	)''')
	
	for guild in bot.guilds:
		for member in guild.members:
			if cursor.execute(f'SELECT id FROM users WHERE id = {member.id}').fetchone() is None:
				cursor.execute(f'INSERT INTO users VALUES ("{member}", {member.id}, 0, False)')
			else:
				pass
	connection.commit()

#New member on server
@bot.event
async def on_member_join(member):
	channel_log = bot.get_channel(730455033346260992)
	guild = bot.get_guild(730187674043809894)
	role = get(guild.roles, id = 730189588781334540)
	emoji = bot.get_emoji(746642817736114187)
	await channel_log.send(embed = Embed(
		title = f'{emoji} Новый участник!',
		description = f'{member.mention} присойденился к серверу.',
		colour = 0xfa1e1e))
	await member.add_roles(role)
	await member.send(
'''
Привет, добро пожаловать на сервер **Renaissance eSports**

**Если ты хочешь получить роль** __**Участник**__, то измени себе никнейм по формату **Никнейм(с учетом раскладки) [Имя]**.

__У нас проходит набор в гильдию, если желаете вступить - зайдите в текстовый канал #заявка-в-гильдию.__
__Так же у нас есть Ивент Битва Тренеров. Если вы хотите стать капитаном - напишите Ивент Менеджеру.__
''')

#Renove member
@bot.event
async def on_member_remove(member):
	channel_log = bot.get_channel(730455033346260992)
	emoji = bot.get_emoji(746642817895628840)
	await channel_log.send(embed = Embed(
		title = f'{emoji} Участник покинул нас',
		description = f'Пользыватель {member.mention} покинул наш сервер 😢',
		colour = 0xfa1e1e))

#Update member
@bot.event
async def on_member_update(before, after):
	channel_log = bot.get_channel(730455033346260992)
	guild = bot.get_guild(730187674043809894)
	emoji = bot.get_emoji(746642818025652254)
	#Update nick
	if before.nick != after.nick:        
		await channel_log.send(embed = Embed(
        	title = f'{emoji} Обновление ника',
        	description = f'**{before.nick}**({before.mention}) обновил свой ник.',
        	colour = 0xfa1e1e)
        	.add_field(name = 'Старый ник:', value = f'{before.nick}') 
        	.add_field(name = 'Новый ник:', value = f'{after.nick}'))
    #MuteRole
	if before.roles != after.roles:
		mute_role = get(guild.roles, id = 740937542483837039)
		if mute_role in after.roles:
			async for entry in guild.audit_logs(limit = 1, action = discord.AuditLogAction.member_role_update):
				if entry.user != bot.user:
					await channel_log.send(embed = Embed(
    				title = f'{emoji} Мут',
    				description = f'{entry.user.mention} замутил {entry.target.mention}',
    				colour = 0xfa1e1e))
   	#Unmure role
		if mute_role in before.roles:
			async for entry in guild.audit_logs(limit = 1, action = discord.AuditLogAction.member_role_update):
				if entry.user != bot.user:
					await channel_log.send(embed = Embed(
    				title = f'{emoji} Размут',
    				description = f'{entry.user.mention} размутил {entry.target.mention}',
    				colour = 0xfa1e1e))

#Update user
@bot.event
async def on_user_update(before, after):
	channel_log = bot.get_channel(730455033346260992)
	emoji = bot.get_emoji(746642818025652254)
	#Update avatar
	if before.avatar != after.avatar:
		await channel_log.send(embed = Embed(
			title = f'{emoji} Новая аватарка',
			description = f'{before.mention} поменял свою аватарку',
			colour = 0xfa1e1e)
			.set_thumbnail(url = after.avatar_url))

#On message
@bot.event
async def on_message(message):
	await bot.process_commands(message)
	if message.author.bot:
		return
	else:
		if message.channel.id in [730187674605977673]:
			x = random.randint(1, 1000000)
			y = random.randint(1, 1000000)
			if x == y:
				await message.channel.send(embed = Embed(
					description = f'{message.author} **вы одарованы ботом!**',
					colour = randcol()))
				await message.author.send(embed = Embed(
					description = 'Поздравляю! Я выбрал тебя на роль **БОГА**\nЯ открыл для тебя доступ в **Комнату Бога**, а так же возможность смены цвета',
					colour = randcol())
					.add_field(name = 'Примечание:',
						value = '''
						Цвет должен быть в формате HEX
						Выбрать цвет можно на этом -> [сайте](https://csscolor.ru/)
						Для смены цвета напиши **-setcolour [цвет**]
						Если тебе нужна помощь - обратись к администрации''', inline = False))

#Event ban user
@bot.event
async def on_member_ban(guild, user):
	warn_channel = bot.get_channel(730479350616686693)
	channel_log = bot.get_channel(730455033346260992)
	pressf = bot.get_emoji(746646614201991180)
	ban_emoji = bot.get_emoji(746655078726893618)
	async for entry in guild.audit_logs(limit = 1, action = discord.AuditLogAction.ban):
		if entry.user != bot.user:
			embed = Embed(
				title = f'{ban_emoji} Бан',
				description = f'Пользователю {entry.target} прилетел бан.\n\n**Press F**',
				colour = 0xfa1e1e)
			embed.add_field(name = 'Причина:', value = f'{entry.reason}', inline = False)
			embed.set_footer(icon_url = entry.user.avatar_url, text = entry.user)
			react = await channel_log.send(embed = embed)
			await react.add_reaction(pressf)
			await warn_channel.send(embed = embed)

#Unban
@bot.event
async def on_member_unban(guild, user):
	warn_channel = bot.get_channel(730479350616686693)
	channel_log = bot.get_channel(730455033346260992)
	unban_emoji = bot.get_emoji(746655079016431616)
	async for entry in guild.audit_logs(limit = 1, action = discord.AuditLogAction.unban):
		if entry.user != bot.user:
			embed = Embed(
				title = f'{unban_emoji} Разбан',
				description = f'{entry.target} был разбанен.',
				colour = 0xfa1e1e)
			embed.set_footer(icon_url = entry.user.avatar_url, text = entry.user)
			await channel_log.send(embed = embed)
			await warn_channel.send(embed = embed)

#Create voice
@bot.event
async def on_voice_state_update(member, before, after):	
	try:
		if after.channel.id == 746077987648307370:
			category = get(member.guild.categories, id = 746077633699381401)
			nick = member.name
			new_channel = await member.guild.create_voice_channel(nick, category = category)
			await new_channel.set_permissions(member,
				stream = True,
				use_voice_activation = True,
				manage_channels = True) #Права нового канала
			await member.move_to(new_channel)
			def check(x, y, z):
				l = len(new_channel.members)
				for user in new_channel.members:
					if user.bot:
						l -= 1
				return l == 0
			await bot.wait_for('voice_state_update', check = check)
			await new_channel.delete()
	except AttributeError:
		pass

#Reaction add
@bot.event
async def on_raw_reaction_add(payload):
	#Play role
	if payload.message_id == config.POST_ID_PLAY_ROLES:
		channel = bot.get_channel(payload.channel_id)
		message = await channel.fetch_message(payload.message_id)
		member = discord.utils.get(message.guild.members, id = payload.user_id)
		try:
			emoji = payload.emoji.id
			role = get(message.guild.roles, id = config.ROLES[emoji])
			play_role = get(message.guild.roles, id = config.ROLE_SEPARATOR)
			if role in member.roles:
				pass
			elif play_role in member.roles:
				await member.add_roles(role)
				await member.send(f'Вы получили роль: {role}.')					
			else:
				await member.add_roles(play_role)
				await member.add_roles(role)
				await member.send(f'Вы получили роль: {role}.')
		except KeyError:
				print(f'Роль для {emoji} не найдена')

	#Create report_channel
	if payload.message_id == config.POST_ID_REPORT:
		channel = bot.get_channel(payload.channel_id)
		message = await channel.fetch_message(payload.message_id)
		member = get(message.guild.members, id = payload.user_id)
		await message.remove_reaction(payload.emoji, member)
		if cursor.execute(f'SELECT repq FROM users WHERE id = {member.id}').fetchone()[0] == False:
			cursor.execute(f'UPDATE users SET repq = True WHERE id = {member.id}')
			category = get(member.guild.categories, id = 746427768941838526)
			moder_chat = get_channel(730454833194205194)
			moder_role = get(guild.roles, id = 730188643771088976)
			# Создаем канал с правами
			new_channel_report = await member.guild.create_text_channel(member.name, category = category)
			await new_channel_report.set_permissions(member, create_instant_invite = False, manage_channels = False, add_reactions = False, read_messages = True, send_messages = True, attach_files = True)
			msg = await new_channel_report.send(embed = Embed(description = '**Ожидайте...\nМодератор в ближайшее время свяжется с Вами!**', colour = 0xfa1e1e))
			complete = bot.get_emoji(746430035665354872)
			await msg.add_reaction(complete)
			# Отправляем сообщение модерации
			await moder_chat.send(f'{moder_role.mention}')
			await moder_chat.send(embed = Embed(description = f'{member.mention} **требует вашего внимания.**', colour = 0xfa1e1e))
			# Ждем ответа от модера
			def check(reaction, user):
				return user != message.author and user.id != member.id and str(reaction.emoji) == str(complete)
			react, user = await bot.wait_for('reaction_add', check = check)
			await new_channel_report.delete()
			cursor.execute(f'UPDATE users SET repq = False WHERE id = {member.id}')
			connection.commit()
			await msg.remove_reaction(complete, member)			
		else:
			await member.send(embed = Embed(description = 'Для Вас уже создан канал.', colour = 0xfa1e1e))

@bot.event			
async def on_raw_reaction_remove(payload):
	if payload.message_id == config.POST_ID_PLAY_ROLES:
		channel = bot.get_channel(payload.channel_id)
		message = await channel.fetch_message(payload.message_id)
		member = discord.utils.get(message.guild.members, id = payload.user_id)
		try:
			emoji = payload.emoji.id
			role = get(message.guild.roles, id = config.ROLES[emoji])
			play_role = get(message.guild.roles, id = config.ROLE_SEPARATOR)
			await member.remove_roles(role)
			await member.send(f'Роль {role} убрана.')
		except KeyError:
			print(f'Роль для {emoji} не найдена')
		TOP = get(message.guild.roles, id = config.PLAY_ROLES[0])
		JUNGLE = get(message.guild.roles, id = config.PLAY_ROLES[1])
		MID = get(message.guild.roles, id = config.PLAY_ROLES[2])
		ADC = get(message.guild.roles, id = config.PLAY_ROLES[3])
		SUPPORT = get(message.guild.roles, id = config.PLAY_ROLES[4])
		if TOP not in member.roles and JUNGLE not in member.roles and MID not in member.roles and ADC not in member.roles and SUPPORT not in member.roles:
			print('123')
			await member.remove_roles(play_role)

'''@bot.event
async def on_command_error(ctx, error):
	member = ctx.author
	channel = ctx.message.channel
	if isinstance(error, commands.MissingAnyRole):
		if ctx.command.name in ['clear', 'mute', 'unmute', 'ban', 'unban', 'warn', 'unwarn', 'say']:
			await ctx.send(embed = Embed(
				description = f'Упс, кажется у {ctx.author.mention} недостаточно прав.',
				colour = randcol()), delete_after = 5.0)
	if isinstance(error, commands.MissingRequiredArgument):
		if ctx.command.name == 'clear':
			await ctx.send(embed = Embed(
				description = f'{ctx.author.mention}, укажите количество сообщений.',
				colour = randcol()), delete_after = 5.0)
		if ctx.command.name in ['mute', 'unmute', 'ban', 'unban', 'warn', 'unwarn']:
			await ctx.send(embed = discord.Embed(
				description = f'{ctx.author.mention}, Вы забыли пользователя.',
				colour = randcol()), delete_after = 5.0)
		if ctx.command.name == 'say':
			await ctx.send(embed = discord.Embed(
				description = f'{ctx.author.mention}, Вы забыли указать канал.',
				colour = randcol()), delete_after = 5.0)
	if isinstance(error, commands.BadArgument):
		if ctx.command.name == 'clear':
			await ctx.send(embed = Embed(
				description = f'Так сколько сообщение нужно удалить 🧐?',
				colour = randcol()), delete_after = 5.0)
		if ctx.command.name in ['mute', 'unmute', 'ban']:
			await ctx.send(embed = discord.Embed(
				description = f'{ctx.author.mention}, пользователь Not Found.',
				colour = randcol()), delete_after = 5.0)
		if ctx.command.name == 'say':
			await ctx.send(embed = discord.Embed(
				description = f'Кажется такой канал не существует 🤔',
				colour = randcol()), delete_after = 5.0)
		if ctx.command.name == 'rand':
			await ctx.send(embed = Embed(
				description = 'Вы указали не правильные значения',
				colour = randcol()), delete_after = 5.0) '''


async def if_stop(ctx, x):
	await ctx.channel.purge(limit = x)
	await ctx.send(embed = Embed(description = 'Команда say прервана', colour = randcol()), delete_after = 5.0)

#======================================================
#					Admin Commands
#======================================================

#Clear command
@bot.command(name = 'clear', aliases = ['clear', 'очистить'])
@commands.has_any_role(730188450011021425, 730188643771088976, 730188373557248132, 730191238082592819)
async def clear(ctx, amount : int):
	await ctx.message.delete()
	if amount > 50:
		msg = await ctx.send(embed = Embed(
			description = f'{ctx.author.mention}, нельзя удалить так много сообщний за раз.',
			colour = 0xfa1e1e), delete_after = 5.0)
		await msg.add_reaction('🚫')
	elif amount == 0:
		await ctx.send(embed = Embed(
			description = 'И как мне удалить 0 сообщений 🧐?',
			colour = 0xfa1e1e), delete_after = 5.0)
	else:
		await ctx.channel.purge(limit = amount)
		if amount % 10 == 1:
			end = 'ие'
		elif amount % 10 > 1 and amount % 10 < 5:
			end = 'ия'
		else:
			end = 'ий'
		msg = await ctx.send(embed = Embed(
			description = f'{ctx.author.mention} удалил {amount} сообщен{end}.',
			colour = 0xfa1e1e), delete_after = 5.0)
		await msg.add_reaction('✅')

#Mute command
@bot.command(name = 'mute', aliases = ['mute', 'мут'])
@commands.has_any_role(730188450011021425, 730188643771088976, 730188373557248132, 730191238082592819)
async def mute(ctx, member : discord.Member, time = 12, *, reason = None):
	await ctx.message.delete()
	guild = bot.get_guild(730187674043809894)
	mute_role = get(guild.roles, id = 740937542483837039)
	channel_log = bot.get_channel(730455033346260992)
	warn_channel = bot.get_channel(730479350616686693)
	emoji = bot.get_emoji(746642818025652254)
	
	if reason == None:
		reason = 'Причина не указана'

	if time % 10 == 1:
		minutes = 'час'
	elif time % 10 > 1 and time % 10 < 5:
		minutes = 'часа'
	else:
		minutes = 'часов'

	if mute_role in member.roles:
		await ctx.send(embed = Embed(description = f'{member.mention} уже в муте.', colour = 0xfa1e1e), delete_after = 5.0)
		return

	if member == ctx.author:
		await ctx.send(embed = Embed(
			description = f'Как ты выбежал с дурки?',
			colour = 0xfa1e1e), delete_after = 5.0)
	else:
		await member.add_roles(mute_role)
		embed = Embed(
			title = f'{emoji} Мут',
			description = f'Пользователю {member.mention} был выдан мут на **{time} {minutes}**.',
			colour = 0xfa1e1e)
		embed.add_field(name = 'Причина:', value = f'{reason}', inline = False)
		embed.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
		await channel_log.send(embed = embed)
		await warn_channel.send(embed = embed)
		await asyncio.sleep(int(time * 60 * 60))
		await member.remove_roles(mute_role)
		embed = Embed(
			title = f'{emoji} Размут',
			description = f'Пользователь {member.mention} снова может говорить.',
			colour = 0xfa1e1e)
		embed.add_field(name = 'Причина:', value = 'Время мута вышло', inline = False)
		await channel_log.send(embed = embed)
		await warn_channel.send(embed = embed)

#Unmute command
@bot.command(name = 'unmute', aliases = ['unmute', 'анмут', 'размут'])
@commands.has_any_role(730188450011021425, 730188643771088976, 730188373557248132, 730191238082592819)
async def unmute(ctx, member : discord.Member, *, reason = None):
	await ctx.message.delete()
	channel_log = bot.get_channel(730455033346260992)
	guild = bot.get_guild(730187674043809894)
	mute_role = get(guild.roles, id = 740937542483837039)
	warn_channel = bot.get_channel(730479350616686693)
	emoji = bot.get_emoji(746642818025652254)

	if reason == None:
		reason = 'Причина не указана'

	if member == ctx.author:
		await ctx.send(embed = discord.Embed(
			description = f'Как ты выбежал с дурки?',
			colour = 0xfa1e1e), delete_after = 5.0)
	else:
		if mute_role in member.roles:
			await member.remove_roles(mute_role)
			embed = Embed(
				title = f'{emoji} Размут',
				description = f'Пользователь {member.mention} снова может говорить.',
				colour = 0xfa1e1e)
			embed.add_field(name = 'Причина:', value = f'{reason}', inline = False)
			embed.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
			await channel_log.send(embed = embed)
			await warn_channel.send(embed = embed)
		else:
			await ctx.send(embed = discord.Embed(
				description = f'{member.mention} не имеет мута',
				colour = 0xfa1e1e), delete_after = 5.0)

#Ban command
@bot.command(name = 'ban', aliases = ['ban', 'бан'])
@commands.has_any_role(730188450011021425, 730188643771088976, 730188373557248132, 730191238082592819)
async def ban(ctx, member : discord.Member, *, reason = None):
	await ctx.message.delete()
	channel_log = bot.get_channel(730455033346260992)
	warn_channel = bot.get_channel(730479350616686693)
	pressf = bot.get_emoji(746646614201991180)
	ban_emoji = bot.get_emoji(746655078726893618)

	if reason == None:
		reason = 'Причина не указана'

	if member == ctx.author:
		await ctx.send(embed = discord.Embed(
			description = f'Как ты выбежал с дурки?',
			colour = 0xfa1e1e), delete_after = 5.0)
	else:
		await member.ban(reason = reason)
		embed = Embed(
			title = f'{ban_emoji} Бан',
			description = f'Пользователю {member.mention} прилетел бан.\n\n**Press F**',
			colour = 0xfa1e1e)
		embed.add_field(name = 'Причина:', value = f'{reason}', inline = False)
		embed.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
		react = await channel_log.send(embed = embed)
		await react.add_reaction(pressf)
		await warn_channel.send(embed = embed)

#Umban command
@bot.command(name = 'unban', aliases = ['unban', 'анбан', 'разбан'])
@commands.has_any_role(730188450011021425, 730188643771088976, 730188373557248132, 730191238082592819)
async def unban(ctx, *, member):
	await ctx.message.delete()
	channel_log = bot.get_channel(730455033346260992)
	warn_channel = bot.get_channel(730479350616686693)
	guild = bot.get_guild(730187674043809894)
	unban_emoji = bot.get_emoji(746655079016431616)

	member_name, member_discriminator = member.split('#')
	banned_users = await ctx.guild.bans()
	for ban_entry in banned_users:
		user = ban_entry.user
		if (user.name, user.discriminator) == (member_name, member_discriminator):
			await ctx.guild.unban(user)
			embed = Embed(
				title = f'{unban_emoji} Разбан', description = f'{member} был разбанен.',
				colour = 0xfa1e1e)
			embed.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
			await channel_log.send(embed = embed)
			await warn_channel.send(embed = embed)
			return
		else:
			await ctx.send(embed = discord.Embed(
				description = f'**{member_name}#{member_discriminator}** не был найден.',
				colour = 0xfa1e1e), delete_after = 5.0)

@bot.command(name = 'say', aliases = ['сказать', 'say', 'отправить'])
@commands.has_any_role(730188450011021425, 730188643771088976, 730188373557248132, 730191238082592819)
async def say(ctx, channel : discord.TextChannel):
	await ctx.message.delete()
	check = lambda message: message.author == ctx.author
	x = 0

	# Title
	await ctx.send(embed = Embed(description = 'Укажите название нового сообщения.', colour = randcol()))
	msg = await bot.wait_for('message', check = check)
	x += 2
	if msg.content.lower() in ['stop', 'стоп']:
		await if_stop(ctx, x)
		return
	else:
		title = msg.content

	# Text
	await ctx.send(embed = Embed(description = 'Укажите текст нового сообщения.', colour = randcol()))
	msg = await bot.wait_for('message', check = check)
	x += 2
	if msg.content.lower() in ['stop', 'стоп']:
		await if_stop(ctx, x)
		return
	else:
		text = msg.content

	# Colour
	await ctx.send(embed = Embed(description = 'Укажите цвет вставки в формате HEX\n**Пример:** fa1e1e\nДля указания случайного цвета напишите: **r, rand, random**.',
		colour = randcol()))
	msg = await bot.wait_for('message', check = check)
	x += 2
	if msg.content.lower() in ['stop', 'стоп']:
		await if_stop(ctx, x)
		return
	elif msg.content.lower() in ['r', 'rand', 'random']:
		colour = randcol()
	else:
		try:
			colour = int(msg.content, 16)
		except ValueError:
			colour = randcol()
			await ctx.send(embed = Embed(description = 'Цвет был указан не корректно, по этому был заменен на случайный', colour = randcol()))
			x += 1

	# Image
	await ctx.send(embed = Embed(description = 'Вставьте ссылку на изображение.', colour = randcol()))
	msg = await bot.wait_for('message', check = check)
	x += 2
	if msg.content.lower() in ['stop', 'стоп']:
		await if_stop(ctx, x)
		return
	elif msg.content.lower() in ['n', 'no', 'not', 'none', 'н', 'нет']:
		image = ''
	else:
		image = msg.content

	# Author
	await ctx.send(embed = Embed(description = 'Указать Вас как автора?', colour = randcol()))
	msg = await bot.wait_for('message', check = check)
	x += 2
	if msg.content.lower() in ['stop', 'стоп']:
		await if_stop(ctx, x)
		return
	elif msg.content.lower() in ['n', 'no', 'not', 'none', 'н', 'нет']:
		icon_url_author = ''
		name = ''
	elif msg.content.lower() in ['y', 'ye', 'yes', 'д', 'да']:
		icon_url_author = ctx.author.avatar_url
		name = f'Сообщение от {ctx.author.name}'

	# Mention
	await ctx.send(embed = Embed(description = 'Кого следует упомянуть о сообщении?', colour = randcol()))
	msg = await bot.wait_for('message', check = check)
	x += 2
	if msg.content.lower() in ['stop', 'стоп']:
		await if_stop(ctx, x)
		return
	elif msg.content.lower() in ['everyone', 'всех']:
		role = get(ctx.message.guild.roles, name = '@everyone')
		message_for = 'everyone'
	elif msg.content.lower() in ['guild', 'гильдию', 'гильдия']:
		role = get(ctx.message.guild.roles, name = 'Гильдия')
		message_for ='гильдия'
	else:
		role = ''
		message_for = ''

	# Подтвердить
	await ctx.send('Вы хотите отправить следующее сообщение?')
	embed = Embed(
		title = title,
		description = text,
		colour = colour)
	embed.set_author(icon_url = icon_url_author, name = name)
	embed.set_image(url = image)
	await ctx.send(embed = embed)
	if message_for == '@everyone':
		role_mention = f'для {role}.'
	elif message_for == 'гильдия':
		role_mention = f'для {role.mention}.'
	else:
		role_mention = ''
	await ctx.send(f'В канал {channel.mention} {role_mention}')
	msg = await bot.wait_for('message', check = check)
	x += 4
	if msg.content.lower() in ['stop', 'стоп']:
		await if_stop(ctx, x)
		return
	elif msg.content.lower() in ['y', 'ye', 'yes', 'д', 'да']:
		if message_for != '':
			await channel.send(role_mention)
		await channel.send(embed = embed)
		await ctx.channel.purge(limit = x)
		react = await ctx.send(embed = Embed(description = 'Сообщение отправлено', colour = randcol()), delete_after = 5.0)
		await react.add_reaction('✅')
	elif msg.content.lower() in ['n', 'no', 'not', 'none', 'н', 'нет']:
		await ctx.channel.purge(limit = x)
		react = await ctx.send(embed = Embed(description = 'Сообщение не отправлено', colour = randcol()), delete_after = 5.0)
		await react.add_reaction('❌')

# Warn
@bot.command(name = 'warn', aliases = ['warn', 'варн', 'предупреждение'])
@commands.has_any_role(730188450011021425, 730188643771088976, 730188373557248132, 730191238082592819)
async def warn(ctx, member : discord.Member, *, reason = None):
	await ctx.message.delete()
	channel_log = bot.get_channel(730455033346260992)
	warn_channel = bot.get_channel(730479350616686693)

	if reason == None:
		reason = 'Причина не указана'

	if member == ctx.author:
		await ctx.send(embed = discord.Embed(
			description = f'Как ты выбежал с дурки?',
			colour = 0xfa1e1e), delete_after = 5.0)

	cursor.execute(f'UPDATE users SET warn = warn + 1 WHERE id = {member.id}')
	connection.commit()

	embed = Embed(title = 'Warn',
			description = f'Пользователь {member.mention} получил предупреждение от {ctx.author.mention}.', colour = 0xfa1e1e)
	embed.add_field(name = 'Причина:', value = f'{reason}', inline = True)
	embed.add_field(name = 'Предупреждений всего:', value = f'**{cursor.execute(f"SELECT warn FROM users WHERE id = {member.id}").fetchone()[0]}**', inline = True)
	await channel_log.send(embed = embed)
	await warn_channel.send(embed = embed)

	async def check_warn(ctx, member):
		if cursor.execute(f'SELECT warn FROM users WHERE id = {member.id}').fetchone()[0] == 3:
			await member.ban(reason = reason)
			embed = Embed(title = 'Ban',
				description = f'Пользователь {member.mention} был забанен.', colour = 0xfa1e1e)
			embed.add_field(name = 'Причина:', value = 'Получил 3 предупреждения', inline = True)
			embed.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
			react = await channel_log.send(embed = embed)
			await react.add_reaction('🇫')
			await warn_channel.send(embed = embed)
			cursor.execute(f'UPDATE users SET warn = 0 WHERE id = {member.id}')
			connection.commit()
	await check_warn(ctx, member)

# Unwarn
@bot.command(name = 'unwarn', aliases = ['unwarn', 'анварн', 'снять'])
@commands.has_any_role(730188450011021425, 730188643771088976, 730188373557248132, 730191238082592819)
async def unwarn(ctx, member : discord.Member, limit = 'all'):
	await ctx.message.delete()
	channel_log = bot.get_channel(730455033346260992)
	warn_channel = bot.get_channel(730479350616686693)

	warn = ''
	if limit == 'all':
		limit = 3
		warn = 'предупреждения'
	elif int(limit) >= 3:
		await ctx.send(embed = Embed(description = 'Вы не можете удалить столько предупреждений', colour = 0xfa1e1e), delete_after = 5.0)
		return
	elif int(limit) <= 0:
		await ctx.send(embed = Embed(description = 'Укажите количество варнов больше **1**.', colour = 0xfa1e1e), delete_after = 5.0)
		return
	else:
		if int(limit) % 10 == 1:
			warn = 'предупреждение'
		elif int(limit) % 10 == 2:
			warn = 'предупреждения'

	if member == ctx.author:
		await ctx.send(embed = discord.Embed(
			description = f'Как ты выбежал с дурки?',
			colour = 0xfa1e1e), delete_after = 5.0)
		return

	if cursor.execute(f'SELECT warn FROM users WHERE id = {member.id}').fetchone() == 0:
		await ctx.send(embed = Embed(description = f'У {member.mention} нет предупреждений.', colour = 0xfa1e1e), delete_after = 5.0)
		return
	else:
		cursor.execute(f'UPDATE users SET warn = warn - {int(limit)} WHERE id = {member.id}')

	if cursor.execute(f'SELECT warn FROM users WHERE id = {member.id}').fetchone()[0] <= 0:
		cursor.execute(f'UPDATE users SET warn = 0 WHERE id = {member.id}')
	connection.commit()

	embed = Embed(
		title = 'Unwarn',
		description = f'{ctx.author.mention} снял {limit} {warn} у пользователя {member.mention}.',
		colour = 0xfa1e1e)
	embed.add_field(name = 'Предупреждений всего: ', value = f'**{cursor.execute(f"SELECT warn FROM users WHERE id = {member.id}").fetchone()[0]}**', inline = False)
	await channel_log.send(embed = embed)
	await warn_channel.send(embed = embed)

# Пост с правилами
@bot.command()
@commands.has_any_role(730188450011021425, 730188643771088976, 730188373557248132, 730191238082592819)
async def rules_post(ctx):
	await ctx.message.delete()
	await ctx.send(embed = Embed(
		title = 'УСТАВ КЛУБА',
		colour = 0xfa1e1e
		)
		.add_field(name = '**1. Общие положения**',
			value = '''
			1.1 Решения Администрации обсуждению не подлежат и обязательны к исполнению;
			1.2 Вступающий в Клуб обязан ознакомится со всеми положениями Устава Клуба;
			1.3 Незнание Устава не освобождает от последствий за его нарушение;
			1.4 Руководство Клуба имеет право внести в любой момент изменения в настоящий Устав при возникновении соответствующей необходимости.
			''', inline = False)
		.add_field(name = '**2. Обязанности участников клуба**',
			value = '''
			2.1 Соблюдать положения настоящего Устава;
			2.2 Относиться с уважением к другим членам Клуба;
			2.3 Ник должен соответствовать установленному формату: Ник в игре [Имя];
			''', inline = False)
		.add_field(name = '**3. Членам клуба запрещается**',
			value = '''
			3.1 Выдавать себя за другое лицо;
			3.2 Использовать аватар, писать сообщения, размещать картинки, размещать материалы, использовать никнейм, статус несущие порнографический / оскорбительный характер или разжигающий межнациональные конфликты;
			3.3 Делать публичные заявления от имени Клуба без предварительного согласования с Администрацией;
			3.4 Писать бессмысленную или малосодержательную информацию, не несущую смысловой нагрузки (ФЛУД), спам командами, оффтоп, писать с включённой клавишей Caps Lock. Исключением является текстовый канал #общий-чат-флудилка;
			3.5 Допускать сторонние звуки в голосовом чате, мешающие другим игрокам;
			3.6 Рекламировать любые ресурсы, без согласования с Администрацией.
			''', inline = False)
		.add_field(name = '**4. Ответственность**',
			value = '''
			4.1 Если Администрация расценит Ваши действия как нарушение требований Устава, то вы рискуете получить БАН;
			4.2 За нарушение Устава Администрация вправе применить то наказание, какое посчитает нужным в каждом отдельном случае.
			''', inline = False)
		.add_field(name = 'Ссылки на наши ресурсы:',
			value = '''
			**[Группа Вконтакте](https://vk.com/renaissanceesport)
			[Twitch](https://www.twitch.tv/renaissance_esports)
			[Youtube](https://www.youtube.com/channel/UCQZWQNKAmvjdbtNrm2N4WFg)**
			''', inline = False))

# Информация о гильдии
@bot.command()
@commands.has_any_role(730188450011021425, 730188643771088976, 730188373557248132, 730191238082592819)
async def guild_info(ctx):
	await ctx.message.delete()
	channel = bot.get_channel(732206020679696385)
	guild_channel = bot.get_channel(730196134131269682)
	guild = bot.get_guild(730187674043809894)
	role = get(guild.roles, id = 730188901372657675)
	await ctx.send(embed = Embed(
		title = 'НАБОР В ГИЛЬДИЮ',
		colour = 0xfa1e1e)
		.add_field(name = 'Как попасть?', value = f'Оставляете заявку в {channel.mention} и ждете ответа!', inline = False)
		.add_field(name = 'Условия принятия', value = 'Ранг от **Серебро 4 Соло/Флекс** на момент подачи заявки.', inline = False)
		.add_field(name = 'И что дальше?', value = f'1. Вы получите роль {role.mention}.\n2. Для Вас будет открыт чат {guild_channel.mention}, в котором можно найти пати.', inline = False)
		.add_field(name = 'Правила', value = f'**Минимальное количество очков** - __200 в каждом этапе.__\nЕсли участник гильдии не выполняет норму - он исключаетсяя из гильдии и лишают роли {role.mention}'))
	await ctx.send('**КАК ПОДТВЕРДИТЬ УЧАСТИЕ?**')
	await ctx.send('url image 1')
	await ctx.send('url image 2')
	await ctx.send('url image 3')

# Про ботов
@bot.command()
@commands.has_any_role(730188450011021425, 730188643771088976, 730188373557248132, 730191238082592819)
async def about_bots(ctx):
	await ctx.message.delete()
	guild = bot.get_guild(730187674043809894)
	bot_hydra = get(guild.members, id = 547905866255433758)
	bot_panckake = get(guild.members, id = 239631525350604801)
	renaissanceesport_bot = get(guild.members, id = 739970734062829631)

	await ctx.send(embed = Embed(
		title = 'КОМАНДЫ БОТОВ',
		colour = 0xfa1e1e)
		.add_field(name = f'Команды {bot_hydra.mention}',
			value = '''
			Префикс бота: **!**;
			!song [название композиции/ссылка] - бот заходит в твой канал и включает музыку (ВКонтакте не поддерживает);
			:play_pause: - Пауза/Продолжить;
			:stop_button: - Остановить и очистить очередь;
			:track_next: - Пропустить трек;
			:arrows_counterclockwise: - Повторить песню;
			:regional_indicator_s: - Перетасовать очередь;
			:star: - Добавить текущую песню в избранное;
			:x: - Удаление текущей песни из избранного.
			Избранные песни можно включить сразу нажав на :star:
			''', inline = False)
		.add_field(name = f'Команды {bot_panckake.mention}',
			value = '''
			Префикс бота: **$**
			$join - Бот зайдет к Вам в комнату;
			$play [название композиции / ссылка] - Бот включит данную композицию (ВКонтакте не поддерживает);
			$pause - Бот приостановит воспроизведение композиции;
			$resume - Бот продолжит воспроизведение композиции;
			$queue - Бот покажет очередь композиций.
			''', inline = False)
		.add_field(name = f'Команды для {renaissanceesport_bot.mention}', value = 'Чтобы узнать список команд бота напишите **-help**', inline = False))

# Пост бота
@bot.command()
@commands.has_any_role(730188450011021425, 730188643771088976, 730188373557248132, 730191238082592819)
async def rolepost(ctx):
	toplane = bot.get_emoji(746424116218691654)
	jungle = bot.get_emoji(746424116051050589)
	midlane = bot.get_emoji(746424115489013874)
	botlane = bot.get_emoji(746424115606323281)
	support = bot.get_emoji(746424115854049280)

	react = await ctx.send(embed = Embed(
		title = 'Получение игровых ролей',
		description = '**Для полечения игровой роли нажмите на соотвествующую реакцию под сообщением.**',
		colour = 0xfa1e1e))
	await react.add_reaction(toplane)
	await react.add_reaction(jungle)
	await react.add_reaction(midlane)
	await react.add_reaction(botlane)
	await react.add_reaction(support)

# Пост бота
@bot.command()
@commands.has_any_role(730188450011021425, 730188643771088976, 730188373557248132, 730191238082592819)
async def post(ctx):
	guild = bot.get_guild(730187674043809894)
	reaction = bot.get_emoji(746426449694687253)
	react = await ctx.send(embed = Embed(
		title = 'Жалоба/Вопрос',
		description = '**Если у Вас есть вопрос или жалоба, то нажмите на реакцию ниже, и Модератор сервера свяжется с Вами!**', colour = 0xfa1e1e)
		.set_footer(text = 'Администрация Renaissance eSports', icon_url = guild.icon_url))

	await react.add_reaction(reaction)

# Инфо о ролях
@bot.command()
@commands.has_any_role(730188450011021425, 730188643771088976, 730188373557248132, 730191238082592819)
async def roleinfo(ctx):
	id_roles = [730188373557248132, 730191238082592819, 730188450011021425,
	730188643771088976, 730189868109529108, 730190188285788201,
	730518905348685877, 730199188326973460, 730190651936866445,
	730188901372657675, 730189110022635631, 730189588781334540]
	guild = bot.get_guild(730187674043809894)
	role1 = get(guild.roles, id = 730188373557248132)
	role2 = get(guild.roles, id = 730191238082592819)
	role3 = get(guild.roles, id = 730188450011021425)
	role4 = get(guild.roles, id = 730188643771088976)
	role5 = get(guild.roles, id = 730189868109529108)
	role6 = get(guild.roles, id = 730190188285788201)
	role7 = get(guild.roles, id = 730518905348685877)
	role8 = get(guild.roles, id = 730199188326973460)
	role9 = get(guild.roles, id = 730190651936866445)
	role10 = get(guild.roles, id = 730188901372657675)
	role11 = get(guild.roles, id = 730189110022635631)
	role12 = get(guild.roles, id = 730189588781334540)

	await ctx.send(embed = Embed(title = 'Информация о ролях сервера',
		description = f'''
		{role1} - Главенствующий в этом клубе.
		{role2} - Главный по Ивентам в клубе.
		{role3} - Старший модератор.
		{role4} - Модератор, следящий за исполнением Устава клуба.
		{role5} - Важные участники этого клуба.
		{role6} - Комментатор этого клуба.
		{role7} - Стример этого клуба.
		{role8} - Капитан команды на ивент Битву Тренеров.
		{role9} - Участники ивента Битва Тренеров этого клуба.
		{role10} - Участники гильдия этого клуба.
		{role11} - Участники клуба Renaissance eSport.
		{role12} - Гость клуба
		''', colour = 0xfa1e1e))

#======================================================================
#						Commands
#======================================================================

# Hello
@bot.command(aliases = ['hello', 'привет', 'хай', 'hi', 'holla'])
@commands.check(is_not_onotoliy)
async def hello(ctx):
	await ctx.message.delete()
	hello = random.choice(hello_words)
	compliment = random.choice(compliment_words)
	emoji = random.choice(smile_list)
	await ctx.send(embed = Embed(description = f'{hello} {ctx.author.mention}, {compliment} {emoji}', colour = randcol()))

# Info user
@bot.command()
@commands.check(is_not_onotoliy)
async def info(ctx, member : discord.Member = None):
	await ctx.message.delete()
	guild = bot.get_guild(730187674043809894)

	online_emoji = bot.get_emoji(746440243787595948)
	offline_emoji = bot.get_emoji(746440243359645779)
	idle_emoji = bot.get_emoji(746440243686932642)
	dnd_emoji = bot.get_emoji(746440243636338779)

	if member == None:
		member = ctx.author

	embed = Embed(
		title = f'Информация о {member}:',
		colour = randcol())
	if member != ctx.author:
		embed.set_author(icon_url = ctx.author.avatar_url, name = f'Запрос от {ctx.author.name}')
	embed.set_thumbnail(url = member.avatar_url)
	embed.add_field(name = 'Ник:', value = f'{member.name}', inline = False)
	embed.add_field(name = 'Тэг:', value = f'#{member.discriminator}', inline = False)
	embed.add_field(name = 'ID:', value = f'{member.id}', inline = False)

	day_now = datetime.datetime.now() # Дата сегодня

	async def day_end(days):
		if days % 10 == 1:
			day = 'день'
		elif days % 10 > 1 and days % 10 < 5:
			day = 'дня'
		else:
			day = 'дней'
		return day

	async def type_days(h):
		if h > 5 and h < 12:
			hour = 'утра'
		elif h > 13 and h < 17:
			hour = 'дня'
		elif h > 18 and h < 22:
			hour = 'вечера'
		else:
			hour = 'ночи'
		return hour 
		
	creat_date = member.created_at # Аккаунт создан
	day_with = day_now - creat_date # Дней в Discord
	hour = await type_days(creat_date.hour)
	date_str_create = creat_date.strftime(f'%a, %d.%m.%Y в %H:%M:%S {hour}') # Дата создания в нормальном виде
	day = await day_end(day_with.days)
	embed.add_field(name = 'Аккаунт создан:', value = f'🗓 {date_str_create}.\nЭто же {day_with.days} {day} назад!', inline = False)

	creat_date = member.joined_at # Присойденился
	day_with = day_now - creat_date # Дней на сервере
	hour = await type_days(creat_date.hour)
	date_str_create = creat_date.strftime(f'%a, %d.%m.%Y в %H:%M:%S {hour}') # Дата присойденения к серверу в нормальном виде
	day = await day_end(day_with.days)
	embed.add_field(name = 'Присойденился к серверу:', value = f'🗓 {date_str_create}.\nЭто же {day_with.days} {day} назад!', inline = False)

	member_status = member.status
	if str(member_status) == 'online':
		status = f'{online_emoji} | В сети'
	elif str(member_status) == 'dnd':
		status = f'{dnd_emoji} | Не беспокоить'
	elif str(member_status) == 'idle':
		status = f'{idle_emoji} | Не активен'
	else:
		status = f'{offline_emoji} | Не в сети'
	embed.add_field(name = 'Статус:', value = f'{status}', inline = False)

	if str(member_status) != 'offline':
		mobile = member.mobile_status
		desktop = member.desktop_status
		web = member.web_status
		if str(desktop) in ['online', 'idle', 'dnd'] or str(web) in ['online', 'idle', 'dnd']:
			embed.add_field(name = 'В сети с:', value = '🖥', inline = False)
		else:
			embed.add_field(name = 'В сети с:', value = '📱', inline = False)

	await ctx.send(embed = embed)

# Info server
@bot.command(aliases = ['serverinfo'])
@commands.check(is_not_onotoliy)
async def server_info(ctx):
	await ctx.message.delete()
	guild = ctx.message.guild

	async def day_end(days):
		if days % 10 == 1:
			day = 'день'
		elif days % 10 > 1 and days % 10 < 5:
			day = 'дня'
		else:
			day = 'дней'
		return day

	async def type_days(h):
		if h > 5 and h < 12:
			hour = 'утра'
		elif h > 13 and h < 17:
			hour = 'дня'
		elif h > 18 and h < 22:
			hour = 'вечера'
		else:
			hour = 'ночи'
		return hour 

	online_emoji = bot.get_emoji(746440243787595948)
	offline_emoji = bot.get_emoji(746440243359645779)
	idle_emoji = bot.get_emoji(746440243686932642)
	dnd_emoji = bot.get_emoji(746440243636338779)
	members_all_emoji = bot.get_emoji(746451296881475715)
	boost_emoji = bot.get_emoji(746451296608976928)
	steam_emoji = bot.get_emoji(746451296403456053)

	creat_date = guild.created_at # Сервер создан
	now_date = datetime.datetime.now() # Дата сегодня
	day_with = now_date - creat_date # Дней назад
	hour = await type_days(creat_date.hour)
	date_str_create = creat_date.strftime(f'%a, %d.%m.%Y в %H:%M:%S {hour}') # Дата создания в нормальном виде
	day = await day_end(day_with.days)

	embed = Embed(
		title = f'Информация о {guild.name}',
		colour = randcol())
	embed.set_author(icon_url = ctx.author.avatar_url, name = f'Запрос от {ctx.author.name}')
	embed.set_thumbnail(url = guild.icon_url)
	embed.add_field(name = 'Создатель сервера:', value = f'{guild.owner.mention}', inline = False)
	embed.add_field(name = 'ID сервера:', value = f'{guild.id}', inline = False)
	embed.add_field(name = 'Регион:', value = f'🇷🇺 {str.capitalize(str(guild.region))}', inline = False)
	embed.add_field(name = 'Дата создания:', value = f'🗓 {date_str_create}\nЭто же {day_with.days} {day} назад!', inline = False)
	embed.add_field(name = 'Количество каналов:', value = f'Всего | {len(guild.channels)}\n📝 Текстовых | {len(guild.text_channels)}\n🎙 Голосовых | {len(guild.voice_channels)}', inline = False)
	
	member_online = 0
	member_idle = 0
	member_dnd = 0
	member_offline = 0
	member_stream = 0
	for member in guild.members:
		member_status = member.status
		if str(member_status) == 'online':
			member_online += 1
		elif str(member_status) == 'idle':
			member_idle += 1
		elif str(member_status) == 'dnd':
			member_dnd += 1
		else:
			member_offline +=1
		if member != bot.user:
			if member.activity != None:
				if str(member.activity.type) == 'ActivityType.streaming':
					member_stream += 1


	embed.add_field(name = 'Количество участников:\n', value = f'''
		{members_all_emoji} Всего | {guild.member_count}
		{online_emoji} В сети | {member_online}
		{idle_emoji} Не активен | {member_idle}
		{dnd_emoji} Не беспокоить | {member_dnd}
		{offline_emoji} Не в сети | {member_offline}
		{boost_emoji} Премиум | {len(guild.premium_subscribers)}
		{steam_emoji} Сейчас стримит | {member_stream}
		''', inline = False)
	embed.add_field(name = 'Количество смайликов:', value = f'🧐 | {len(guild.emojis)}', inline = False)

	await ctx.send(embed = embed)

# Warn info
@bot.command()
@commands.check(is_not_onotoliy)
async def warn_info(ctx, member : discord.Member = None):
	await ctx.message.delete()

	if member is None:
		member = ctx.author

	warn_count = cursor.execute(f'SELECT warn FROM users WHERE id = {member.id}').fetchone()[0]
	if warn_count > 0:
		if int(warn_count) % 10 == 1:
			warn = 'предупреждение'
		else:
			warn = 'предупреждения'
		await ctx.send(embed = Embed(
			description = f'У пользователя {member.mention} **`{warn_count} {warn}`**.', colour = 0xfa1e1e).set_author(icon_url = ctx.author.avatar_url, name = f'Запрос от {ctx.author}'))
	else:
		await ctx.send(embed = Embed(description = f'У пользователя {member.mention} нет предупреждений', colour = 0xfa1e1e).set_author(icon_url = ctx.author.avatar_url, name = f'Запрос от {ctx.author}'))

# Игра в флаги
@bot.command(aliases = ['флаг', 'флаги', 'flag', 'flags'])
@commands.check(is_not_onotoliy)
async def game_flag(ctx):

	await ctx.send(embed = Embed(title = 'Правила игры',
		description = '''
		Задача игроков написать название страны по флагу. Принимается только первый правильный ответ.
		Кол-во участников неограничено.
		P.S. Название указывать только **полное** и только на **русском языке**.
		
		Для начала игры укажите кол-во раундов.
		Максимум раундов: **20**.
		''', colour = randcol()))
	try:
		msg = await bot.wait_for('message', timeout = 60.0)
		rounds = int(msg.content)
		if rounds >= 21:
			await ctx.send(embed =Embed(description = 'Максимум **20** раундов', colour = randcol()), delete_after = 5.0)
			return await game_flag(ctx)
	except ValueError:
		await ctx.send(embed = Embed(description = 'Вы указали не верное значение :(', colour = randcol()), delete_after = 5.0)
		return await game_flag(ctx)
	except asyncio.TimeoutError:
		await ctx.send(embed = Embed(description = 'Время подготовки вышло :(', colour = randcol()), delete_after = 5.0)
	else:
		await ctx.send(embed = Embed(title = 'ПОЕХАЛИ!', colour = randcol()))
		await asyncio.sleep(1)
		event_members = {}
		with open('flags.json', 'r', encoding = 'utf8') as f:
			flags = json.load(f)
			count = 1
			flags_list = []
			while count <= rounds:
				flag = random.choice(flags['Флаги'])
				if flag in flags_list:
					pass
				elif flag not in flags_list:
					flags_list.append(flag)
					x = 10
					await ctx.send(embed = Embed(title = f'Раунд | {count}',
						colour = randcol())
						.set_image(url = flag['url']))

					def check(msg):
						otvet = msg.content.lower()
						if otvet == flag['answer'].lower() and msg.channel == ctx.channel:
							return otvet
				
					try:
						msg = await bot.wait_for('message', timeout = 10.0, check = check)
						title = ''
						text = ''
						if str(msg.author.id) not in event_members:
							event_members[str(msg.author.id)] = {}
							event_members[str(msg.author.id)]['score'] = 0
						else:
							pass
						otvet_user = msg.content.lower()
						if otvet_user == flag['answer'].lower():
							event_members[str(msg.author.id)]['score'] += 1
							title = 'Дан правильный ответ!'
							text = f'{ctx.author.mention} дал правильный ответ.'
						elif otvet_user != flag['answer']:
							pass
					except asyncio.TimeoutError:
						title = 'Время вышло'
						text = 'Правильного ответа не было :('
					await ctx.send(embed = Embed(title = title, description = text, colour = randcol()))
					count += 1
					await asyncio.sleep(1)
					if count > rounds:
						embed = Embed(title = 'Игра завершена\nРезультати:')
						leaders = sorted(event_members, key = lambda score: event_members[score]['score'], reverse = True)
						position = 1
						for leader in leaders:
							leader = bot.get_user(int(leaders[position - 1]))
							leader_score = event_members[str(leader.id)]['score']
							embed.add_field(name = f'{position} место:', value = f'{leader.mention} | очки: **{leader_score}**', inline = False)
							position += 1
						embed.set_footer(text = 'Спасибо, что используете бота.\nЕсли Вы обнаружили ошибку или баг, то сообщите, пожалуйста, администрации.')
						await ctx.send(embed = embed)
						return

@bot.command(aliases = ['report'])
@commands.check(is_not_onotoliy)
async def create_report(ctx):
	await ctx.message.delete()
	if cursor.execute(f'SELECT repq FROM users WHERE id = {ctx.author.id}').fetchone()[0] == False:
		cursor.execute(f'UPDATE users SET repq = True WHERE id = {ctx.author.id}')
		category = get(ctx.author.guild.categories, id = 746427768941838526)
		moder_chat = get_channel(730454833194205194)
		moder_role = get(guild.roles, id = 730188643771088976)
		# Создаем новый канал с правами
		new_channel_report = await ctx.author.guild.create_text_channel(ctx.author.name, category = category)
		await new_channel_report.set_permissions(ctx.author, create_instant_invite = False, manage_channels = False, add_reactions = False, read_messages = True, send_messages = True, attach_files = True)
		msg = await new_channel_report.send(embed = Embed(description = '**Ожидайте...\nМодератор в ближайшее время свяжется с Вами!**', colour = 0xfa1e1e))
		complete = bot.get_emoji(746430035665354872)
		await msg.add_reaction(complete)
		# Отрпавляем сообщение модераторам
		await moder_chat.send(f'{moder_role.mention}')
		await moder_chat.send(embed = Embed(description = f'{ctx.author.mention} **требует вашего внимания.**', colour = 0xfa1e1e))
		# Ждем ответа от модератора
		def check(reaction, user):
			return user != message.author and user.id != ctx.author.id and str(reaction.emoji) == str(complete)
		react, user = await bot.wait_for('reaction_add', check = check)
		await new_channel_report.delete()
		cursor.execute(f'UPDATE users SET repq = False WHERE id = {ctx.author.id}')
		connection.commit()
		await msg.remove_reaction(complete, ctx.author)			
	else:
		await ctx.author.send(embed = Embed(description = 'Для Вас уже создан канал.', colour = 0xfa1e1e))

# Случайное число
@bot.command(name = 'rand')
@commands.check(is_not_onotoliy)
async def rand(ctx, *, num = 100):
	rand_num = random.randint(1, num)

	embed = Embed(description = '🎲 бросаю кубик...', colour = randcol())
	msg = await ctx.send(embed = embed)
	await asyncio.sleep(1.5)
	new_embed = Embed(description = f'... упало число **{rand_num}** 🎲', colour = randcol())
	await msg.edit(embed = new_embed)

# Смена цвета роли Бота
'''@bot.command()
@commands.has_role(746711912959442975)
async def setcolour(ctx, colour : discord.Colour):
	guild = get_guild(730187674043809894)
	role = get(guild.roles, id = 746711912959442975)
	await role.edit(colour = colour)
	await ctx.send('Ты успешно поменял цвет роли')'''

# Помощь
@bot.command(name = 'help')
@commands.check(is_not_onotoliy)
async def help(ctx):
	await ctx.message.delete()

	supp_emoji = bot.get_emoji(746687700127580210)
	guide_emoji = bot.get_emoji(746690228529397780)
	smile_emoji = random.choice(smile_list)
	channel_flag = bot.get_channel(746692378760314901)
	report_channel = bot.get_channel(746427967969820775)
	role_channel = bot.get_channel(746079454803263488)

	embed1 = Embed(title = f'{supp_emoji} Помощник Renaissance eSports',
		description = 'Реакции под сообщением преключают страницы',
		colour = randcol())
	embed1.add_field(name = 'Общие команды',
		value = f'{guide_emoji} Описание общедоступных команд для бота', inline = False)
	embed1.add_field(name = 'События сервера',
		value = f'{guide_emoji} Описание событий, в которых задействован бот', inline = False)
	embed1.add_field(name = 'Модерация',
		value = f'{guide_emoji} Описание команд для модерации', inline = False)
	embed1.set_footer(text = 'Сообщение удалиться через 5 минут бездействия')
	embed1.set_author(icon_url = ctx.author.avatar_url, name = f'Запрос от {ctx.author.name}')

	embed2 = Embed(title = 'Общие команды',
		description = '📌 Префикс бота: **-**',
		colour = randcol())
	embed2.add_field(name = 'hello', value = f'Поздоровайся с ботом {smile_emoji}', inline = False)
	embed2.add_field(name = 'info [участник]', value = 'Получить информацию о пользователе.\nЕсли участник не указан - выводит информацию об авторе', inline = False)
	embed2.add_field(name = 'serverinfo', value = 'Показать информацию о сервере.', inline = False)
	embed2.add_field(name = 'warninfo [участник]', value = 'Показать информацию о предупреждениях пользователя.\nЕсли участник не указан - выводит информацию об авторе', inline = False)
	embed2.add_field(name = 'flag', value = f'Игра во флаги\nТолько для канала {channel_flag.mention}', inline = False)
	embed2.add_field(name = 'rand [число]', value = 'Случайное число в диапазоне от 1 до заданного.', inline = False)

	embed3 = Embed(title = 'События сервера',
		colour = randcol())
	embed3.add_field(name = 'Создать голосовой канал', value = 'Для создания голосового канала зайдите в канал **Создать канал**', inline = False)
	embed3.add_field(name = 'Отрпавить жалобу / задать вопрос', value = f'Перейдите в текстовый канал {report_channel.mention}', inline = False)
	embed3.add_field(name = 'Получение игровых ролей', value = f'Перейдите в текстовый канал {role_channel.mention}', inline = False)

	guild = bot.get_guild(730187674043809894)
	moder_role = get(guild.roles, id = 730188643771088976)
	if ctx.author.top_role >= moder_role:
		embed4 = Embed(title = 'Модерция',
			colour = randcol())
		embed4.add_field(name = 'clear [число]', value = 'Очищает чат. Максимум 50 сообщений за раз', inline = False)
		embed4.add_field(name = 'mute [пользователь] [время] [причина]', value = 'Мутит пользователя.\nВремя устанавливается в **часах**.\nПо-умолчанию, причина не указана', inline = False)
		embed4.add_field(name = 'unmute [пользователь] [причина]', value = 'Размутит пользователя.\nПо-умолчанию, причина не указана', inline = False)
		embed4.add_field(name = 'ban [пользователя] [причина]', value = 'Забанить пользователя.\nПо-умолчанию, причина не указана', inline = False)
		embed4.add_field(name = 'unban [пользователь]', value = 'Разбанить пользователя', inline = False)
		embed4.add_field(name = 'warn [пользователь] [причина]', value = 'Дать предупреждение.\nПо-умолчанию, причина не указана', inline = False)
		embed4.add_field(name = 'unwarn [пользователь] [кол-во]', value = 'Снять предупреждение.\nПо-умолчанию, кол-во равно **all**', inline = False)
		embeds = [embed1, embed2, embed3, embed4]
	else:
		embeds = [embed1, embed2, embed3]
	message = await ctx.send(embed = embed1)

	page = Paginator(bot, message,
		only = ctx.author,
		embeds = embeds,
		timeout = 300,
		use_exit = True,
		delete_message = True,
		footer = False,
		reactions = ['<:arrowleft:746697454212087809>', '<:arrowright:746697454300299295>'],
		exit_reaction = ['<:exit:746695899253571694>'])
	await page.start()

#START BOT
token=os.environ.get('BOTTOKEN')
bot.run(str(token))
