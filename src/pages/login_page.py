from src.core.base_page import BasePage
from src.utils.logger import logger


class LoginPage(BasePage):
    """Handles authentication for the ERP portal."""

    def __init__(self, page):
        super().__init__(page)
        self.credentials = self.config.CREDENTIALS["ERP"]
        self._selectors = {
            "username": '//*[@id="loginform-email"]',
            "password": '//*[@id="loginform-password"]',
            "submit": '//*[@id="login-form"]/button'
        }
        logger.debug("LoginPage initialized with ERP credentials and selectors.")

    async def login(self):
        """Performs complete login flow to the ERP portal."""
        try:
            logger.info(f"Navigating to ERP login page: {self.credentials.URL}")
            await self.page.goto(self.credentials.URL, timeout=self.timeout)
            print(f"[INFO] Navigated to: {self.credentials.URL}")

            logger.debug("Entering credentials...")
            await self._enter_credentials()

            logger.debug("Submitting login form...")
            await self._submit_login()

            logger.info("Login sequence completed successfully.")
            print("[SUCCESS] ERP Login successful.")
        except Exception as e:
            logger.error(f"Login failed: {str(e)}", exc_info=True)
            print("[ERROR] ERP Login failed. Check logs for details.")
            raise

    async def _enter_credentials(self):
        """Enters username and password into the login form fields."""
        logger.debug(f"Filling username field: {self._selectors['username']}")
        await self.wait_and_fill(self._selectors["username"], self.credentials.USERNAME)

        logger.debug(f"Filling password field: {self._selectors['password']}")
        await self.wait_and_fill(self._selectors["password"], self.credentials.PASSWORD)

        logger.info("Credentials entered into login form.")
        print("[DEBUG] Credentials filled.")

    async def _submit_login(self):
        """Submits the login form and waits for navigation."""
        logger.debug(f"Clicking submit button: {self._selectors['submit']}")
        await self.wait_and_click(self._selectors["submit"])

        logger.debug("Waiting for page to finish loading after login...")
        await self.page.wait_for_load_state('networkidle')

        logger.info("Login form submitted and page loaded.")
        print("[DEBUG] Login form submitted, waiting for dashboard.")
