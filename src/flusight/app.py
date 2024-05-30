import structlog

from flusight.util.logs import setup_logging

setup_logging()
logger = structlog.get_logger()


def main():
    """Application entry point."""

    return "howdy"


if __name__ == "__main__":
    main()
