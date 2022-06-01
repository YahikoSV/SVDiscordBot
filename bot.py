# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 22:23:16 2020

@author: Potatsu
"""

# bot.py
import os
import random

import discord
from discord.ext import tasks, commands
from itertools import cycle
from dotenv import load_dotenv

import requests
import random as rand
from bs4 import BeautifulSoup as bs
from itertools import permutations

import nest_asyncio
import asyncio
#nest_asyncio.apply()

from flask import Flask
from threading import Thread
import urllib.request
import json

#from textblob import TextBlob  #got issues
import deep_translator as dt
import detectlanguage as dlang
import pyshorteners as sh
import pandas as pd

dlang.configuration.api_key = 'ca91cd9ad76ce61ebde42e41d801b652'
result = dlang.detect("Buenos dias señor")

app = Flask('')


@app.route('/')
def main():
    return "Your Bot Is Ready"


def run():
    app.run(host="0.0.0.0", port=8000)


def keep_alive():
    server = Thread(target=run)
    server.start()


load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='~', case_insensitive=True, intents=intents)
status = cycle(['with Python', 'MikoHub'])


@bot.event
async def on_ready():
    activity = discord.Game(name="~help", type=3)
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print(f'{bot.user.name} has connected to Discord!')


@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


################### Bot Commands  ######################


# @bot.event
# async def on_member_join(member):
#     await member.create_dm()
#     await member.dm_channel.send(
#         f'Hi {member.name}, welcome to the Discord server! FAQ!'
#     )

@bot.command(name='fbkcat', help='Responds with a random quote from Fubuki')
async def Fubuki_Cat(ctx):
    Fubuki_quotes = [
        'No no cat! I\'m Fox', 
        'Kitsune jyaa!', 
        'Nyaajyanee yo!'
    ]
    response = random.choice(Fubuki_quotes)
    await ctx.send(response)
    
    
@bot.command(name='dl', help='Returns SV Portal link from deckcode')
async def svcodetostatic(ctx, deck_code, lang='en', mode='u'):
    
    response, valid_input = createlinkfromcode(deck_code, lang, mode)
    await ctx.send(response)
    
    
@bot.command(name='db', help='Turns SV builder links into static links')
async def svbuildtostatic(ctx, link, lang='en', mode='u'):

    response, valid_input = createlinkfrombuilder(link, lang, mode)
    await ctx.send(response)


@bot.command(name='mull', help='Test out a mulligan')
async def openingmull(ctx, deck_code, lang='en', mode='u'):
    
    response, valid_input = createlinkfromcode(deck_code, lang, mode)
    
    if valid_input == False:
            await ctx.send(response)
    else:
       
        card_list = decklist(response)     
        draw_count = 3
        time_out = False
        while time_out == False:
            author = ctx.author.name
            txt_response =  f"**{author}**, choose cards that you want to mulligan."
            await ctx.send(txt_response)
            opening_hand = rand.sample(card_list,draw_count)
            description = f' Ooo {opening_hand[0]}\n \
                             oOo {opening_hand[1]}\n \
                             ooO {opening_hand[2]}'
                             
            embed_response = discord.Embed(title="Opening Hand", description = description, color=0xffb7c5)
            embed_response.set_footer(text='x = mull, o = keep (eg. xox, oxx, ooo)')
            await ctx.send(embed=embed_response) 
    
            
            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel
            
            valid_mull = False
            while valid_mull == False:
                try:
                    msg = await bot.wait_for("message", check=check, timeout=60)
                    opening_hand, valid_mull = mulliganfunction(ctx, msg.content, card_list, opening_hand, valid_mull)
                except asyncio.TimeoutError:
                    await ctx.send(f"**{author}**, Time's up! (Mulligan Ended)")
                    valid_mull = True
                    time_out = True
                
                if valid_mull == False:
                    await ctx.send(f"**{author}**, Invalid Mulligan please enter a valid mulligan (eg. oxo, xoo, xxx)")
                
            if time_out == False:
                description = f' {opening_hand[0]}\n \
                                 {opening_hand[1]}\n \
                                 {opening_hand[2]}'
                embed_response = discord.Embed(title="Final Hand", description = description, color=0x92ddf7)
                embed_response.set_footer(text='Try Again? (Enter y if yes): ')
                await ctx.send(embed=embed_response)
                
                try:
                    msg = await bot.wait_for("message", check=check, timeout=10)
                    if msg.content.lower() == "y":
                        continue
                    else:
                        await ctx.send(f"**{author}**, Mulligan Ended")
                        break
                except asyncio.TimeoutError:
                    await ctx.send(f"**{author}**, Time's up! (Mulligan Ended)")
                    break

bot.remove_command('help')            
@bot.command(name='help')
async def help(ctx):
    
    author = ctx.message.author
    
    embed1 = discord.Embed(color = discord.Color.orange())
    embed1.set_author(name='SV FAQ Bot Commands \n')
    embed1.add_field(name="__dl <code> <lang> <mode>__",
                    value="Transforms deckcode into SV Portal link. \n\n",
                    inline=False
                    )
        
    embed1.add_field(name="__dbtdl <builder_link> <lang> <mode>__",
                    value="Transforms deck builder link into SV Portal link. \n\n",
                    inline=False
                    )
        
    embed1.add_field(name="__mull <code> <lang> <mode>__",
                    value="Mulligan Simulator with the given deck code. \n\n",
                    inline=False
                    )    
    
    embed1.add_field(name="Parameters:",
                    value="deck_code: 4 character deck_code \n \
                    language: Options: {'en'(default), 'ja', 'ko', 'zh-tw' , 'fr', 'it', 'de', 'es'}  \n \
                    mode: Rotation, Unlimited {'r', 'u' (default)} \n\n \
                    Choose which cards you want to mull based on their positions with...\n \
                    x: Mull card, o: Keep card (e.g. xxo, oxo) \n\n",
                    inline=False
                    )         
        
    embed2 = discord.Embed(color = discord.Color.blue())
    embed2.set_author(name='Other Commands (for testing) \n')
    embed2.add_field(name="__fbkcat__",
                    value="Responses with a random quote of what Fubuki would say \n \
                          Try out what quote you got hehehe",
                    inline=False
                    ) 

    embed2.add_field(name="__greet__",
                    value="Alice greets you",
                    inline=False
                    )

    embed2.add_field(name="__about__",
                    value="About Alice Bot",
                    inline=False
                    )
    
    await author.send(embed=embed1)
    await author.send(embed=embed2)


# @bot.event
# async def on_message(message):
#     # No infinite bot loops
#     if message.author == bot.user or message.author.bot:
#         return

#     if message.content == 'great':
#         mention = message.author.mention
#         response = f"hey {mention}, you're great!"
#         await message.channel.send(response)

# @bot.event
# async def on_message2(message):
#     if message.content.startswith('$greet'):
#         channel = message.channel
#         await channel.send('Say hello!')

#         def check(m):
#             return m.content == 'hello' and m.channel == channel

#         msg = await bot.wait_for('message', check=check)
#         await channel.send('Hello {.author}!'.format(msg))
        
@bot.command(name='greet')
async def on_message3(ctx):
    # No infinite bot loops
    if ctx.author == bot.user or ctx.author.bot:
        return

    mention = ctx.author.name
    response = f"Hi {mention}!"
    await ctx.channel.send(response)
    
    
@bot.command(name='about')
async def about(ctx):
    author = ctx.message.author
    embed1 = discord.Embed(color = discord.Color.orange())
    embed1.set_author(name='SV FAQ Bot Commands \n')
    embed1.add_field(name="__dl <code> <lang> <mode>__",
                    value="Transforms deckcode into SV Portal link. \n\n",
                    inline=False
                    )
    await author.send(embed=embed1)
   
 
@bot.command(name='arg1')
async def arg1(ctx, *args):
    await ctx.send(" ".join(args[:]))
    # args contains all arguments written after the command i.e !game game i want to play
    # print(" ".join(args[:])) will print "game i want to play"

   
@bot.command(name='card')
async def searchcard(ctx, *args):
    
    #author = ctx.message.author
    
    
    #Search Function
    chosen_lang = False
    add_chosen_lang = 'lang=en'
    for i in range(0,len(args)):
        if 'lang=' in args[i] :
            add_chosen_lang = args[i]
            args = args[:i] + args[i+1:]
            chosen_lang = True
       
        
    
    
    card_name = " ".join(args[:]) #not 5b

    
    # if len(card_name) >= 3:
    #     blob = TextBlob(card_name).detect_language()
    #     languages = ['en', 'ja', 'ko', 'zh-tw' , 'fr', 'it', 'de', 'es']    
    #     if blob.lower() in languages:
    #         d_lang = blob
    #     elif blob.lower() == 'fy':
    #         d_lang = 'de'
    #     else:
    #         d_lang = 'en'        
    #     add_lang = f'lang={d_lang}'
    # else:
    #     add_lang = add_chosen_lang
    
#    if chosen_lang == True:
#        add_lang =  add_chosen_lang
    if len(card_name) >= 3:
        try:
            result = dlang.detect(card_name)[0]['language']
            languages = ['en', 'ja', 'ko', 'zh-tw' , 'fr', 'it', 'de', 'es']  
            if result.lower() in languages:
                d_lang = result
            elif result.lower() == 'zh-Hant':
                d_lang = 'zh-tw'
            elif result.lower() == 'fy':
                d_lang = 'de'
            else: 
                d_lang = 'en'
            add_lang = f'lang={d_lang}'
        except: 
            add_lang = add_chosen_lang  
    else:
        add_lang = add_chosen_lang        
    
    dict_filters = {
                      'card_name'   : 'card_name' 
                     ,'card_clan'   : 'clan%5B%5D'
                     ,'sv_format'   : 'format'
                     ,'card_set'    : 'card_set%5B%5D'
                     ,'card_cost'   : 'cost%5B%5D'
                     ,'card_type'   : 'char_type%5B%5D'
                     ,'card_rarity' : 'rarity%5B%5D'
                     ,'language'    : 'lang'
                   }
    
    dict_set_acro =   {
                      '23' : 'EOP'
                    , '22' : 'DOC'
                    , '21' : 'RSC' 
                    , '20' : 'DOV'
                    , '19' : 'ETA'
                    , '18' : 'SOR' 
                    , '17' : 'FOH'
                    , '16' : 'WUP'
                    , '15' : 'UCL'
                    , '14' : 'VEC'
                    , '13' : 'ROG'
                    , '12' : 'STR'
                    , '11' : 'ALT'
                    , '10' : 'OOT' 
                    , '09' : 'BOS'
                    , '08' : 'DBN'
                    , '07' : 'CGS'
                    , '06' : 'SFL' 
                    , '05' : 'WLD' 
                    , '04' : 'TOG'
                    , '03' : 'ROB'
                    , '02' : 'DRK' 
                    , '01' : 'CLC'
                    , '00' : 'Basic'   
                    }    
    
    
    initial_link = 'https://shadowverse-portal.com/cards?'   
    added_filters = [] 
    #Add Card Name                 }
    add_card_name = dict_filters['card_name'] + '=' + card_name
    add_card_name = add_card_name.replace(' ', '+')
    added_filters.append(add_card_name)
    
    #Add Lang Name
    #add_lang = dict_filters['language'] + '=' + language
    added_filters.append(add_lang) 
    
    added_link = '&'.join(added_filters)
    
    
    count = 0
    increment = 12
    move_button = ''    
    while move_button in ['N','B'] or count == 0:
        
        if move_button == 'B' and  count % increment  == 0:
            count = count - increment * 2
        elif move_button == 'B' and  count % increment  != 0:
            count = count - count % increment  - increment     
    
        card_offset = '&card_offset=' + str(count) 
            
        full_link = initial_link + added_link + card_offset
        source = requests.get(full_link).text
        soup = bs(source, 'lxml')
        
        card_list = soup.find_all('a', class_="el-card-visual-content")
        
        
        if len(card_list) == 0:
            msg_no_result = 'No result found'
            chosen_card_number = False
            await ctx.send(msg_no_result)
            break
        
        if len(card_list) == 1 and count == 0:
            chosen_card_number = card_list[0]['href'].split('/')[2]        
            break
        
        right_ans = ['N', 'B', 'Q']
        embed_desc = ''
        for i in range (1,len(card_list)+1):
            count += 1
            card_title = card_list[i-1].find('img')['alt']
            card_number = card_list[i-1]['href'].split('/')[2]
            
            if  card_number[0] == '7':
                expac_acro = '[alt]'
            else:
                expac_acro = f'[{dict_set_acro[card_number[1:3]]}]'
            #print(str(count) + '.) ' + card_title + ' ' + expac_acro)
            embed_desc = embed_desc + str(count) + '.) ' + card_title + ' ' + expac_acro + '\n'
            right_ans.append(str(count))
        embed_footer = '## - Choose card, N - next page, B - prev page, Q - quit'
        

        time_out = False
        while time_out == False:
            author = ctx.author.name
            txt_response =  f"**{author}**, did you mean..."
            await ctx.send(txt_response)
                           
            embed_response = discord.Embed(title="Search Results", description = embed_desc, color=0xffb7c5)
            embed_response.set_footer(text=embed_footer)
            await ctx.send(embed=embed_response)         

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel
            
            valid_ans = False
            while valid_ans == False:
                try:
                    msg = await bot.wait_for("message", check=check, timeout=10)
                    
                    if msg.content in right_ans:
                        move_button = msg.content
                        valid_ans = True
                        time_out = True
                        chosen_card_number = False

                except asyncio.TimeoutError:
                    await ctx.send(f"**{author}**, Time's up!")
                    valid_ans = True
                    time_out = True
                    chosen_card_number = False
                
                if valid_ans == False:
                    await ctx.send(f"**{author}**, Invalid Response")
        
        
        #move_button = input('## - Choose card, N - next page, B - prev page, Q - quit = ')

    
        if move_button.isnumeric() == True and int(move_button) in range(count - len(card_list) + 1, count + 1):
            chosen_card_number = card_list[(int(move_button) % increment) - 1]['href'].split('/')[2] 
        else:
            chosen_card_number = False
    
    #if query == '1':
    #    chosen_card_number = '110124010'    
    #else:
    #    chosen_card_number = '120541010' 
           
    if chosen_card_number is not False:
        add_lang = add_chosen_lang if chosen_lang == True else add_lang
        chosen_card_link = f'https://shadowverse-portal.com/card/{chosen_card_number}?{add_lang}'
        source = requests.get(chosen_card_link).text
        soup = bs(source, 'lxml')
        
        card_info   = soup.find('ul', class_="card-info-content")
        card_text   = card_info.find_all('span')
        p_text      = card_info.find_all('p')
        
        trait     = card_text[1].text.split('\r\n')[1]
        class_    = card_text[3].text.split('\r\n')[1]
        rarity    = card_text[5].text.split('\r\n')[1]
        create    = card_text[7].text.split('\r\n')[1]
        if chosen_card_number[0] != '7' and chosen_card_number[1:3] != '00':
            liquefy   = f'{p_text[0].text} / ' + p_text[1].text.split("\n")[2] 
            card_pack = card_text[11].text.split('\r\n')[1]
        
        if add_lang == 'lang=ja':
            title = soup.find_all('li', class_="bl-breadcrumb-content-list")[2].text
        else:
            title = soup.find('h1', class_="card-main-title").text.split('\r\n')[1]

        embed1 = discord.Embed(  title = title
                                ,url   = chosen_card_link
                                ,color = discord.Color.orange())
                
        flavor = soup.find('p', class_="card-content-description").text    
        
        if int(chosen_card_number[-4]) == 1: #follower
        
        
            skill_txt = soup.find_all('p', class_="card-content-skill")        
            if skill_txt[0].text == '\n':
                skill_u = 'None'
            else:
                skill_u = str(skill_txt[0]).split('>',1)[1].split('</p>',1)[0].split('\r\n')[-2]        
    
            if skill_txt[1].text == '\n':
                skill_e = 'None'
            else:
                skill_e = str(skill_txt[1]).split('>',1)[1].split('</p>',1)[0].split('\r\n')[-2]       
                
            skill_u = clean_text_1(skill_u)
            skill_e = clean_text_1(skill_e)
            lang_unevo= soup.find_all('p', class_="el-label-card-state l-inline-block")[0].text.split('\r\n')[1]
            lang_evo  = soup.find_all('p', class_="el-label-card-state l-inline-block")[1].text.split('\r\n')[1]
            atk_unevo = soup.find_all('p', class_="el-card-status is-atk")[0].text.split('\r\n')[1]
            atk_evo   = soup.find_all('p', class_="el-card-status is-atk")[1].text.split('\r\n')[1]
            life_unevo= soup.find_all('p', class_="el-card-status is-life")[0].text.split('\r\n')[1]
            life_evo  = soup.find_all('p', class_="el-card-status is-life")[1].text.split('\r\n')[1]

            embed1.add_field(name=f'{lang_unevo}: {atk_unevo}/{life_unevo}',
                             value=f'{skill_u}',
                             inline=False
                             )       
            embed1.add_field(name=f'{lang_evo}: {atk_evo}/{life_evo}',
                             value=f'{skill_e}',
                             inline=False
                             )
        else: #non-follower
            skill = str(soup.find_all('p', class_="card-content-skill")[0]).split('>',1)[1].split('</p>',1)[0].split('\r\n')[1]
            skill = clean_text_1(skill)
            embed1.add_field(name='Effect:',
                             value=f'{skill}',
                             inline=False
                             )
        

        #embed1.set_author(name='SV FAQ Bot Commands \n')
        #embed1.add_field(name="__dl <code> <lang> <mode>__",
        #            value="Transforms deckcode into SV Portal link. \n\n",
        #            inline=False
        #            )
        #embed1.add_field(name='Effect:',
        #                 value=f'{skill} \n {flavor}')
        

        embed1.set_image(url=f"https://svgdb.me/assets/cards/en/C_{chosen_card_number}.png")    #the image itself
        #embed1.set_footer(text='Yahiko#1354',icon_url="https://cdn.discordapp.com/attachments/84319995256905728/252292324967710721/embed.png")   #image in icon_url
        #embed1.set_thumbnail(url="https://cdn.discordapp.com/attachments/84319995256905728/252292324967710721/embed.png") #image itself   
        
        #await author.send(embed=embed1)
        await ctx.send(embed=embed1)
        
        
        
@bot.command(name='t2')
async def t2deck_stats(ctx, deck_code):
    list_classes = ['Forest', 'Sword', 'Rune', 'Dragon' ,'Necro' ,'Blood', 'Haven', 'Portal']
    
    response, valid_input = createlinkfromcode(deck_code, lang='ja', mode='t')
    
    if valid_input == False:
        await ctx.send(response)
    else:
        short = sh.Shortener()
        #draft_link = short.tinyurl.short(response)
               
        draft_list = decklist_t2(response)
        draft_class = list_classes[int(response[38])-1]

        deck_cardList = pd.DataFrame(draft_list, columns=['JP Name'])
        score_class = pd.read_excel(io='take_2_scores.xlsx', sheet_name=draft_class).drop(labels='Unnamed: 0', axis=1)

        result = pd.merge(deck_cardList, score_class, how='inner', on=['JP Name'])
        result_mean   = result.mean()
        result_median = result.median()
    
        author = ctx.author.name
        embed1 = discord.Embed(  title = f"{author}'s Draft"
                                ,url   = response
                                ,color = discord.Color.orange())      
        
        mean_desc = ''
        mean_desc = mean_desc + f'Class: {draft_class} \n'
        
        for index_name in result_mean.index:
        #for index_name in ['Cost', 'Score-GW']:
            mean_desc = mean_desc + 'Avg ' + index_name + ': ' + '{:.2f}'.format(result_mean[index_name]) + '\n'
        
        embed1.add_field(name='Stats',
                         value=mean_desc,
                         inline=False
                         )        
        await ctx.send(embed=embed1)        
        
        
        
        
#################### Functions ######################


def createlinkfrombuilder(deck_builder_url, lang, mode, valid_input = False):
    sv_format = {'R':'3', 'U':'1','T':'2'}
    languages = ['en', 'ja', 'ko', 'zh-tw' , 'fr', 'it', 'de', 'es']            

    if 'shadowverse-portal.com/deckbuilder/create/' not in deck_builder_url:
        response = "Invalid link"
    elif mode.upper() not in sv_format:
        response = "Invalid deck format"
    elif lang.lower() not in languages:
        response = "Invalid language"
    else:      
        deck_hash = deck_builder_url.split("hash=")[1].split("&")[0]
        #deck_hash = deck_hash.replace("1",str(sv_format[mode.upper()]),1)
        deck_list_url = "https://shadowverse-portal.com/deck/" + str(deck_hash) + "?lang=" + str(lang)
        #response = discord.Embed(title="Sample Embed", url=deck_list_url)
        response = deck_list_url
        valid_input = True
    return response, valid_input


def createlinkfromcode(deck_code, lang, mode, valid_input = False):
    sv_format = {'R':'3', 'U':'1','T':'2'}
    languages = ['en', 'ja', 'ko', 'zh-tw' , 'fr', 'it', 'de', 'es']
    
    deck_code_url = "https://shadowverse-portal.com/api/v1/deck/import?format=json&deck_code=" + deck_code + "&lang=en"
    with urllib.request.urlopen(deck_code_url) as response:
            source = response.read()            
    deck_json = json.loads(source)
    
    if len(deck_json['data']['errors']) != 0:
        response = "Deck code invalid or does not exist"
    elif mode.upper() not in sv_format:
        response = "Invalid deck format"
    elif lang.lower() not in languages:
        response = "Invalid language"
    else:      
        deck_hash = deck_json['data']['hash']
        #deck_hash = deck_hash.replace("1",str(sv_format[mode.upper()]),1)
        
        deck_list_url = "https://shadowverse-portal.com/deck/" + str(deck_hash) + "?lang=" + str(lang)
        response = deck_list_url
        valid_input = True
    return response, valid_input 


def mullcards(card_list, opening_hand, card_to_mull):
    mull_count = len(card_to_mull)
    for num in range (1,len(opening_hand)+1):
        if num in card_to_mull:
            opening_hand[num-1] = 'Empty'
        else:
            card_list.remove(opening_hand[num-1])
        counter = 0
        
    mull_hand = rand.sample(card_list,mull_count)
    counter = 0
    
    for num in range (1,len(opening_hand)+1):
        if opening_hand[num-1] == 'Empty':
            opening_hand[num-1] = mull_hand[counter]
            counter += 1
    return opening_hand


def decklist(link):
    source = requests.get(link).text
    soup = bs(source, 'lxml')
    
    card_name = soup.find_all('span', class_="el-card-list-info-name-text")
    card_qty = soup.find_all('p', class_="el-card-list-info-count")
    card_cost = soup.select('i[class*="icon-cost is-cost-"]')
    card_stats = soup.find_all('a', class_="el-icon-search is-small tooltipify")
    card_atk = [card['data-card-atk'] for card in card_stats]
    card_def = [card['data-card-life'] for card in card_stats]
    card_type = [card['data-card-char-type'] for card in card_stats]
    
    card_info = []
    for card in range (0,len(card_type)):
        if card_type[card] == '1': #follower
            card_info.append(f'{card_cost[card].text}pp {card_atk[card]}/{card_def[card]}')
        elif card_type[card] == '3': #amulet
            card_info.append(f'{card_cost[card].text}pp Amulet')
        elif card_type[card] == '4': #spell
            card_info.append(f'{card_cost[card].text}pp Spell')
    
    card_list = []
    for unique_card in range(0,len(card_name)):

        for copies in range(0,int(card_qty[unique_card].text[1])):
            card_list.append(f'{card_name[unique_card].text} ({card_info[unique_card]})')
    return card_list


def decklist_t2(link):
    source = requests.get(link).text
    soup = bs(source, 'lxml')
    
    card_name = soup.find_all('span', class_="el-card-list-info-name-text")
    card_qty = soup.find_all('p', class_="el-card-list-info-count")
     
    card_list = []
    for unique_card in range(0,len(card_name)):

        for copies in range(0,int(card_qty[unique_card].text[1])):
            card_list.append(f'{card_name[unique_card].text}')           
    return card_list

    
@bot.command(name='test1')
async def test1(ctx):
    embedVar = discord.Embed(title='title', description='description', color=0xffd800)
    embedVar.set_image(url="https://cdn.discordapp.com/attachments/84319995256905728/252292324967710721/embed.png")    #the image itself
    embedVar.set_footer(text='footer',icon_url="https://cdn.discordapp.com/attachments/84319995256905728/252292324967710721/embed.png")   #image in icon_url
    embedVar.set_thumbnail(url="https://cdn.discordapp.com/attachments/84319995256905728/252292324967710721/embed.png") #image itself    
    await ctx.send(embed=embedVar)
        
# def mulliganfunction(mulligan, card_list, opening_hand):
#     x = '123'
#     if mulligan.lower() == 'n':
#         pass
#     elif mulligan in [''.join(j) for i in range(1,len(x) + 1) for j in  permutations(x, i)]:
#         if mulligan == '1':
#             card_to_mull = [1]
#         elif mulligan == '2':
#             card_to_mull = [2]
#         elif mulligan == '3':
#             card_to_mull = [3]
#         elif mulligan in [''.join(p) for p in permutations('12')]:
#             card_to_mull = [1,2]
#         elif mulligan in [''.join(p) for p in permutations('23')]:
#             card_to_mull = [2,3]
#         elif mulligan in [''.join(p) for p in permutations('13')]:
#             card_to_mull = [1,3]
#         elif mulligan in [''.join(p) for p in permutations('123')]:
#             card_to_mull = [1,2,3]
#         opening_hand = mullcards(card_list, opening_hand, card_to_mull)
    
#     return opening_hand

def mulliganfunction(ctx, mulligan, card_list, opening_hand, valid_mull):   
    answer = 'oooxxx'
    if mulligan.lower() not in set([''.join(p) for p in permutations(answer,3)]):
        pass
    else:
        card_to_mull = [card + 1 for card in range (0,len(mulligan)) if mulligan[card] == 'x']
        opening_hand = mullcards(card_list, opening_hand, card_to_mull)
        valid_mull = True
        
    return opening_hand, valid_mull


def clean_text_1(text):
    c_text = text.replace('<br/>','\n')

    #c_text = f'*{c_text}*'  
    return c_text

    
bot.run(TOKEN)
