# -*- coding: utf-8 -*-
"""
Created on Mon May 30 15:01:14 2022

@author: Potatsu
"""



import discord
import random
import asyncio
from discord.ext import commands
import nest_asyncio
nest_asyncio.apply()


#Keys
Token = 'OTYzMTI2ODI5MDg0OTg3NDcz.YlRjwg.MonSFXQq5mcKQhttsN7QGfm1Vwo'
Giphy_api_key = 'P9qw4uhc7VMND8hIsV8RHResufNRvPsi'
youtube_API = 'AIzaSyA90DCPaxXxl_n9sn13Kmt9igVyLJFgqgI'
client = commands.Bot(command_prefix='!')
bunny_gifs = ['https://media.giphy.com/media/ejIRH33RxAJl9Aumdf/giphy.gif', 'https://media.giphy.com/media/J4D9ZWn4zQlvOWIpiq/giphy.gif']
suzumiya = ['Haruhi Time']
singing_gifs = ['https://media.giphy.com/media/BQwu1mSFrgSBSAAHrf/giphy.gif', 'https://media.giphy.com/media/QRC0qUZ7uxQVHRJNCS/giphy.gif']
sing = ['Lets sing']
party_gifs = ['https://media.giphy.com/media/HnS4Y64oonm3C/giphy.gif', 'https://media.giphy.com/media/QRC0qUZ7uxQVHRJNCS/giphy.gif']
dance = ['Lets Dance']
punch_gifs = ['https://media.giphy.com/media/1Bgr0VaRnx3pCZbaJa/giphy.gif', 'https://media.giphy.com/media/S8nGEQ0yR8z6M/giphy.gif', 'https://media.giphy.com/media/DuVRadBbaX6A8/giphy.gif']
punch = ['Fuck you']
playlist = ['https://youtube.com/playlist?list=PL8lZieNFgOdmrNGTqwjqYJpJ_2nw_O_M2', 'https://youtube.com/playlist?list=PLOpYIT5ND76ILBX-Yxpo34Doqs8IpQfVH']
DJ = ['listen to some tunes']
#list for responses 
Responses = ['Yes ', 'No', 'Maybe','Bad Idea', 'Good Idea', 'Reroll',"Go get isekai'd  "]




class music(commands.Cog):
    def __init__(self, client):
        self.client = client

        def setup(client):
            client.add_Cog(music(client))

#Greeting in terminal
@client.event
async def on_ready():
    print('What is it {0.user}?'.format(client))
    
client = commands.Bot(command_prefix="!")    
client.run(Token)

