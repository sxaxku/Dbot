# DISCORD_TOKEN -
from livePls import keep_alive
import discord

from discord.ext import commands

TOKEN = "MTIzNDI2Mjc2NTQ4MTM2MTUxMQ.GizlYk.Vf5pyKJQYBDf3Q1stL8w5xYVAKwJpsnKlJRoTY"
CHANNEL_ID = 1215359935333007370
SOURCE_CHANEL_ID = 1234263458158215179

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='/', intents=intents)

keep_alive()


async def delete_other_webhooks(channel_id):
  channel = client.get_channel(channel_id)
  if not channel:
    print("Канал не найден.")
    return

  webhooks = await channel.webhooks()

  for webhook in webhooks[:-1]:
    await webhook.delete()
    print(f"Вебхук {webhook.name} успешно удален.")


async def create_buttons(ctx):
  if ctx.channel.id != SOURCE_CHANEL_ID:
    return

  await ctx.send("Введите ник проверяемого:")
  nickname = await client.wait_for('message',
                                   check=lambda m: m.author == ctx.author)

  await ctx.send("Введите тег проверяемого:")
  player_tag = await client.wait_for('message',
                                     check=lambda m: m.author == ctx.author)

  await ctx.send("Введите преведущей тир:")
  old_tire = await client.wait_for('message',
                                   check=lambda m: m.author == ctx.author)

  await ctx.send("Введите полученый тир:")
  new_tire = await client.wait_for('message',
                                   check=lambda m: m.author == ctx.author)

  await create_webhook(ctx.author.mention, nickname.content,
                       player_tag.content, ctx.author.id, CHANNEL_ID,
                       old_tire.content, new_tire.content)


@client.command()
async def thelp(ctx):
  await ctx.send(
      "Message 1: /test\nMessage 2: User Name(H248x example)\nMessage 3: User Tag(\\@TAG_HERE example)\nMessage 4: Old Tire(ht5 example)\nMessage 5: Getted tire(lt1 example)"
  )


@client.command()
async def test(ctx):
  await delete_other_webhooks(CHANNEL_ID)
  await create_buttons(ctx)


async def create_webhook(tester, player_nickname, player_tag, user_id,
                         channel_id, old_tire, new_tire):
  channel = client.get_channel(channel_id)
  if not channel:
    print("Канал не найден.")
    return

  webhook = await channel.create_webhook(name="Tier")
  print(f"Вебхук Tier успешно создан в канале {channel.name}.")

  embed = discord.Embed(description=f"**Тестер:**\n"
                        f"<@{user_id}>\n"
                        f"**Тег:**\n{player_tag}\n"
                        f"**Прошлый тир:**\n{str(old_tire).upper()}\n"
                        f"**Полученный тир:**\n{str(new_tire).upper()}",
                        color=16711680)

  embed.set_author(name=f"Результаты теста {player_nickname} 🏆")

  await webhook.send(content=f"{player_tag}", embed=embed)


@client.event
async def on_ready():
  print(f'Бот {client.user} успешно подключен.')


client.run(TOKEN)
