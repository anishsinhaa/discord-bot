import mysql.connector
import discord
from dotenv import load_dotenv
from discord.utils import find
import os
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


TOKEN = os.getenv('DISCORD_TOKEN')

db = mysql.connector.connect(
    host=os.getenv("DATABASE_HOST"),
    user=os.getenv("DATABASE_USERNAME"),
    passwd=os.getenv("DATABASE_PASSWORD"),
    db=os.getenv("DATABASE"),
)

cursor = db.cursor()


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await message.channel.send(f'Hello world {message.guild.name}!')


@client.event
async def on_guild_join(guild):
    # send msg to general
    general = find(lambda x: x.name == 'general' or x.name== 'general-chat',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send('Hello {} !'.format(guild.name))

     # Insert server id and token into the Auth table
    cursor.execute("INSERT INTO Auth (token, server_id) VALUES (%s, %s)", (TOKEN, guild.id))
    db.commit()

client.run(TOKEN)

