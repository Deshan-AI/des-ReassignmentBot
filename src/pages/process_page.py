import os
import yaml
import re
import asyncio
from src.utils.logger import logger


class ProcessPage:
    RETRY_TIMEOUT = 120  # 2 minutes in seconds

    def __init__(self, page):
        self.page = page
        self.xpaths = self._load_xpaths()
        logger.debug("ProcessPage initialized successfully.")

    def _load_xpaths(self):
        """Load XPaths from YAML configuration."""
        config_path = os.path.join(os.path.dirname(__file__), "xpath_ERP.yaml")
        logger.debug(f"Attempting to load XPaths from {config_path}")

        try:
            with open(config_path, "r") as file:
                data = yaml.safe_load(file)
                logger.info(f"Successfully loaded {len(data) if data else 0} XPaths from {config_path}")
                return data
        except Exception as e:
            logger.error(f"Failed to load XPaths from {config_path}: {str(e)}", exc_info=True)
            raise

    async def check_and_process_tasks(self):
        """Check and process available tasks."""
        try:
            logger.debug("Checking for ongoing tasks...")
            ongoing_tasks = await self._get_ongoing_tasks()

            if not ongoing_tasks:
                logger.info("No ongoing tasks available. Waiting for 2 minutes before retry...")
                print("[INFO] No ongoing tasks available. Waiting 2 minutes...")
                await asyncio.sleep(self.RETRY_TIMEOUT)
                return "RETRY"

            logger.debug("Ongoing tasks found. Starting visa queue processing...")
            return await self._process_visa_queue()
            
        except Exception as e:
            logger.error(f"Task processing failed: {str(e)}", exc_info=True)
            raise

    async def _get_ongoing_tasks(self):
        """Get count of ongoing tasks."""
        ongoing_tasks_xpath = '//*[@class="heading-divider"][contains(., "Ongoing Task")]'
        logger.debug(f"Locating ongoing tasks using XPath: {ongoing_tasks_xpath}")

        tasks_text = await self.page.locator(ongoing_tasks_xpath).inner_text()
        logger.debug(f"Raw ongoing tasks text: '{tasks_text}'")

        match = re.search(r"\((\d+)\)", tasks_text)
        task_count = int(match.group(1)) if match else 0

        logger.info(f"Ongoing tasks detected: {task_count}")
        print(f"[DEBUG] Ongoing task count: {task_count}")
        return task_count > 0

    async def _process_visa_queue(self):
        """Process visa queue tasks."""
        logger.debug("Fetching visa queue task rows...")
        rows = await self.page.locator(
            "//div[@class='task'][.//h2[contains(., 'Ongoing Task')]]//div[@class='task-activity']/table/tbody/tr"
        ).all()

        logger.debug(f"Found {len(rows)} rows in the visa queue.")

        visa_xpaths = [
            f"//div[@class='task'][.//h2[contains(., 'Ongoing Task')]]//div[@class='task-activity']/table/tbody/tr[{index}]"
            for index in range(2, len(rows) + 1, 2)
        ]

        logger.debug(f"Constructed {len(visa_xpaths)} visa task XPaths.")

        for xpath in visa_xpaths:
            logger.debug(f"Processing potential visa task at XPath: {xpath}")
            await self.page.wait_for_load_state('networkidle')

            if await self._process_single_task(xpath):
                logger.info(f"Visa queue task processed successfully at XPath: {xpath}")
                return True
        
        logger.info("No valid Visa Queue tasks available.")
        print("[INFO] No valid visa queue tasks to process.")
        return False

    async def _process_single_task(self, xpath):
        """Process a single visa queue task."""
        logger.debug(f"Checking task visibility for XPath: {xpath}")
        await self.page.wait_for_load_state('networkidle')

        if not await self.page.locator(xpath).is_visible():
            logger.debug(f"Task at {xpath} is not visible. Skipping.")
            return False

        status = await self.page.locator(f"{xpath}/td[1]/span").inner_text()
        link_text = await self.page.locator(f"{xpath}/td[1]/a").inner_text()

        logger.info(f"Task detected → Status: '{status}', Link Text: '{link_text}'")
        print(f"[TASK] Status: {status} | Link: {link_text}")

        if status == "Visa - Visa new" and link_text == "Application Verification":
            logger.debug("Valid visa task found. Clicking link...")
            await self.page.locator(f"{xpath}/td[1]/a").click()
            await self.page.wait_for_load_state('networkidle')
            return True
        
        logger.debug("Task did not match required status/link criteria.")
        return False
