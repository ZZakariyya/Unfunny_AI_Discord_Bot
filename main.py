import os
import discord
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

openai_api_key = 'your api key'
TOKEN = 'your token'

chat = ChatOpenAI(temperature=1, openai_api_key=openai_api_key)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!ask'):
        user_msg = message.content[len('!ask '):].strip()  # strip to ensure you're not just getting whitespace
        
        if not user_msg:
            await message.channel.send("Please provide a question after '!ask'.")
            return

        try:
            response = chat(
                [
                    SystemMessage(content="You are an unhelpful AI bot that makes a joke at whatever the user says"),
                    HumanMessage(content=user_msg)
                ]
            )
            ai_msg = response.content if isinstance(response, AIMessage) else "I don't know what to say."
            await message.channel.send(ai_msg)
        except Exception as e:
            await message.channel.send(f"Sorry, I encountered an error: {e}")

client.run(TOKEN)
