import asyncio
import discord
from discord import role
from discord import message
from discord import channel
from discord.ext import commands
from discord import embeds
import datetime
import os
import json
import random
from discord.utils import get
from PIL import Image, ImageFont, ImageDraw
import time

welcome_channel_id = "welcome channel id here" #remove ""
verify_channel_id = "verification channel id here" #remove ""
role_name = "role name here"

class Test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open ('codes.json', 'r') as f:
            data = json.load(f)

        guild = member.guild
        channel = self.client.get_channel(int(welcome_channel_id))
        if not member.bot:
                
            embed = discord.Embed(
                title="Welcome",
                description=f"Hey {member.mention},\nwelcome to {member.guild.name}"
                )
            embed.set_thumbnail(url=member.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            await channel.send(embed=embed)
                
            random_int=random.randrange(start=10000, stop=99999)
            data[str(member.id)] = str(random_int)

            with open ('codes.json', 'w') as f:
                json.dump(data, f, indent=4)


            img_bg = Image.open('bg.png').convert('RGB')
            font = ImageFont.truetype('arial.ttf', 60)
            draw = ImageDraw.Draw(img_bg)

            draw.text((62,39), str(random_int), font=font, fill='#b57d86')
            img_bg.save(f'{member.id}.png')


            file = discord.File(f'{member.id}.png', filename=f'{member.id}.png')

            embed2 = discord.Embed(
                title = "Welcome!",
                description=f"Hey,\n welcome to **{guild.name}**!\n\nPlease complete the verification. Under this message you can see an image with a code. Send `&verify [code]` in a channel, you are able to send messages to.\n\nPlease do not forget to remove [] while typing in the command!"
            )
            embed2.timestamp = datetime.datetime.utcnow()
            embed2.set_image(url=f'attachment://{member.id}.png')
            await member.send(embed=embed2, file=file)

            time.sleep(5)
            os.remove(f'{member.id}.png')

    @commands.command()
    async def verify(self, ctx, code):
        with open('codes.json', 'r') as f:
            data = json.load(f)
        if ctx.channel.id == verify_channel_id:
            if not code == None:
                if str(ctx.message.author.id) in data:
                    if str(code) == data[str(ctx.message.author.id)]:
                        await ctx.channel.purge(limit=1)
                        role1 = get(ctx.guild.roles, name=role_name)
                        await ctx.message.author.add_roles(role1)
                        
                        data.pop(str(ctx.message.author.id))
                        with open('codes.json', 'w') as f:
                            json.dump(data, f, indent=4)

                    else: pass
                else: pass
            else: pass
        else: pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        with open('codes.json', 'r') as f:
            data = json.load(f)
        if str(member.id) in data:
            data.pop(str(member.id))
            with open('codes.json', 'w') as f:
                json.dump(data, f, indent=4)

        
            

def setup(client):
    client.add_cog(Test(client))