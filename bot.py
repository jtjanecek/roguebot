# bot.py
import os
import discord


def _require_env(name: str) -> str:
  value = os.getenv(name)
  if value is None or value.strip() == "":
    raise RuntimeError(f"Missing required env var: {name}")
  return value


def _require_int_env(name: str) -> int:
  value = _require_env(name)
  try:
    return int(value)
  except ValueError as exc:
    raise RuntimeError(f"Env var {name} must be an integer.") from exc


TOKEN = _require_env("ROGUEBOT_DISCORD_TOKEN")
VERIFICATION_CHANNEL_ID = _require_int_env("ROGUEBOT_VERIFICATION_CHANNEL_ID")
VERIFICATION_LOG_CHANNEL_ID = _require_int_env("ROGUEBOT_VERIFICATION_LOG_CHANNEL_ID")
VERIFICATION_HELP_CHANNEL_ID = _require_int_env("ROGUEBOT_VERIFICATION_HELP_CHANNEL_ID")
VERIFICATION_HELP_MESSAGE_ON_FAIL = "Please type `agree - {0}` to get verified."
VERIFIED_ROLE_ID = _require_int_env("ROGUEBOT_VERIFIED_ROLE_ID")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Bot(intents=intents)


def _get_expected_verification_message(author_name: str) -> str:
  return f"agree - {author_name}".lower().strip()


@client.event
async def on_ready():
  print(f"{client.user} has connected to Discord!")


@client.event
async def on_message(message):
  if message.author.bot:
    return

  if message.channel.id not in (VERIFICATION_CHANNEL_ID, VERIFICATION_HELP_CHANNEL_ID):
    return

  raw_msg = message.content.replace("`", "(backtick)")
  expected = _get_expected_verification_message(message.author.name)
  pass_verification = message.content.lower().strip() == expected

  if pass_verification:
    role = message.author.guild.get_role(VERIFIED_ROLE_ID)
    if role:
      await message.author.add_roles(role)

  if message.channel.id == VERIFICATION_CHANNEL_ID and not pass_verification:
    help_channel = client.get_channel(VERIFICATION_HELP_CHANNEL_ID)
    if help_channel:
      help_message = VERIFICATION_HELP_MESSAGE_ON_FAIL.format(message.author.name.lower().strip())
      await help_channel.send(f"<@{message.author.id}> - {help_message}")

  if message.channel.id == VERIFICATION_CHANNEL_ID or pass_verification:
    msg_to_send = f'''
=================================================
User Tag: <@{message.author.id}>
```
Passed Verification: {pass_verification}
Display Name: {message.author.display_name}
Discord Username: {message.author.name}
User ID: {message.author.id}
User Created At: {message.author.created_at}
Message Created At: {message.created_at}
Message: {raw_msg}
```
'''
    if len(msg_to_send) > 2000:
      msg_to_send = msg_to_send[0:1980] + '\n```'

    welcome_logs_channel = client.get_channel(VERIFICATION_LOG_CHANNEL_ID)
    if welcome_logs_channel:
      await welcome_logs_channel.send(msg_to_send)

    try:
      await message.delete()
    except Exception:
      pass


client.run(TOKEN)
