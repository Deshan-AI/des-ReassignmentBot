import logging

# Logger configuration
logging.basicConfig(level=logging.DEBUG,
                    filename="app.log",
                    encoding="utf-8",
                    filemode="a",
                    format="{asctime} - {levelname} - {filename}:{lineno} - {message}",
                    style="{",
                    datefmt="%Y-%m-%d %H:%M")

class CustomLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        extra = kwargs.get("extra", {})
        kwargs["extra"] = extra  # Update kwargs with the extra dictionary
        return msg, kwargs

# Initialize the logger
logger = CustomLoggerAdapter(logging.getLogger(__name__), {})

# Suppress logs from external libraries
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("selenium").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)