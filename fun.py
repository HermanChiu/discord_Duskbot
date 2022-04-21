import asyncio
import discord
import os
import random
import json
import requests
import time
import config
from discord.ext import commands, tasks
from io import BytesIO

# from dotenv import load_dotenv

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.morsedict = {'0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....',
                     '7': '--...', '8': '---..', '9': '----.', 'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..',
                     'e': '.',
                     'f': '..-.', 'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..', 'm': '--',
                     'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.', 's': '...', 't': '-', 'u': '..-',
                     'v': '...-', 'w': '.--', 'x': '-..-', 'y': '-.--', 'z': '--..', '!': '-.-.--', '@': '.--.-.',
                     '#': '#',
                     '$': '...-..-', '%': '%', '^': '^', '&': '.-...', '*': '*', '(': '-.--.', ')': '-.--.-',
                     '_': '..--.-',
                     '-': '-....-', '+': '.-.-.', '=': '-...-', '{': '{', '}': '}', '[': '[', ']': ']', '\\': '\\',
                     ':': '---...', ';': '-.-.-.', '\"': '.-..-.', '\'': '.----.', ',': '--..--', '.': '.-.-.-',
                     '/': '-..-.', '<': '<', '>': '>', '?': '..--..', '|': '|', ' ': ' '}
        self.decmorsedict = {'-----': '0', '.----': '1', '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6',
                     '--...': '7', '---..': '8', '----.': '9', '.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd',
                     '.': 'e', '..-.': 'f', '--.': 'g', '....': 'h', '..': 'i', '.---': 'j', '-.-': 'k',
                     '.-..': 'l', '--': 'm', '-.': 'n', '---': 'o', '.--.': 'p', '--.-': 'q', '.-.': 'r', '...': 's',
                     '-': 't', '..-': 'u', '...-': 'v', '.--': 'w', '-..-': 'x', '-.--': 'y', '--..': 'z',
                     '-.-.--': '!', '.--.-.': '@', '#': '#', '...-..-': '$', '%': '%', '^': '^', '.-...': '&',
                     '*': '*', '-.--.': '(', '-.--.-': ')', '..--.-': '_', '-....-': '-', '.-.-.': '+', '-...-': '=',
                     '{': '{', '}': '}', '[': '[', ']': ']', '\\': '\\', '---...': ':', '-.-.-.': ';', '.-..-.': '\"',
                     '.----.': '\'', '--..--': ',', '.-.-.-': '.', '-..-.': '/', '<': '<', '>': '>', '..--..': '?',
                     '|': '|', ' ': ''}

    @commands.command(aliases=['hai', 'hru'])
    async def hello(self, ctx):
        response = random.randrange(10)
        if response < 4:
            await ctx.channel.send('How are you?')
        elif response < 9:
            await ctx.channel.send('hello {}'.format(ctx.author.mention))
        else:
            await ctx.channel.send('Hello {0.user.mention}\'s MVP'.format(self))

    @commands.command()
    async def cookie(self, message):
        await message.channel.send('Here have a cookie :cookie:')

    @commands.command(aliases=['m8', '8ball'])
    async def magik8(self, ctx, *, message):
        mag8 = random.randint(0, 7)
        if mag8 == 1:
            await ctx.reply('Yes')
        elif mag8 == 2:
            await ctx.reply('No')
        elif mag8 == 3:
            await ctx.reply('100%')
        elif mag8 == 4:
            await ctx.reply('0%')
        elif mag8 == 5:
            await ctx.reply('Maybe')
        elif mag8 == 6:
            await ctx.reply('not too sure')
        else:
            await ctx.reply('Why are you asking me you know the answer')

    @magik8.error
    async def magik8_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            message = f"you are missing a question to ask the 8 ball"
            await ctx.channel.send(message)

            # show the different uses of ^ and v

    @commands.command(aliases=['st'])
    async def strikethrough(self, ctx, *, message):
        await ctx.channel.send(f'~~{message}~~')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')


    @commands.command(aliases=['bt'])
    async def bigtext(self, ctx, *, msg):
        msg = msg.lower()
        mylist = []
        numdict = {0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six',
                   7: 'seven', 8: 'eight', 9: 'nine',
                   }
        for char in msg:
            if (97 <= ord(char) <= 122):
                mylist.append(f':regional_indicator_{char}:')
            elif (48 <= ord(char) <= 57):
                mylist.append(f':{numdict[(ord(char) - 48)]}:')
            elif (ord(char) == 33):
                mylist.append(':exclamation:')
            elif (ord(char) == 32):
                mylist.append(' ')
            elif (ord(char) == 35):
                mylist.append(':hash:')
            elif (ord(char) == 42):
                mylist.append(':asterisk:')
            elif (ord(char) == 43):
                mylist.append(':heavy_plus_sign:')
            elif (ord(char) == 45):
                mylist.append(':heavy_minus_sign:')
            elif (ord(char) == 47):
                mylist.append(':heavy_division_sign:')
            else:
                mylist.append(':question:')
        print(mylist)
        msg2 = "".join(mylist)
        print(msg2)
        await ctx.channel.send(msg2)

    @commands.command(aliases=['mc', 't2mc']) #technically anon morse decode isnt needed, reg/anon morse is fine base decode is ok too
    async def morsecode(self, ctx, *, msg):
        msg = msg.lower()
        mylist = []

        for char in msg:
            mylist.append(f'{self.morsedict[char]} ')
        msg2 = "".join(mylist)
        await ctx.channel.send(msg2)

    @commands.command(aliases=['md', 'mc2t'])
    async def morsedecode(self, ctx, *, msg):
        msg = msg.lower()
        mylist = []

        msg = msg.split()
        print(msg)
        for elem in msg:
            if elem in self.decmorsedict:
                mylist.append(f'{self.decmorsedict[elem]} ')
            else:
                await ctx.channel.send(f'{elem} is an invalid sequence/letter')
                mylist.append('**?**')
        msg2 = "".join(mylist)
        await ctx.channel.send(msg2)

    @commands.command(aliases=['amc', 'anont2mc'])
    async def anonmorsecode(self, ctx, *, msg):
        await ctx.message.delete()
        msg = msg.lower()
        mylist = []
        for char in msg:
            mylist.append(f'{self.morsedict[char]} ')
        msg2 = "".join(mylist)
        await ctx.channel.send(msg2)

    @commands.command(aliases=['amd', 'anonmc2t'])
    async def anonmorsedecode(self, ctx, *, msg):
        await ctx.message.delete()
        msg = msg.lower()
        mylist = []
        msg = msg.split()
        print(msg)
        for elem in msg:
            mylist.append(f'{self.decmorsedict[elem]} ')
        msg2 = "".join(mylist)
        await ctx.channel.send(msg2)

    @commands.command(aliases=['ihatethisguy'])
    async def sosucks(self, ctx):
        await ctx.channel.send(
            'this bot sucks, but the person who made this bot sucks so much more')

    @commands.command(aliases=['hiddensend'])
    async def anonmsg(self, ctx, *, msg):
        # await ctx.channel.purge(limit=1) #issues with deleting stuff if msgs are sent inbetween
        await ctx.message.delete()
        await ctx.channel.send(f'{msg}')

    @commands.command(aliases=['c', 'choose'])
    async def choose4me(self, ctx, choice1, choice2, *args):  # *args?
        tuple1 = (choice1, choice2)
        tuple2 = args
        # if not tuple2:
        #  await ctx.channel.send(f'{tuple1[random.randrange(len(tuple1))]}')
        # else:
        tuple1 = tuple1 + tuple2
        await ctx.channel.send(f'{tuple1[random.randrange(len(tuple1))]}')

    # experimental
    # just to test if formating works on embeds
    # added member into function to get member avatar_url and to test how it works/ maybe try user next
    @commands.command(aliases=['ginfo'])
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def guildinfo(self, ctx):
        admin_roles = [role for role in ctx.guild.roles if role.permissions.administrator]
        # print(admin_roles) #print(type(admin_roles)) #print(type(admin_roles[0]))
        admins = []
        for role in admin_roles:
            for member in role.members:
                if not member.bot:
                    admins.append(member.mention)  # can just be member.name
        admins = list(dict.fromkeys(admins))
        admins = '\n'.join([elem for elem in admins])
        #
        num_mem = ctx.guild.member_count
        # print(f"list: {admins}")
        bot_list = [member.mention for member in ctx.guild.members if member.bot]

        # print(bot_list) print (discord.Colour.blue()) #print (discord.Colour.from_rgb(55, 72, 162)) #print (
        # discord.Colour.random())# test to show what it prints ( hex value if we want custom colors)
        embed = discord.Embed(title=f"__**Welcome to {ctx.guild.name}**__",
                              description=f"**Here's some stats about the server!!! :eyes:** ",
                              colour=discord.Colour.from_rgb(55, 72, 162))
        # try stuff e,g from_rgb(r,g,b)/.from_rgb(55, 72, 162) / .random(seed) / colour = 3748a2
        # test set_(feature),footer, image,thumbnail,author, field, and colour and the order of each added
        embed.set_footer(text=f"Guild ID : {ctx.guild.id} | Created at : {ctx.guild.created_at.date()}",
                         icon_url=config.FOOTER_IMG)
        embed.set_image(
            url=config.SERVER_IMG)  # same image but
        # https://i.pximg.net/img-master/img/2021/08/09/00/00/02/91828089_p0_master1200.jpg doesnt work prob bc no
        # access to site
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_author(name="author",
                         url=config.AUTHOR_IMG,
                         icon_url=config.AUTHOR_ICON)  # url here links to a website , icon will be scaled
        # down even if using big image?
        # test set_field_at and add_field
        # maybe test if there is a way to tag or list in fields the server owner is __ or admin/ mods are
        # maybe use fields for, for this contact __ for __  contact __
        embed.add_field(name="__Server owner__", value=f"{self.bot.get_user(ctx.guild.owner.id)}",
                        inline=False)  # {self.bot.get_user(ctx.guild.owner.id).mention}
        if not admins:  # if empty
            embed.add_field(name=" Admins", value=f"None", inline=True)
        else:  # if not empty
            embed.add_field(name=" Admins", value=f"{admins}", inline=True)
        embed.add_field(name="Members",
                        value=f"Total: {num_mem}\n Humans: {num_mem - len(bot_list)}\n Bots: {len(bot_list)}",
                        inline=True)
        embed.add_field(name=f"{len(bot_list)} Bots", value='\n'.join([elem for elem in bot_list]),
                        inline=True)  # f"{len(bot_list)} Bots"
        embed.add_field(name=" Channels",
                        value=f"Text Channels: {len(ctx.guild.text_channels)} \n Voice Channel: {len(ctx.guild.voice_channels)} ",
                        inline=False)
        # ^showing order matters only 3 fields per row shown? guild_owner = self.bot.get_user(ctx.guild.owner.id)
        # await ctx.channel.send(f'{guild_owner}') print (discord.bot.Guild.owner) was going to do this
        # https://stackoverflow.com/questions/65089714/how-do-i-list-users-with-roles-that-have-administrator
        # -privileges-in-an-embed-fo
        await ctx.channel.send(embed=embed)

    @guildinfo.error
    async def guildinfo_Error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.channel.send(
                f'Please do not spam this command(it gives the same thing mostly)\n You can only use this {error.cooldown.rate} time per {error.cooldown.per} secs, wait {int(error.retry_after)} secs')

    @commands.command(aliases=['uinfo'])
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def userinfo(self, ctx, member: commands.MemberConverter = None):
        if member == None:
            member = ctx.message.author
        mem_roles = [role.mention for role in member.roles]
        embed = discord.Embed(title=f"__**User: {member.name} \nDiscriminator: #{member.discriminator}**__",
                              description=f"**Some info on this user! :smiling_face_with_3_hearts: ** ",
                              colour=discord.Colour.from_rgb(218, 186, 242))
        # try stuff e,g from_rgb(r,g,b)/.from_rgb(55, 72, 162) / .random(seed) / colour = 3748a2
        # test set_(feature),footer, image,thumbnail,author, field, and colour and the order of each added
        embed.set_footer(text=f"Created account on: {member.created_at.date()}",
                         icon_url=config.FOOTER_ICON2)
        embed.set_thumbnail(url=member.avatar_url)

        embed.set_author(name="author",
                         url=config.AUTHOR_IMG,
                         icon_url=config.AUTHOR_ICON)
        embed.add_field(name="ID", value=f"{member.id}", inline=True)
        embed.add_field(name="Nickname", value=f"{member.nick}", inline=True)
        embed.add_field(name="Presence", value=f"{member.status}", inline=True)
        if (member.activity == None):
            embed.add_field(name="Game/Status", value=f"{member.activity}/No activity is shown", inline=True)
        elif (member.activity != None):
            if (member.activity.name == "Spotify"):
                embed.add_field(name="Game/Status",
                                value=f"{member.activity.name} listening to:"
                                      f" \n {member.activities[0].title} \n by {member.activities[0].artist} ",
                                inline=True)
            else:
                embed.add_field(name="Game/Status", value=f"{member.activity.name}", inline=True)
        embed.add_field(name="Mention", value=f"{member.mention}", inline=True)
        embed.add_field(name=f"Roles", value='\n'.join([elem for elem in mem_roles]),
                        inline=True)  # f"{len(bot_list)} Bots"
        embed.add_field(name="Joined server on", value=f"{member.joined_at}", inline=True)
        await ctx.channel.send(embed=embed)

    @userinfo.error
    async def userinfo_Error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.channel.send(
                f'Please do not spam this command(it gives the same thing mostly)\n You can only use this {error.cooldown.rate} time per {error.cooldown.per} secs, wait {int(error.retry_after)} secs')

    @commands.command(aliases=['sinfo', 'spotify'])
    @commands.cooldown(2, 20, commands.BucketType.user)
    async def spotifyinfo(self, ctx, member: commands.MemberConverter = None):
        member = ctx.author if member is None else member
        act_names = []
        sindex = -1
        song_duration = random.randint(0, 1)
        for ind in range(0, len(member.activities)):
            act_names.append(member.activities[ind].name)
            if (member.activities[ind].name == 'Spotify'):
                sindex = ind
        if (sindex == -1):
            await ctx.send(f'{member.name} is currently not listening to spotify')
            return
        embed = discord.Embed(title=f"__**Spotify Info for User: {member.name}#{member.discriminator}**__",
                              colour=member.activities[sindex].color)
        embed.set_footer(text=f"Member ID: {member.id}",
                         icon_url=config.FOOTER_ICON)
        embed.set_thumbnail(url=member.activities[sindex].album_cover_url)
        embed.add_field(name="Album & Song",
                        value=f"__**Album:**__ {member.activities[sindex].album}\n __**Song:**__ {member.activities[sindex].title}",
                        inline=True)
        embed.add_field(name="Artists", value=f"{member.activities[sindex].artist}", inline=True)
        embed.add_field(name="Song ID", value=f"{member.activities[sindex].track_id}", inline=True)
        dur = str(member.activities[sindex].duration).split(".")[0]
        embed.add_field(name="Song length", value=f"__{dur}__", inline=True)
        if song_duration == 0:
            current_time = member.activities[sindex].start.utcnow() - member.activities[sindex].start
            current_time = str(current_time).split(".")[0]
            embed.add_field(name="Currently at", value=f"__{current_time}__ Of __{dur}__", inline=True)
        else:
            remaining_time = member.activities[sindex].end - member.activities[sindex].end.utcnow()
            remaining_time = str(remaining_time).split(".")[0]
            embed.add_field(name="Remaining Song Time", value=f"__{remaining_time}__", inline=True)
        await ctx.send(embed=embed)

    @spotifyinfo.error
    async def spotify_Error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.channel.send(
                f'Do not spam commands\n You can use this {error.cooldown.rate} time per {error.cooldown.per} secs, wait {int(error.retry_after)} secs')

    @commands.command()
    async def hug(self, ctx, member: commands.MemberConverter = None):
        def check(m):
             return m.channel == ctx.channel
        #trying to make it so it accepts message author's replies only
        # def check(author):
        #     def inner_check(message):
        #         if message.author != author:
        #             return False
        #         try:
        #             int(message.content)
        #             return True
        #         except ValueError:
        #             return False
        #     return inner_check and author.channel == ctx.channel

        member = ctx.author if member is None else member
        await ctx.reply(f'Do you need a hug? {member.mention}')
        try:
            msg = await self.bot.wait_for('message', timeout=60.0, check=check)
        except:
            await ctx.send('you didnt respond :c', delete_after=60)
        if msg.content.lower().startswith(('yes', 'ya')):
            await ctx.send('https://c.tenor.com/OXCV_qL-V60AAAAC/mochi-peachcat-mochi.gif')
        elif msg.content.lower().startswith(('no', 'na')):
            await ctx.send('https://tenor.com/view/peach-cat-sad-lonely-heartbroken-gif-15230929')
        else:
            await ctx.send('what do you mean?')

    @commands.command()
    async def hug2(self, ctx, member: commands.MemberConverter = None):
        print(type(member))
        print(type(ctx.author))
        if member is None:
            await ctx.channel.send(f'I\'m here to give you a hug {ctx.author.mention}')
        elif member == ctx.author:
            await ctx.channel.send(f'weird.... {ctx.author.mention} is hugging themself')
        else:
            await ctx.channel.send(f'{ctx.author.mention} gave {member.mention} a hug')


def setup(bot):
    bot.add_cog(Fun(bot))
