import asyncio
import discord
import os
import random
import numpy
import json
import requests
import time
import config
from management import Management

from discord.ext import commands, tasks
from discord.ext.commands import MissingPermissions
from io import BytesIO


# from dotenv import load_dotenv

class Listener(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.react_msg_id = []
        self.emojis = ['🥺', '😳']
        self.logchid = 0
        self.onjoinchid = 0

    #add on_voice_state_update on_user_update

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None:
            if after.channel is not None:
                embed = discord.Embed(
                    title=f"{member}",
                    colour=discord.Colour.from_rgb(27, 44, 151))
                embed.add_field(name= f'{member.name} has joined a voice channel:',
                                value = f'**Server**: {after.channel.guild} \n **Channel**: {after.channel.mention}')
                channel = self.bot.get_channel(config.LOGCHID)
                await channel.send(embed = embed)
        elif before.channel is not None:
            if after.channel is not None:
                embed = discord.Embed(
                    title=f"{member}",
                    colour=discord.Colour.from_rgb(27, 44, 151))
                embed.add_field(name=f'{member.name} has changed voice channels',
                                value=f'before:{before.channel.mention} \n after:{after.channel.mention}')
                channel = self.bot.get_channel(config.LOGCHID)
                await channel.send(embed=embed)
            elif after.channel is None:
                embed = discord.Embed(
                    title=f"{member}",
                    colour=discord.Colour.from_rgb(27, 44, 151))
                embed.add_field(name=f'{member.name} has left the voice channel:',
                                value=f'**Server**: {before.channel.guild}: \n **channel**: {before.channel.mention}')
                channel = self.bot.get_channel(config.LOGCHID)
                await channel.send(embed=embed)
        else:
            return

    @commands.Cog.listener()
    async def on_message(self, message):
    #    print(f'{message.content}') #for testing
    #    print(f'{message.guild.owner.mention}')
    #    print(f'{message.guild.owner.status}')
        #print(f'{time.localtime(time.time())}')
        if not message.author.bot:
            if message.content.lower().startswith('i dont like'):
                channel = message.channel
                await channel.send('i dont like you!')
            # if message.content.lower().startswith(('remind me', 'tomorrow', 'tmr')):
            #     channel = message.channel
            #     await channel.send('would you like a reminder? use !reminder')
            if message.content.lower().startswith(('i cant choose', 'cant choose', 'i can\'t choose')):
                channel = message.channel
                await channel.send('try !=choose')
            if message.content.lower().startswith('help'):
                channel = message.channel
                await channel.send('do you need help? maybe !=help will help you')
            # remember for bool all int values not 0 is true, fix bottom later
            if message.content.lower().find('hug me') != -1:
                channel = message.channel
                ctx = await channel.send('!=hug',delete_after = 0)
                abc = random.randint(0, 1)
                if abc == 1:
                    await Management.hug3(self, ctx, message.author)
                    # await self.bot.invoke(self.bot.get_command('hug3'), member=message.author)
                else:
                    await Management.hug3(self, ctx)
                    # await self.bot.invoke(self.bot.get_command('hug3'))
            print(f'#mentions: {len(message.mentions)}')
            if(len(message.mentions) == 1): # maybe >1 but it deletes whole msg if multiple ppl are pinged and only 1 of them are on dnd\
                print('in')
                if (str(message.mentions[0].status) == 'dnd'):
                    print('in2')
                    channel = await message.mentions[0].create_dm()
                    msgcont = message.content.replace(str(message.mentions[0].id), message.mentions[0].name)
                    print(msgcont)
                    await channel.send(f'{message.author}: {msgcont}')#maybe do a check later check or just have it in log ch even tho deleted msgs are sent there
                    channel = message.channel
                    await message.delete()
                    await channel.send(f'don\'t ping {message.mentions[0]}', delete_after=5)
            # if (len(message.mentions) > 1):  # maybe >1 but it deletes whole msg if multiple ppl are pinged and only 1 of them are on dnd\
            #     print('in')
            #     for i in len(message):
            #       
            #     if (str(message.mentions[0].status) == 'dnd'):
            #         print('in2')
            #         channel = await message.mentions[0].create_dm()
            #         msgcont = message.content.replace(str(message.mentions[0].id), message.mentions[0].name)
            #         print(msgcont)
            #         await channel.send(
            #             f'{message.author}: {msgcont}')  # maybe do a check later check or just have it in log ch even tho deleted msgs are sent there
            #         channel = message.channel
            #         await message.delete()
            #         await channel.send(f'don\'t ping {message.mentions[0]}', delete_after=5)
            # maybe have bot command to set custom do not disturb (self.dnd = true/false)? or
            # #figure out how to do this for not jsut guild owner? maybe a list of dnd members? read thru message to
            #find <@ or <@! and find the member to check dnd and then delete msgs?
            elif (str(message.guild.owner.status) == 'dnd'):
                # print(f'message content:{message.content}')
                # print(f'message content:{message.content.lower()}')
                # print(f"found 1: {message.content.lower().find(f'{message.guild.owner.mention}')}")
                # print(f"found 2: {message.content.lower().find(f'@!{message.guild.owner.id}')}")
                # print(f'mention:{message.guild.owner.mention}')
                # print(f'id: {message.guild.owner.id}')
                if message.content.lower().find(f'{message.guild.owner.mention}') != -1 or message.content.lower().find(f'<@!{message.guild.owner.id}>') != -1:
                    #doesnt work if no nickname(<@249016489628139520>) vs nickname(<@!249016489628139520>)
            #   if message.content.lower().find('<@!249016489628139520>') != -1: #this to test how mentioning works and maybe use it as a prefix
                    #next 2 lines uncomment if you mute this bot's dms/ or add a self.dndmode  for true/false for on or off
                    channel = await message.guild.owner.create_dm()
                    msgcont = message.content.replace(str(message.guild.owner.id), message.guild.owner.name)
                    await channel.send(f'{message.author}: {msgcont}')
                    channel = message.channel
                    await message.delete()
                    await channel.send(f'don\'t ping {message.guild.owner}', delete_after = 5)
            #top if statement isnt needed now?^

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        embed = discord.Embed(
            title=f"User banned",
            colour=discord.Colour.from_rgb(0, 0, 0))
        embed.add_field(name=f'User has been banned from {guild}:', value = f'{user.mention}', inline=False)
        channel = self.bot.get_channel(config.LOGCHID)
        now = guild.created_at.now().strftime('%b-%d-%Y %I:%M %p')
        embed.set_footer(text=f"Banned on: {now}")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        embed = discord.Embed(
            title=f"User unbanned",
            colour=discord.Colour.from_rgb(255, 255, 255))
        embed.add_field(name=f'User has been unbanned from {guild}:', value = f'{user.mention}', inline=False)
        channel = self.bot.get_channel(config.LOGCHID)
        now = guild.created_at.now().strftime('%b-%d-%Y %I:%M %p')
        embed.set_footer(text=f"Banned on: {now}")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        embed = discord.Embed(
            title=f"Message has been edited",
            colour=discord.Colour.from_rgb(25, 102, 182))
        embed.add_field(name="Before edit:", value=f"{before.content}", inline=False)
        embed.add_field(name="After edit:", value=f"{after.content}", inline=False)
        log_ch = config.LOGCHID
        channel = self.bot.get_channel(log_ch)
        now = before.created_at.now().strftime('%I:%M %p')
        embed.set_footer(text=f"Message ID: {before.id} |Edited at:{now}")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        now = message.created_at.now().strftime('%I:%M %p')
        embed = discord.Embed(
            title=f"Message by {message.author} has been deleted",
            description=f"{message.content}",
            colour=discord.Colour.red())
        now = message.created_at.now().strftime('%I:%M %p')
        embed.set_footer(text=f"Message ID: {message.id} |Deleted at:{now}")
        log_ch = config.LOGCHID
        channel = self.bot.get_channel(log_ch)
        await channel.send(embed=embed)
        # : discord.member part is optional?

    @commands.Cog.listener()
    async def on_member_join(self, member: commands):
        channel = self.bot.get_channel(885745300118069318)
        embed = discord.Embed(
            title=f"Welcome {member.name}",
            description=
            f"Thanks for joining {member.guild.name}, {member.mention} !")
        embed.set_image(
            url=config.SERVER_IMG)
        embed.set_thumbnail(url=member.avatar_url)
        await channel.send(embed=embed)
        await channel.send(f'hai hows your day {member.mention}')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(885745300118069318)
        await channel.send(f'we never wanted you anyways {member.mention}, you\'re not welcome back')

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        # log_ch = config.LOGCHID
        # channel = self.bot.get_channel(log_ch)
        # embed = discord.Embed(
        #   title=f"{before}",
        #   description=
        #   f"things have changed!",
        #   colour=discord.Colour.from_rgb(25, 102, 182))
        # await channel.send(embed=embed)
        log_ch = config.LOGCHID
        channel = self.bot.get_channel(log_ch)
        color = discord.Colour.from_rgb(25, 102, 182)
        print(f'id = {after.id}')
        print(f'name: {after.name}')
        print(f'guild id: {after.guild.id}')
        print(f'guild name: {after.guild.name}')
        if str(after.activity) == "🤐 512":
            role = discord.utils.get(after.guild.roles, name="secret status role")
            await after.add_roles(role)
            descr = f"{after.mention} got a secret role \n "
        elif str(before.activity) == "🤐 512":
            if str(after.activity) != "🤐 512":
                role = discord.utils.get(after.guild.roles, name="secret status role")
                await after.remove_roles(role)
                descr = f"{after.mention}'s secret role got removed \n "
        elif str(before.status) == "online":
            if str(after.status) == "idle":
                role = discord.utils.get(after.guild.roles, name="afkers")
                await after.add_roles(role)
                descr = f"{after.mention} was given the afk role \n "
        elif str(before.status) == "idle":
            if str(after.status) == "online":
                role = discord.utils.get(after.guild.roles, name="afkers")
                await after.remove_roles(role)
                descr = f"{after.mention} was removed from the afk role \n "
        if before.roles != after.roles:
            beforeroles = [role.mention for role in before.roles]
            afterroles = [role.mention for role in after.roles]
            removedroles = list(set(beforeroles) - set(afterroles))
            addedroles = list(set(afterroles) - set(beforeroles))
            if len(removedroles) != 0:
                descr = f"The role {removedroles[0]} has been removed from {before.mention} "
                color = discord.Colour.red()
            elif len(addedroles) != 0:
                descr = f"The role {addedroles[0]} has been added to {before.mention} "
                color = discord.Colour.blue()
        embed = discord.Embed(
            title=f"{before}",
            description=descr,
            colour=color)
        now = before.created_at.now().strftime('%I:%M %p')
        embed.set_footer(text=f"User ID: {before.id} |{now}")
        await channel.send(embed=embed)

    @commands.Cog.listener() #prob merge user and member update? not much difference
    async def on_user_update(self, before, after):
        channel = self.bot.get_channel(config.LOGCHID)
        if before.avatar != after.avatar:
            embed = discord.Embed(
                title=f"Avatar update:", description=f"{after.mention}",
                colour=discord.Colour.from_rgb(248, 119, 238))
            embed.set_author(name=f"{after}", icon_url = f'{after.avatar_url}')
            embed.set_thumbnail(url = after.avatar_url)
            await channel.send(embed=embed)
        if before.name != after.name:
            embed = discord.Embed(
                title=f"Username update:", description=f"old username: {before.name} \n  new username: {after.name}",
                colour=discord.Colour.from_rgb(145, 233, 255))
            embed.set_author(name=f"{after}", icon_url = f'{after.avatar_url}')
            embed.set_thumbnail(url = after.avatar_url)
            await channel.send(embed=embed)
        if before.discriminator != after.discriminator:
            embed = discord.Embed(
                title=f"Discriminator Changed:",
                description=f"old discriminator: {before.discriminator} \n  new discriminator: {after.discriminator}",
                colour=discord.Colour.from_rgb(145, 233, 255))
            embed.set_author(name=f"{after}", icon_url = f'{after.avatar_url}')
            embed.set_thumbnail(url = after.avatar_url)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # print(reaction.emoji)
        if user.bot:
            return
        log_ch = config.LOGCHID
        channel = self.bot.get_channel(log_ch)
        embed = discord.Embed(
            title=f"React added",
            description=
            f"{user.name} added {reaction.emoji} to {reaction.message.id} !",
            colour=discord.Colour.from_rgb(25, 102, 182))
        await channel.send(embed=embed)
        if reaction.message.id not in self.react_msg_id:
            print("1")
            return
        if reaction.message.id in self.react_msg_id:
        # can change bottom for emoji in self.emoji, if emoji[] == str(reaction) #maybe also change self.emoji into dictionary
        #so you can make emoji: name dictionary pair
            if str(reaction) == '🥺':
                role = discord.utils.get(user.guild.roles, name="blink")
                await user.add_roles(role)
            if str(reaction) == '😳':
                role = discord.utils.get(user.guild.roles, name="Jisoo")
                await user.add_roles(role)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if user.bot:
            return
        log_ch = config.LOGCHID
        channel = self.bot.get_channel(log_ch)
        embed = discord.Embed(
            title=f"React removed",
            description=
            f"{user.name} removed {reaction.emoji} to {reaction.message.id} !",
            colour=discord.Colour.from_rgb(182, 22, 105))
        await channel.send(embed=embed)
        if reaction.message.id not in self.react_msg_id:
            return
        if reaction.message.id in self.react_msg_id:
            if str(reaction) == '🥺':
                role = discord.utils.get(user.guild.roles, name="blink")
                await user.remove_roles(role)
            if str(reaction) == '😳':
                role = discord.utils.get(user.guild.roles, name="Jisoo")
                await user.remove_roles(role)


    @commands.command()
    async def rolereact(self, ctx):
        embed = discord.Embed(
            title=f"Roles:",
            description=
            f":pleading_face:  blink \n :flushed:  Jisoo")
        message = await ctx.send(embed=embed)
        self.react_msg_id.append(message.id)
        for emoji in self.emojis:
            await message.add_reaction(emoji)

    # @commands.command(aliases=['h3'])
    # @commands.is_owner()
    # async def hug3(self, ctx, member: commands.MemberConverter = None):
    #     if member is None:
    #         await ctx.channel.send(f'I\'m here to give you a hug {ctx.author.mention}')
    #     else:
    #         await ctx.channel.send(f'{ctx.author.mention} gave you a hug {member.mention}')


def setup(bot):
    bot.add_cog(Listener(bot))
