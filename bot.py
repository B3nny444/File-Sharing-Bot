#(©)Codexbotz

from aiohttp import web
from plugins import web_server
import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
from datetime import datetime
import asyncio
import time
from pyrogram.errors import FloodWait, RPCError  # Added for error handling

from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, CHANNEL_ID, PORT

ascii_art = """
░█████╗░░█████╗░██████╗░███████╗██╗░░██╗██████╗░░█████╗░████████╗███████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗╚══██╔══╝╚════██║
██║░░╚═╝██║░░██║██║░░██║█████╗░░░╚███╔╝░██████╦╝██║░░██║░░░██║░░░░░███╔═╝
██║░░██╗██║░░██║██║░░██║██╔══╝░░░██╔██╗░██╔══██╗██║░░██║░░░██║░░░██╔══╝░░
╚█████╔╝╚█████╔╝██████╔╝███████╗██╔╝╚██╗██████╦╝╚█████╔╝░░░██║░░░███████╗
░╚════╝░░╚════╝░╚═════╝░╚══════╝╚═╝░░╚═╝╚═════╝░░╚════╝░░░░╚═╝░░░╚══════╝
"""

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER
        self.retry_count = 0  # Track retry attempts
        self.max_retries = 3  # Maximum retries before giving up

    async def handle_flood_wait(self, error):
        wait_time = error.value
        self.LOGGER.warning(f"FloodWait: Sleeping for {wait_time} seconds...")
        time.sleep(wait_time)
        self.retry_count += 1

    async def start(self):
        while self.retry_count < self.max_retries:
            try:
                await super().start()
                usr_bot_me = await self.get_me()
                self.uptime = datetime.now()

                # Force Sub Channel Handling
                if FORCE_SUB_CHANNEL:
                    try:
                        link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                        if not link:
                            await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                            link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                        self.invitelink = link
                    except Exception as a:
                        self.LOGGER.warning(a)
                        self.LOGGER.warning("Bot can't Export Invite link from Force Sub Channel!")
                        self.LOGGER.warning(f"Please check FORCE_SUB_CHANNEL value and ensure Bot is Admin. Current Value: {FORCE_SUB_CHANNEL}")
                        self.LOGGER.info("\nBot Stopped. Join https://t.me/CodeXBotzSupport for support")
                        sys.exit()

                # DB Channel Verification
                try:
                    db_channel = await self.get_chat(CHANNEL_ID)
                    self.db_channel = db_channel
                    test = await self.send_message(chat_id=db_channel.id, text="Test Message")
                    await test.delete()
                except Exception as e:
                    self.LOGGER.warning(e)
                    self.LOGGER.warning(f"Ensure bot is Admin in DB Channel. Current CHANNEL_ID: {CHANNEL_ID}")
                    self.LOGGER.info("\nBot Stopped. Join https://t.me/CodeXBotzSupport for support")
                    sys.exit()

                self.set_parse_mode(ParseMode.HTML)
                self.LOGGER.info(f"Bot Running! Created by https://t.me/CodeXBotz")
                print(ascii_art)
                print("Welcome to CodeXBotz File Sharing Bot")
                self.username = usr_bot_me.username

                # Web Server Setup
                app = web.AppRunner(await web_server())
                await app.setup()
                bind_address = "0.0.0.0"
                await web.TCPSite(app, bind_address, PORT).start()
                return  # Successfully started, exit the retry loop

            except FloodWait as e:
                await self.handle_flood_wait(e)
            except RPCError as e:
                self.LOGGER.error(f"RPCError: {e}")
                if self.retry_count == self.max_retries - 1:
                    self.LOGGER.critical("Max retries reached. Bot failed to start.")
                    sys.exit(1)
            except Exception as e:
                self.LOGGER.critical(f"Unexpected error: {e}")
                sys.exit(1)

    async def stop(self, *args):
        await super().stop()
        self.LOGGER.info("Bot stopped.")

if __name__ == "__main__":
    print("Launching bot...")
    bot = Bot()
    
    try:
        bot.run()
    except KeyboardInterrupt:
        bot.LOGGER.info("Bot stopped by user")
    except Exception as e:
        bot.LOGGER.critical(f"Critical error during execution: {e}")
