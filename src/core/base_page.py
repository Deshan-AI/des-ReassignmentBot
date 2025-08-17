from playwright.async_api import Page
import asyncio
from src.utils.logger import logger
from src.utils.config import Config

class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, page: Page):
        self.page = page
        self.config = Config()
        self.timeout = 60000  # 1 minute in milliseconds

    async def wait_and_fill(self, selector: str, value: str) -> None:
        """Safely wait for element and fill it"""
        try:
            await self.page.fill(selector, value)
            await asyncio.sleep(self.config.MIN_SLEEP)
        except Exception as e:
            logger.error(f"Failed to fill {selector}: {str(e)}")
            raise

    async def wait_and_click(self, selector: str) -> None:
        """Safely wait for element and click it"""
        try:
            await self.page.click(selector)
            await asyncio.sleep(self.config.MIN_SLEEP)
        except Exception as e:
            logger.error(f"Failed to click {selector}: {str(e)}")
            raise
