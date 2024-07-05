import discord
import json
import time

# Load configuration file for the Discord token
def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config
    except Exception as e:
        return {}

# Load armor data from JSON file
def load_armor_data():
    try:
        with open('armor_sets_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except Exception as e:
        return []

# Function to get armor set details by name
def get_armor_set(name):
    armor_data = load_armor_data()
    for armor in armor_data:
        if armor['Armor_Name'].lower() == name.lower():
            return armor
    return None

# Function to format armor set details into Discord embed
def format_armor_embed(armor):
    if not armor:
        return discord.Embed(title='Armor Set Not Found', description='Could not find the specified armor set.')

    embed = discord.Embed(title=f"{armor['Armor_Name']} Stats")

    # Set armor image as thumbnail with timestamp to refresh cache
    image_url = armor['Armor_Image'] + f"?timestamp={int(time.time())}"
    embed.set_image(url=image_url)

    damage_negation_str = ""
    for damage_type, value in armor['Damage_Negation'].items():
        damage_negation_str += f"{damage_type}: {value}\n"

    resistance_str = ""
    for resistance_type, value in armor['Resistance'].items():
        resistance_str += f"{resistance_type}: {value}\n"

    embed.add_field(name="Damage Negation", value=damage_negation_str, inline=True)
    embed.add_field(name="Resistance", value=resistance_str, inline=True)
    embed.add_field(name="Armor Weight", value=f"{armor['Armor_Weight']} Weight", inline=False)

    return embed

# Load the configuration
config = load_config()
discord_token = config.get("DISCORD_TOKEN")

# Discord bot client with intents
intents = discord.Intents.default()
intents.message_content = True  # Ensure this is enabled for handling message events
intents.presences = True  # Enable this if your bot needs to track member presence
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    # Add a command instruction message below the bot name
    game = discord.Game("Type !armor <name> for armor stats")
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!armor '):
        query = message.content[len('!armor '):].strip()
        
        if not query:
            await message.channel.send("Please provide an armor name or a single letter to search for armor sets.")
            return
        
        armor = get_armor_set(query)
        
        if armor:
            embed = format_armor_embed(armor)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(f"Armor set '{query}' not found.")

# Run the bot with the loaded token
if discord_token:
    client.run(discord_token)
else:
    print("Discord token not found. Please check your config file.")
