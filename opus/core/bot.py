# Copyright (c) 2025 OpusMusic
# Licensed under the MIT License.
# This file is part of OpusMusic


import pyrogram

from opus import config, logger


class Bot(pyrogram.Client):
    def __init__(self):
        super().__init__(
            name="opus",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            parse_mode=pyrogram.enums.ParseMode.HTML,
            max_concurrent_transmissions=7,
            link_preview_options=pyrogram.types.LinkPreviewOptions(is_disabled=True),
        )
        self.owner = config.OWNER_ID  # ab yeh list hai [id1, id2, ...]
        self.logger = config.LOGGER_ID
        self.bl_users = pyrogram.filters.user()
        self.sudoers = pyrogram.filters.user(self.owner)  # list pass hogi seedha

    async def boot(self):
        """
        Starts the bot and performs initial setup.

        Raises:
            SystemExit: If the bot fails to access the log group or is not an administrator in the logger group.
        """
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name
        self.username = self.me.username
        self.mention = self.me.mention

        try:
            # LOGGER_ID is the configured log/discussion group or channel ID.
            log_chat = await self.get_chat(self.logger)
            await self.send_message(self.logger, "Bot Started")
            member = await self.get_chat_member(self.logger, self.id)
        except Exception as ex:
            raise SystemExit(
                f"Bot has failed to access LOGGER_ID={self.logger}. "
                f"Set LOGGER_ID to the numeric ID of your log group/channel and "
                f"make the bot an administrator there.\nReason: {ex}"
            )

        if member.status not in (
            pyrogram.enums.ChatMemberStatus.ADMINISTRATOR,
            pyrogram.enums.ChatMemberStatus.OWNER,
        ):
            raise SystemExit("Please promote the bot as an admin in the LOGGER_ID group/channel.")

        log_title = getattr(log_chat, "title", None) or getattr(log_chat, "first_name", None) or "Untitled"
        log_username = getattr(log_chat, "username", None)
        linked_chat_id = getattr(log_chat, "linked_chat_id", None)
        logger.info(
            "Logger destination resolved: title=%r id=%s type=%s username=%r "
            "linked_chat_id=%r",
            log_title,
            getattr(log_chat, "id", self.logger),
            getattr(log_chat, "type", "unknown"),
            log_username,
            linked_chat_id,
        )
        if log_username:
            logger.info("Logger destination link: https://t.me/%s", log_username)
        logger.info(f"Bot started as @{self.username}")

    async def exit(self):
        """
        Asynchronously stops the bot.
        """
        await super().stop()
        logger.info("Bot stopped.")
