import discord
import requests
from bs4 import BeautifulSoup
import asyncio
from datetime import datetime
import pytz

TOKEN = 'UTILIZAR-AQUI-O-TOKEN-DO-BOT-DO-DISCORD-GERADO-ACIMA'
BASE_URL = 'https://books.toscrape.com/catalogue/1000-places-to-see-before-you-die_1/index.html'
DISCORD_CHANNEL = 'book'
CHECK_INTERVAL = 30
REQUEST_TIMEOUT = 10

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
client = discord.Client(intents=intents)

async def send_status_update(guild, message, channel_name=DISCORD_CHANNEL):
    channel = discord.utils.get(guild.text_channels, name=channel_name)
    if channel:
        await channel.send(message)

def get_price():
    try:
        response = requests.get(BASE_URL, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        return soup.find(class_='price_color').get_text()
    except requests.RequestException as e:
        return None

async def check_status():
    await client.wait_until_ready()

    while not client.is_closed():
        price = get_price()

        if price is not None:
            time = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%d/%m/%Y %H:%M:%S')

            for guild in client.guilds:
                await send_status_update(guild, f"{price} - {time}")

        await asyncio.sleep(CHECK_INTERVAL)

@client.event
async def on_ready():
    client.loop.create_task(check_status())

async def main():
    async with client:
        await client.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())