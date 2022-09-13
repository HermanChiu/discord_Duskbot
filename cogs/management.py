import asyncio
import discord
import random
import config
import datetime
from discord.ext import commands, tasks
from discord.ext.commands import MissingPermissions
from io import BytesIO


# from dotenv import load_dotenv

class Management(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.react_msg_id = []
        self.emojis = ['🥺', '😳']
        self.logchid = 0
        self.onjoinchid = 0


    @commands.command()
    async def setgame(self, ctx, *, gamee):
        activity = discord.Game(name=gamee)
        await self.bot.change_presence(activity=activity)

    @commands.command(aliases=['p', 'prune'])
    async def purge(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.channel.send(
            f' ```\n{amount} messages deleted \nThis message will automatically delete in 10 seconds ```',
            delete_after=10
        )
        # not needed bc im dumb: https://discordpy.readthedocs.io/en/latest/api.html#discord.abc.Messageable.send
        # time.sleep(10)
        # await ctx.channel.purge(limit=1)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: commands.MemberConverter, *, reason=None):
        await member.kick(reason=reason)
        await ctx.channel.send(f'Get kicked, see you loser{member.mention}')

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            text = "Sorry {}, you do not have permissions kick anyone".format(ctx.message.author.mention)
            await ctx.channel.send(text)
        elif isinstance(error, commands.MissingRequiredArgument):
            message = f"Missing a required argument, please enter: \n !=kick <member>"
            await ctx.channel.send(message)
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(f'you entered an invalid member, make sure to enter a member after !=kick')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: commands.MemberConverter, *, reason=None):
        await member.ban(reason=reason)
        await ctx.channel.send(f'{member.mention} has been banned', delete_after = 5)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            text = "Sorry {}, you do not have permissions ban anyone".format(ctx.message.author.mention)
            await ctx.channel.send(text)
        elif isinstance(error, commands.MissingRequiredArgument):
            message = f"Missing a required argument, please enter: \n !=ban <member>"
            await ctx.channel.send(message)
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(f'you entered an invalid member, make sure to enter a member after !=ban')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member):
        if member.find('#') == -1: #if you cant find #
            await ctx.send(f'format is in correct, please enter: username#discriminator', delete_after = 10)
            return
        banned_list = await ctx.guild.bans()
        member_name,  member_discrim = member.split('#')
        print(member_discrim.isnumeric())
        print(not member_discrim)
        if(member_discrim.isnumeric() == False or not member_discrim or len(member_discrim) != 4):
            await ctx.send(f'discriminator is invalid/wrong format')
            return

        for banned in banned_list:
            user = banned.user
            if (user.name, user.discriminator) == (member_name, member_discrim):
                await ctx.guild.unban(user)
                await ctx.send(f'{user} has been unbanned', delete_after= 5)
                return
        #if member not found:
        await ctx.send(f'{member} is not found double check username and discriminator', delete_after=10)


    @commands.command(aliases=['frpl'])
    @commands.is_owner()
    async def flagplaylist(self, ctx):
        await ctx.channel.send('https://www.youtube.com/playlist?list=PLrUjznJcKqzFQ5w6WNs0Ikq-z78XIQp69')

    # maybe do a react for role bot using all things we learned before and use wait for command
    @commands.command()
    async def createbaseroles(self, ctx):
        guildroles = [role.name for role in ctx.guild.roles]
        # print(guildroles)#print(type(admin_roles)) #print(type(admin_roles[0])
        baseroles = ['rose', 'admin', 'str', 'luk', 'int', 'dex']
        createroles = list(set(baseroles) - set(guildroles))
        rolereactions = ['❤️', '🧡', '💛', '💚', '💙', '💜', '🤎', '🖤', '🤍']

        for rolenames in createroles:
            await ctx.guild.create_role(name=rolenames)
        await ctx.send(f'roles have been created, {len(createroles)} has been created', delete_after = 30)

    @commands.command(aliase=['ReactRoles'])
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def reactroles(self, ctx):
        valuelist = []
        baseroles = ['rose', 'admin', 'str', 'luk', 'int', 'dex']
        rolereactions = ['❤️', '🧡', '💛', '💚', '💙', '💜', '🤎', '🖤', '🤍']
        for ind in range(0, len(baseroles)):
            valuelist.append(rolereactions[ind] + baseroles[ind])
        embed = discord.Embed(
            title=f"React for 1 of the Roles:",
            description=
            '\n'.join([elem for elem in valuelist]))
        message = await ctx.send(embed=embed, delete_after=70)
        for ind in range(0, len(baseroles)):
            await message.add_reaction(rolereactions[ind])

        await ctx.send('pls react for a role', delete_after=60)

        def check(reaction, user):
            return user and reaction

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('no reaction detected ', delete_after=20)
        # can try to do
        for ind in range(0, min(len(baseroles), len(rolereactions))):
            if str(reaction) == rolereactions[ind]:
                print(rolereactions[ind])
                print(ind)
                role = discord.utils.get(ctx.guild.roles, name=baseroles[ind])
                await user.add_roles(role)
        # if str(reaction) == '❤️':
        #   role = discord.utils.get(ctx.guild.roles, name="rose")
        #   await user.add_roles(role)
        # if str(reaction) == '🧡':
        #   role = discord.utils.get(ctx.guild.roles, name="admin")
        #   await user.add_roles(role)
        # if str(reaction) == '💛':
        #   role = discord.utils.get(ctx.guild.roles, name="str")
        #   await user.add_roles(role)
        # if str(reaction) == '💚':
        #   role = discord.utils.get(ctx.guild.roles, name="luk")
        #   await user.add_roles(role)
        # if str(reaction) == '💙':
        #   role = discord.utils.get(ctx.guild.roles, name="int")
        #   await user.add_roles(role)
        # if str(reaction) == '💜':
        #   role = discord.utils.get(ctx.guild.roles, name="dex")
        #   await user.add_roles(role)
        await ctx.send(f'you have been given the role __**{role.name}**__', delete_after=60)

    @reactroles.error
    async def reactroles_Error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.channel.send(
                f'you can only get 1 role every 2mins, You can only use this {error.cooldown.rate} time per {error.cooldown.per} secs, wait {int(error.retry_after)} secs')

    @commands.command(aliases=['dm'])
    @commands.has_permissions(manage_guild=True)
    async def dm_send(self, ctx, member: commands.MemberConverter, *, content):
        if len(ctx.message.attachments) != 0:
            channel = await member.create_dm()
            await channel.send(f'{ctx.author.mention}: {content} {ctx.message.attachments[0]}')
            await ctx.send('message has been sent')
        else:
            channel = await member.create_dm()
            await channel.send(f'{ctx.author.mention}: {content}')
            await ctx.send('message has been sent')

    @dm_send.error
    async def dm_send_Error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(f'{error}', delete_after=10)

    @commands.command(aliases=['anondm'])
    @commands.is_owner()
    async def dm_Anon_send(self, ctx, member: commands.MemberConverter, *, content):
        await ctx.message.delete()
        channel = await member.create_dm()
        await channel.send(f' {content}')

    @dm_Anon_send.error
    async def dm_Anon_send_Error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(f'{error}', delete_after=10)

    @commands.command(aliases=['tts'])
    @commands.has_permissions(manage_guild=True)
    async def tts_msg(self, ctx, *, content):
        await ctx.message.delete()
        await ctx.send(f'{content}', tts=True, delete_after=10)



    @commands.command()
    @commands.has_permissions(administrator=True)
    async def createrole(self, ctx, name, repeat = 'no'):
        name = [name]
        if repeat.lower() == "yes":
            await ctx.guild.create_role(name=name[0])
            await ctx.send(f"__**{name[0]}**__ has been created", delete_after = 10)
        elif repeat.lower() == "no":
            guildroles = [role.name for role in ctx.guild.roles]
            newrole = list(set(name) - set(guildroles))
            if newrole == []:
                await ctx.send(f'__**{name[0]}**__ is already a role', delete_after = 10)
            else:
                await ctx.guild.create_role(name=name[0])
                await ctx.send(f"__**{name[0]}**__ has been created", delete_after = 10)
        else:
            await ctx.send("invalid repeat parameter", delete_after = 10)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def deleterole(self, ctx, role_name):
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role != None:
            await role.delete()
            await ctx.send(f"__**{role.name}**__ role has been deleted", delete_after = 10)
        else:
            await ctx.send("Role is not found", delete_after=10)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def giverole(self, ctx, role, member: commands.MemberConverter = None):
        member = ctx.author if member is None else member
        give_role = discord.utils.get(ctx.guild.roles, name=role)
        if(give_role == None):
            await ctx.send('role was not found in this server', delete_after =10)
        else:
            await member.add_roles(give_role)
            await ctx.send(f'{member.name} was given the role __**{give_role}**__', delete_after =10)
        await ctx.message.delete(delay=10)

    @giverole.error
    async def giveroles_Error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(f'This member is not in the server', delete_after=10)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def removerole(self, ctx, role, member: commands.MemberConverter = None):
        member = ctx.author if member is None else member
        taken_role = discord.utils.get(ctx.guild.roles, name=role)
        if(taken_role == None):
            await ctx.send('role was not found in this server', delete_after =10)
        else:
            await member.remove_roles(taken_role)
            await ctx.send(f'The role __**{taken_role}**__ was removed from {member.name} ', delete_after=10)
        await ctx.message.delete(delay=10)

    @removerole.error
    async def removeroles_Error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(f'This member is not in the server', delete_after = 10)

    @commands.command(aliases=['h3'])
    @commands.is_owner()
    async def hug3(self, ctx, member: commands.MemberConverter = None):
        if member is None:
            await ctx.channel.send(f'I\'m here to give you a hug {ctx.author.mention}')
        else:
            await ctx.channel.send(f'{ctx.author.mention} gave you a hug {member.mention}')


    @commands.command(aliases=['ainfo'])
    async def attachmentinfo(self, ctx):
        if len(ctx.message.attachments) != 0:
            for i in range(len(ctx.message.attachments)):
                await ctx.send(f"__**Attachment**__ #:{i+1} \n**name:** {ctx.message.attachments[i].filename} \n" +
                            f"**type:** {ctx.message.attachments[i].content_type} \n" +
                            f"**attachment id:** {ctx.message.attachments[i].id} \n" +
                            f"**proxy_URL:** {ctx.message.attachments[i].proxy_url} \n"+
                            f"**URL:** {ctx.message.attachments[i].url} \n"+
                            f"**images size:** {ctx.message.attachments[i].size} bytes \n" +
                            f"**images height:** {ctx.message.attachments[i].height} \n" +
                            f"**images width:** {ctx.message.attachments[i].width} \n")
                            # can use height width for ocr
        else:
            await ctx.send("No attachment found")

    ### add optional message id to find attachments info of said message

    @commands.command(aliases=['ginfo'])
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def guildinfo(self, ctx):
        admin_roles = [role for role in ctx.guild.roles if role.permissions.administrator]
        admins = []
        for role in admin_roles:
            for member in role.members:
                if not member.bot:
                    admins.append(member.mention)  # can just be member.name to avoid pings
        admins = list(dict.fromkeys(admins))
        admins = '\n'.join([elem for elem in admins])
        num_mem = ctx.guild.member_count
        bot_list = [member.mention for member in ctx.guild.members if member.bot]
        embed = discord.Embed(title=f"__**Welcome to {ctx.guild.name}**__",
                              description=f"**Here's some stats about the server!!! :eyes:** ",
                              colour=discord.Colour.from_rgb(55, 72, 162))
        embed.set_footer(text=f"Guild ID : {ctx.guild.id} | Created at : {ctx.guild.created_at.date()}",
                         icon_url=config.FOOTER_IMG)
        embed.set_image(url=config.SERVER_IMG)  # same image but
        # https://i.pximg.net/img-master/img/2021/08/09/00/00/02/91828089_p0_master1200.jpg doesnt work prob bc no
        # access to site
        embed.set_thumbnail(url=ctx.guild.icon)
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
        embed.set_footer(text=f"Created account on: {member.created_at.date()}",
                         icon_url=config.FOOTER_ICON2)
        embed.set_thumbnail(url=member.avatar.url)
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
        song_duration_msg = random.randint(0, 1)
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
        if song_duration_msg == 0:
            current_time = member.activities[sindex].start.now(tz=datetime.timezone.utc) - member.activities[sindex].start
            current_time = str(current_time).split(".")[0]
            embed.add_field(name="Currently at", value=f"__{current_time}__ Of __{dur}__", inline=True)
        else:
            remaining_time = member.activities[sindex].end - member.activities[sindex].end.now(tz=datetime.timezone.utc)
            remaining_time = str(remaining_time).split(".")[0]
            embed.add_field(name="Remaining Song Time", value=f"__{remaining_time}__", inline=True)
        await ctx.send(embed=embed)

    @spotifyinfo.error
    async def spotify_Error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.channel.send(
                f'Do not spam commands\n You can use this {error.cooldown.rate} time per {error.cooldown.per} secs, wait {int(error.retry_after)} secs')

    # dont ever use this ever especially if you change line 27 to offline(breaks replit maybe comp also)
    # @bot.command()
    # async def setstatus(ctx, *, response):
    #    response = response.lower()
    #    if response not in ['online', 'offline', 'idle', 'dnd', 'invisible']:
    #        await ctx.channel.send(
    #            'invalid reponse: \n please enter: online, offline, idle, dnd, invisible'
    #        )
    #    elif response == 'online':
    #        await bot.change_presence(status=discord.Status.online)
    #        print(f'{response}')
    #    elif response == 'offline':
    #        await bot.change_presence(status=discord.Status.offline)
    #       print(f'{response}')
    #    elif response == 'idle':
    #        await bot.change_presence(status=discord.Status.idle)
    #        print(f'{response}')
    #    elif response == 'dnd':
    #        await bot.change_presence(status=discord.Status.dnd)
    #        print(f'{response}')
    #    elif response == 'invisible':
    #        await bot.change_presence(status=discord.Status.invisible)
    #        print(f'{response}')

    # @bot.command(pass_context=True)
    # async def getguild(ctx):
    #    id = ctx.message.guild.id

    # cant use all commands only basic ones without mutliple param at least ones with convertors and custom classes
    # since args is just considered a string
    @commands.command(aliases=['t'])
    async def test(self, ctx, command, *, arg=None):
        print(ctx)
        print(command)
        print(arg)
        await ctx.invoke(self.bot.get_command(f'{command}'))


async def setup(bot):
    await bot.add_cog(Management(bot))
