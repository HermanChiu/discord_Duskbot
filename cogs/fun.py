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
        reply_msgs = {0: 'Yes', 1: 'No', 2: '100%', 3: '0%', 4: 'Maybe', 5: 'not too sure',
         6: 'Why are you asking me you know the answer :rolling_eyes:', 7: 'Try again',
         8: 'Ask me later :sleeping:', 9: 'Most likely', 10: 'Probably not', 
         11: 'This question is too complex', 12: 'Duh',13: 'Nuh-uh'}
        print(len(reply_msgs))
        mag8 = random.randint(0, len(reply_msgs))
        await ctx.reply(reply_msgs[mag8])

    @magik8.error
    async def magik8_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            message = f"you are missing a question to ask the 8 ball"
            await ctx.channel.send(message)

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
        numdict = {48: 'zero', 49: 'one', 50: 'two', 51: 'three', 52: 'four', 53: 'five', 54: 'six',
                   55: 'seven', 56: 'eight', 57: 'nine',
                   }
        asciidict = { 32: ' ', 33: ':exclamation:', 35: ':hash:', 42: ':asterisk:',
                     43: ':heavy_plus_sign:', 45: ':heavy_minus_sign:', 47: ':heavy_division_sign:',
                   }           
        for char in msg:
            if (97 <= ord(char) <= 122): # letters
                mylist.append(f':regional_indicator_{char}:')
            elif (48 <= ord(char) <= 57): # numbers
                mylist.append(f':{numdict[(ord(char))]}:')
            elif(ord(char) in asciidict.keys()): #chars that have emojis
                mylist.append(asciidict[ord(char)])
            else:
                mylist.append(':question:')
        msg2 = "".join(mylist)
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
        await ctx.message.delete()
        await ctx.channel.send(f'{msg}')

    @commands.command(aliases=['c', 'choose'])
    async def choose4me(self, ctx, choice1, choice2, *args):  # *args?
        tuple1 = (choice1, choice2)
        tuple2 = args
        tuple1 = tuple1 + tuple2
        await ctx.channel.send(f'{tuple1[random.randrange(len(tuple1))]}')

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
            await ctx.send('what do you mean?', delete_after=10)

    @commands.command()
    async def hug2(self, ctx, member: commands.MemberConverter = None):
        if member is None:
            await ctx.channel.send(f'I\'m here to give you a hug {ctx.author.mention}')
        elif member == ctx.author:
            await ctx.channel.send(f'weird.... {ctx.author.mention} is hugging themself')
        else:
            await ctx.channel.send(f'{ctx.author.mention} gave {member.mention} a hug')


async def setup(bot):
    await bot.add_cog(Fun(bot))
