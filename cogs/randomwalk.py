import discord
import os
import random
import matplotlib.pyplot as plt

from discord.ext import commands, tasks
from discord.ext.commands import MissingPermissions
from io import BytesIO

class Randomwalk(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.react_msg_id = []
        self.emojis = ['🥺', '😳']
        self.logchid = 0
        self.onjoinchid = 0

    @commands.command(aliases = ['rw'])
    @commands.has_permissions(administrator=True)
    async def randwalk(self, ctx, nSteps = 10, nWalks =5 , prob = .5):
        yfinal= 0
        if prob > 1 or prob < 0:
            await ctx.send('prob must be between 0 and 1')
            return
        if nSteps < 0 or nWalks < 0:
            await ctx.send("non-prob inputs should be greater than 1")
            return
        for i in range(nWalks):
            x = []
            y = []
            ypos = 0
            xpos = 0
            y.append(ypos)
            x.append(xpos)
            for z in range(nSteps):
                randval = random.random()
                if randval <= prob:
                    ypos = ypos + 1
                else:
                    ypos = ypos - 1
                y.append(ypos)
                xpos = z + 1
                x.append(xpos)
            yfinal = yfinal + ypos
            rwplot = plt.plot(x, y)
        yavg = yfinal/ nWalks
        #plt.show()
        plt.savefig('plot.png', dpi=300, bbox_inches='tight')
        with open('plot.png', 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file= picture)
            await ctx.send(f'{yavg} is the avg distance from moved away')
        plt.close()
        os.remove('plot.png')

    @commands.command(aliases = ['rw2'])
    @commands.has_permissions(administrator=True)
    async def randwalk2(self, ctx, nSteps=10, nWalks=5, stepdist =1.0 , stepsize =1, xyprob=.5, xpnprob = .5,ypnprob = .5):
        yfinal = 0.0
        xfinal = 0.0
        max_dist = 0.0
        max_dist_ind = 0
        if xyprob > 1 or xyprob < 0 or  xpnprob > 1 or xpnprob < 0 or  ypnprob > 1 or ypnprob < 0 :
            await ctx.send('prob must be between 0 and 1')
            return
        if nSteps < 0 or nWalks < 0 or stepsize < 0:
            await ctx.send("non-prob inputs should be greater than 1 besides stepdist")
            return
        for i in range(nWalks):
            x = []
            y = []
            ypos = 0.0
            xpos = 0.0
            y.append(ypos)
            x.append(xpos)
            for z1 in range(nSteps):  #for a specific walk
                for z2 in range(stepsize): #for each step
                    randxy = random.random() #random for x or y change
                    randypn = random.random() #random for positive or negative
                    randxpn = random.random()
                    if randxy <= xyprob:
                        if randxpn <= xpnprob:
                            xpos = xpos + stepdist
                        else:
                            xpos = xpos - stepdist
                    else:
                        if randypn <= ypnprob:
                            ypos = ypos + stepdist
                        else:
                            ypos = ypos - stepdist
                y.append(ypos)
                x.append(xpos)
            dist = (xpos**2 + ypos**2)**0.5
            print(f'dist ={dist}, walk#: {i}')
            if (dist > max_dist):
                max_dist= dist
                max_dist_ind = i
                coord = (xpos, ypos)
                print(f'dist ={dist}, walk#: {max_dist_ind}')
            yfinal = yfinal + ypos
            xfinal = xfinal + xpos
            rwplot = plt.plot(x, y)
        yavg = yfinal / nWalks
        xavg = xfinal / nWalks
        plt.grid()
        ax = plt.gca()
        ax.spines['top'].set_color('none')
        ax.spines['left'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_position('zero')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        plt.savefig('plot.png', dpi=300, bbox_inches='tight')
        with open('plot.png', 'rb') as f:
            picture = discord.File(f)
            await ctx.send(f'''avg coordinates values are ({xavg},{yavg})\nthe furthest walk is walk #{max_dist_ind} with a distance of {max_dist} at {coord}''',file=picture )
        plt.close()
        os.remove('plot.png')

#try making scatter plot version for heat map?
    # @commands.command(aliases = ['rw5'])
    # @commands.has_permissions(administrator=True)
    # async def randwalk5(self, ctx, nSteps=10, nWalks=5, stepdist =1.0 , stepsize =1, xyprob=.5, xpnprob = .5,ypnprob = .5):
    #     yfinal = 0.0
    #     xfinal = 0.0
    #     max_dist = 0.0
    #     max_dist_ind = 0
    #     if xyprob > 1 or xyprob < 0 or  xpnprob > 1 or xpnprob < 0 or  ypnprob > 1 or ypnprob < 0 :
    #         await ctx.send('prob must be between 0 and 1')
    #         return
    #     if nSteps < 0 or nWalks < 0 or stepsize < 0:
    #         await ctx.send("non-prob inputs should be greater than 1 besides stepdist")
    #         return
    #     for i in range(nWalks):
    #         x = []
    #         y = []
    #         ypos = 0.0
    #         xpos = 0.0
    #         # y.append(ypos)
    #         # x.append(xpos)
    #         for z1 in range(nSteps):  #for a specific walk
    #             for z2 in range(stepsize): #for each step
    #                 randxy = random.random() #random for x or y change
    #                 randypn = random.random() #random for positive or negative
    #                 randxpn = random.random()
    #                 if randxy <= xyprob:
    #                     if randxpn <= xpnprob:
    #                         xpos = xpos + stepdist
    #                     else:
    #                         xpos = xpos - stepdist
    #                 else:
    #                     if randypn <= ypnprob:
    #                         ypos = ypos + stepdist
    #                     else:
    #                         ypos = ypos - stepdist
    #         y.append(ypos)
    #         x.append(xpos)
    #         dist = (xpos**2 + ypos**2)**0.5
    #         if (dist > max_dist):
    #             max_dist= dist
    #             max_dist_ind = i
    #             coord = (xpos, ypos)
    #             print(f'dist ={dist}, walk#: {max_dist_ind}')
    #         yfinal = yfinal + ypos
    #         xfinal = xfinal + xpos
    #     rwplot = plt.scatter(x, y, c =x)
    #     yavg = yfinal / nWalks
    #     xavg = xfinal / nWalks
    #     # plt.show()
    #     #plt.ylim(-2.2*(1-ypnprob)*(2* stepsize* nSteps)**0.5 - .2*nSteps, 2.2*ypnprob *(2* stepsize* nSteps)**0.5 + .2*nSteps)
    #     #plt.xlim(-2.2*(1-ypnprob)*(2* stepsize* nSteps)**0.5 - .2*nSteps, 2.2*ypnprob *(2* stepsize* nSteps)**0.5 + .2*nSteps)
    #     #need to maybe figure out if we can do it if the x/yprob is not .5
    #     plt.grid()
    #     ax = plt.gca()
    #     ax.spines['top'].set_color('none')
    #     ax.spines['left'].set_position('zero')
    #     ax.spines['right'].set_color('none')
    #     ax.spines['bottom'].set_position('zero')
    #     ax.xaxis.set_ticks_position('bottom')
    #     ax.yaxis.set_ticks_position('left')
    #     plt.savefig('plot.png', dpi=300, bbox_inches='tight')
    #     with open('plot.png', 'rb') as f:
    #         picture = discord.File(f)
    #         await ctx.send(file=picture)
    #         await ctx.send(f'avg coordinates values are ({xavg},{yavg})')
    #         await ctx.send(f'the furthest walk is walk #{max_dist_ind} with a distance of {max_dist} at {coord}')
    #     plt.close()
    #     os.remove('plot.png')
    #     #maybe add a max distance value using a^2 + b^2 = c^2 or d = (xpos^2 + ypos^2)^0.5/equivalent syntax for python

async def setup(bot):
    await bot.add_cog(Randomwalk(bot))