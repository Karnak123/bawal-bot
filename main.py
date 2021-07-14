import discord
import os
import requests
import json
import io
import aiohttp
import re

async def get_meme(message, c=1):
  if c==5:
    message.reply('Unable to establish connection')
  res = requests.get('https://meme-api.herokuapp.com/gimme/memes')
  json_data = json.loads(res.text)
  url = json_data['url']
  filename = url.split('/')[-1]
  async with aiohttp.ClientSession() as session:
    async with session.get(url) as resp:
      if resp.status != 200:
        get_meme(message, c+1)
      else:
        try:
          data = io.BytesIO(await resp.read())
          await message.reply(file=discord.File(data, filename))
        except:
          get_meme(message, c+1)

class MyClient(discord.Client):
  async def on_ready(self):
    print(f'Logged in as {self.user} (ID: {self.user.id})')
  
  async def on_message_delete(self, message):
    await message.channel.send(f'Ki delete korli bhai <@!{message.author.id}>?')
  
  async def on_message_edit(self, before, after):
    await after.reply('Dekhe niyechi \N{EYES}')

  async def on_message(self, message):
    if message.author.id == self.user.id:
      return
    
    if 'meme' in message.content:
      await get_meme(message, 0)

    if re.search('b+a+w+a+l+', message.content.lower()):
      await message.reply('Bol bhai', mention_author=True)

    if re.search('a+g+u+n+', message.content.lower()):
      await message.add_reaction('\N{FIRE}')
      await message.add_reaction('💯')
    
    if re.search('c+a+z+', message.content.lower()):
      await message.add_reaction('🇾')
      await message.add_reaction('🇴')
      await message.add_reaction('🇱')
      await message.add_reaction('🅾️')
      await message.add_reaction('😎')

client = MyClient()
client.run(os.environ['TOKEN'])