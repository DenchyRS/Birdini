# Birdini bot.py
import os
import discord
import json
import datetime
import requests

from dotenv import load_dotenv
from pybirdbuddy.birdbuddy.client import BirdBuddy
from discord import app_commands
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from datetime import datetime

# Load enviroment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
EMAIL = os.getenv('BB_NAME')
PASS = os.getenv('BB_PASS')

# Open json file
with open('discVars.json') as discVars:
    jsonData = json.load(discVars)

# Login to birdbuddy feeder
bb = BirdBuddy(EMAIL, PASS)
bb.language_code = "en"

intents = discord.Intents.all()

# This is the URL used to insert multiple images into embeds. This can be changed but it's greatly appreciated if you leave it :)
embedUrl = "https://ko-fi.com/denchy"

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    bird_sighting_new.start()
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# Create buttons to attatch to embed


class EmbedButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        # Always add support me button
        supportMeButton = discord.ui.Button(
            label="Support Me!", style=discord.ButtonStyle.blurple, url=embedUrl, emoji="❤️")
        self.add_item(supportMeButton)

# Change what channel the public messages will be sent too


@bot.tree.command(name="channel", description="Define what channel you want to send public notifications to.")
@has_permissions(administrator=True)
@app_commands.describe(channel="Select a channel you wish to push notifications to. You can also enter the channel ID.")
async def set_message_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    print(f"Message channel updated to {channel}")
    jsonData['ChannelID'] = int(channel.id)
    with open("discVars.json", "w") as fileA:
        json.dump(jsonData, fileA)
    await interaction.response.send_message(f"{bot.user.name} will now post notifications to {channel}", ephemeral=True)

# Change what channel the 'muted' messages will be sent too


@bot.tree.command(name="muted_channel", description="Define what channel you want to redirect public notifications to when muted.")
@has_permissions(administrator=True)
@app_commands.describe(channel="Select a channel you wish to redirect notifications to when muted. You can also enter the channel ID.")
async def set_message_channel_muted(interaction: discord.Interaction, channel: discord.TextChannel):
    print(f"Muted message channel updated to {channel}")
    jsonData['mutedChannelID'] = int(channel.id)
    with open("discVars.json", "w") as fileA:
        json.dump(jsonData, fileA)
    await interaction.response.send_message(f"{bot.user.name} will now post notifications to {channel} when muted", ephemeral=True)


@bot.tree.command(name='mute', description="Mute the bot, the bot will continue to post notifications to your desired privated channel.")
@has_permissions(administrator=True)
async def mute_bot(interaction: discord.Interaction):
    if jsonData['isMuted']:
        await interaction.response.send_message(f"{bot.user.name} is already muted!", ephemeral=True)
        return
    jsonData['isMuted'] = True
    with open("discVars.json", "w") as fileA:
        json.dump(jsonData, fileA)
    await interaction.response.send_message(f"{bot.user.name} is now muted and will no longer post to the public channel!", ephemeral=True)


@bot.tree.command(name='unmute', description="Unmute the bot, let everyone see those beautiful birds again!")
@has_permissions(administrator=True)
async def unmute_bot(interaction: discord.Interaction):
    if not jsonData['isMuted']:
        await interaction.response.send_message(f"{bot.user.name} isn't muted!", ephemeral=True)
        return
    jsonData['isMuted'] = False
    with open("discVars.json", "w") as fileA:
        json.dump(jsonData, fileA)
    await interaction.response.send_message(f"{bot.user.name} is now unmuted and will continue to post to the public channel!", ephemeral=True)


