import asyncio
from playwright.async_api import async_playwright
from src.pages.login_page import LoginPage
from src.pages.button_note import ButtonNote
from src.pages.process_page import ProcessPage
from src.utils.logger import logger

# Constants for queue change
QUEUE_CATEGORY = "VA BOT"
QUEUE_SUBCATEGORY = "Re-assignment"
QUEUE_COMMENT = "Auto Forward"

async def process_tasks(page):
    """Process tasks for a single iteration"""
    try:
        # Initialize and perform login
        login_page = LoginPage(page)
        await login_page.login()
        
        # Refresh the page 3 times after login
        for i in range(1, 4):
            print
            logger.info(f"Refreshing page ({i}/3) after login...")
            print(f"Refreshing page ({i}/3) after login...")  # Using print instead of logger
            await page.reload()
            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(1)  # Small delay between refreshes
        
        # Continue with processing
        process_page = ProcessPage(page)
        await process_page.check_and_process_tasks()

        # Change queue
        button_note = ButtonNote(page)
        await button_note.change_queue(
            category=QUEUE_CATEGORY,
            sub_category=QUEUE_SUBCATEGORY,
            comment=QUEUE_COMMENT
        )
    except Exception as e:
        logger.error(f"Error during task processing: {str(e)}")
        raise

async def main():
    """Continuous processing loop"""
    while True:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                logger.info("Starting new processing cycle")
                await process_tasks(page)
                logger.info("Processing cycle completed successfully")
            except Exception as e:
                logger.error(f"Error during processing cycle: {str(e)}")
            finally:
                await browser.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Process stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")