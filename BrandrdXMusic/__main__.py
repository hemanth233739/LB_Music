import asyncio
import importlib
from sys import exit
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall
from BrandrdXMusic.config import config
from config import config  # Fixed import statement
from BrandrdXMusic import LOGGER, app, userbot
from BrandrdXMusic.core.call import Hotty
from BrandrdXMusic.misc import sudo
from BrandrdXMusic.plugins import ALL_MODULES
from BrandrdXMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS  # Ensure BANNED_USERS is properly initialized

async def init():
    """Initialize the bot and start all components."""
    if not any([config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5]):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()

    await sudo()
    
    try:
        gbanned_users = await get_gbanned()
        BANNED_USERS.update(gbanned_users)  # Make sure BANNED_USERS is initialized as a set
        
        banned_users = await get_banned_users()
        BANNED_USERS.update(banned_users)
    except Exception as e:
        LOGGER(__name__).exception("Error fetching banned users")

    await app.start()
    
    for module in ALL_MODULES:
        try:
            importlib.import_module(f"BrandrdXMusic.plugins.{module}")
        except ImportError as e:
            LOGGER("BrandrdXMusic.plugins").exception(f"Failed to import module {module}: {e}")

    LOGGER("BrandrdXMusic.plugins").info("Successfully Imported Modules...")

    await userbot.start()
    await Hotty.start()
    
    try:
        await Hotty.stream_call("https://graph.org/file/e999c40cb700e7c684b75.mp4")
    except NoActiveGroupCall:
        LOGGER("BrandrdXMusic").error("Please turn on the video chat of your log group/channel. Stopping Bot...")
        exit()
    except Exception as e:
        LOGGER("BrandrdXMusic").exception("Error during stream call")

    await Hotty.decorators()
    
    LOGGER("BrandrdXMusic").info("Drop your girlfriend's number at @learningbots79 join @LB_Music_Bot, @learning_bots for any issues.")
    await idle()
    
    await app.stop()
    await userbot.stop()
    LOGGER("BrandrdXMusic").info("Stopping Brandrd Music Bot...")

if __name__ == "__main__":
    asyncio.run(init())