# timer stuff
@tasks.loop(seconds=60.0)
async def bird_sighting_new():
    channelID = jsonData['ChannelID']
    mChannelID = jsonData['mutedChannelID']
    isMuted = jsonData['isMuted']
    # channel id you want the bird auto-notifications to be sent to
    channel = bot.get_channel(channelID)
    mChannel = bot.get_channel(mChannelID)
    if channel is None:
        print("A valid channel for public alerts was not selected.")
        return
    elif mChannel is None and isMuted is True:
        print("A valid channel for muted alerts was not selected.")
        return
    # BB CODE
    getPostcards = await bb.new_postcards()

    # return if no new postcards are detected
    if len(getPostcards) == 0:
        print("No new postcards found.")
        return

    # after postcard sighting is confirmed use finishPostcard
    getSightings = await bb.sighting_from_postcard(getPostcards[0])
    getReport = getSightings.report
    # get report status and set type

    imageUrls = [item['contentUrl'] for item in getSightings.medias]
    videoUrls = [item['contentUrl'] for item in getSightings.video_media]

    # Determine if there is a video url and select appropriate emoji for embed
    if len(videoUrls) > 0:
        videoEmoji = 'Yes'
        hasVideo = True
    else:
        videoEmoji = 'No'
        hasVideo = False

    appendToDescription = f"\n🖼️ Images captured: {len(imageUrls)} \n📹 Video captured: {videoEmoji}"

    split_string = str(getReport).split("'")
    recognized_phrase = split_string[3]
    if recognized_phrase == "mystery" or recognized_phrase == "best_guess":
        birdIcon = ""
        descriptionText = f"🐦 Total visits: ??{appendToDescription}"
        embedTitle = "Unidentifiable bird spotted!"
        embedColor = 0xb5b5b6
    else:

        birdName = getReport['sightings'][0]['species']['name']
        birdIcon = getReport['sightings'][0]['species']['iconUrl']
        try:
            birdVisitCount = getReport['sightings'][0]['count']
            descriptionText = f"🐦 Total visits: {str(birdVisitCount)}{appendToDescription}"
            embedTitle = f"{birdName} spotted!"
            embedColor = 0x4dff4d
        except:
            birdVisitCount = 1
            descriptionText = f"This is your first time being visited by a {birdName}!\n\n🐦 Total Visits: 1{appendToDescription}"
            embedTitle = f"{birdName} unlocked!"
            embedColor = 0xf1c232

    # Weird embed merge bug thing idk, allows for multiple images in a single embed. Mobile will only show one however.
    embed = discord.Embed(title=embedTitle,
                          url=embedUrl,
                          description=descriptionText,
                          color=embedColor,
                          timestamp=datetime.now())
    # embed.set_image(url=imageUrls[0])
    image_data = requests.get(imageUrls[0]).content
    with open('image.png', 'wb') as handler:
        handler.write(image_data)
    # ^old method linked expires, new one below for test... download and upload the files to discords server and then embed them
    file = discord.File("image.png", filename="image.png")
    files = [file]

    embed = discord.Embed(title=embedTitle,
                          url=embedUrl,
                          description=descriptionText,
                          color=embedColor,
                          timestamp=datetime.now())
    embed.set_image(url="attachment://image.png")
    embed.set_footer(text="Birdini by Denchy", icon_url=bot.user.avatar)

    embeds = [embed]

# Process additional images
    if len(imageUrls) > 1:
        for i in range(1, min(len(imageUrls), 4)):
            image_data = requests.get(imageUrls[i]).content
            with open(f'image{i}.png', 'wb') as handler:
                handler.write(image_data)
            file = discord.File(f"image{i}.png", filename=f"image{i}.png")
            files.append(file)

            embed = discord.Embed(url=embedUrl)
            embed.set_image(url=f"attachment://image{i}.png")
            embeds.append(embed)

# Send embed with attachments to appropriate channel
    if isMuted:
        await mChannel.send(files=files, embeds=embeds, view=EmbedButtons())
    else:
        await channel.send(files=files, embeds=embeds, view=EmbedButtons())

    # uncomment this to finish postcards and send them to collections!
    # await bb.finish_postcard(getPostcards[0]['id'], getSightings)

bot.run(TOKEN)
