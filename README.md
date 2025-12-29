# roguebot

Minimal Discord verification bot. Users must type `agree - {username}` in the verification channel to get the verified role. All attempts are logged.

Required environment variables
- `ROGUEBOT_DISCORD_TOKEN`: Discord bot token.
- `ROGUEBOT_VERIFICATION_CHANNEL_ID`: Channel ID where users type `agree - {username}`.
- `ROGUEBOT_VERIFICATION_HELP_CHANNEL_ID`: Channel ID for verification help messages.
- `ROGUEBOT_VERIFICATION_LOG_CHANNEL_ID`: Channel ID for verification logs.
- `ROGUEBOT_VERIFIED_ROLE_ID`: Role ID to grant on successful verification.
Help message text is set in `bot.py` as `VERIFICATION_HELP_MESSAGE_ON_FAIL` (uses `{0}` for the username).

Build
```sh
./build.sh
```

Run (Docker)
```sh
ROGUEBOT_DISCORD_TOKEN=... \
ROGUEBOT_VERIFICATION_CHANNEL_ID=... \
ROGUEBOT_VERIFICATION_HELP_CHANNEL_ID=... \
ROGUEBOT_VERIFICATION_LOG_CHANNEL_ID=... \
ROGUEBOT_VERIFIED_ROLE_ID=... \
./run.sh
```
