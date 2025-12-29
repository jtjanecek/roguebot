docker container kill roguebot
docker container rm roguebot

docker build . -t roguebot
docker run -d --name roguebot --restart unless-stopped \
  -e ROGUEBOT_DISCORD_TOKEN \
  -e ROGUEBOT_VERIFICATION_CHANNEL_ID \
  -e ROGUEBOT_VERIFICATION_HELP_CHANNEL_ID \
  -e ROGUEBOT_VERIFICATION_LOG_CHANNEL_ID \
  -e ROGUEBOT_VERIFIED_ROLE_ID \
  roguebot
