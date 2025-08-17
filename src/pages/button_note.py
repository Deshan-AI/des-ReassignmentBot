import asyncio
from src.core.base_page import BasePage
from src.utils.logger import logger


class ButtonNote(BasePage):
    """Handles button interactions and queue changes in the application."""

    def __init__(self, page):
        super().__init__(page)
        self._selectors = {
            "ac_ver_button": "//button[normalize-space()='AC VER']",

            "category_dropdown": "//span[@id='select2-EmailModalCategory-container']",
            "input_field": "//input[@aria-controls='select2-EmailModalCategory-results']",

            "subcategory_dropdown": "//span[@id='select2-EmailModalSubCategory-container']",
            "input_field1": "//input[@class='select2-search__field' and @type='search' and @role='searchbox']",

            "comments_field": "#comments",
            "send_button": "#template_form_approve_with_authority"
        }
        logger.debug("ButtonNote initialized with selectors for queue management.")

    async def change_queue(self, category: str, sub_category: str, comment: str) -> None:
        """
        Changes the queue with the specified category, sub-category, and comment.
        """
        try:
            logger.info(f"Starting queue change: Category='{category}', SubCategory='{sub_category}'")
            print(f"[INFO] Changing queue → Category: {category} | SubCategory: {sub_category}")

            await self._open_queue_dialog()
            await self._set_category(category)
            await self._set_subcategory(sub_category)
            await self._add_comment(comment)
            await self._submit_changes()

            logger.info(f"Successfully changed queue to: {category} - {sub_category}")
            print("[SUCCESS] Queue change completed.")
        except Exception as e:
            logger.error(f"Failed to change queue: {str(e)}", exc_info=True)
            print("[ERROR] Queue change failed. See logs for details.")
            raise

    async def _open_queue_dialog(self):
        logger.debug("Opening AC VER queue dialog...")
        await self.wait_and_click(self._selectors["ac_ver_button"])
        logger.debug("Queue dialog opened.")

    async def _set_category(self, category: str):
        logger.debug(f"Selecting category: {category}")
        await self.wait_and_click(self._selectors["category_dropdown"])
        await self.wait_and_fill(self._selectors["input_field"], category)
        await self.page.keyboard.press("Enter")
        logger.info(f"Category set to '{category}'.")

    async def _set_subcategory(self, sub_category: str):
        logger.debug(f"Selecting sub-category: {sub_category}")
        await self.wait_and_click(self._selectors["subcategory_dropdown"])
        await self.wait_and_fill(self._selectors["input_field1"], sub_category)
        await self.page.keyboard.press("Enter")
        logger.info(f"Sub-category set to '{sub_category}'.")

    async def _add_comment(self, comment: str):
        logger.debug("Adding comment to queue change form...")
        await self.wait_and_click(self._selectors["comments_field"])
        await self.wait_and_fill(self._selectors["comments_field"], f"{comment}\n")
        logger.info(f"Comment added: {comment}")

    async def _submit_changes(self):
        logger.debug("Submitting queue change...")
        await self.page.locator('[data-formid="template_form_approve_with_authority"]').click()
        await self.page.get_by_text("SEND AND SAVE", exact=True).click()
        await self.page.wait_for_load_state('networkidle')

        button = self.page.locator(self._selectors["ac_ver_button"])
        button_text = await button.text_content()
        next_queue = button_text.strip() if button_text else 'N/A'
        
        logger.info(f"Queue successfully moved to: {next_queue}")
        print(f"[DEBUG] Moved to queue: {next_queue}")
