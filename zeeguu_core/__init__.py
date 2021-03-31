# -*- coding: utf8 -*-
import logging
import os
import sys
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

logger = logging.getLogger(__name__)
print(f"zeeguu_core initialized logger with name: {logger.name}")

logging.basicConfig(
    stream=sys.stdout, format="%(asctime)s %(levelname)s %(name)s %(message)s"
)

if os.environ.get("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
        integrations=[FlaskIntegration()],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=0.3,
    )

# install nltk punkt & tagger if missing
import nltk

try:
    nltk.sent_tokenize("I am a berliner.")
except LookupError as e:
    nltk.download("punkt")
    nltk.download("averaged_perceptron_tagger")


def info(msg):
    logger.info(msg)


def debug(msg):
    logger.debug(msg)


def log(msg):
    info(msg)


def warning(msg):
    logger.warning(msg)


def critical(msg):
    logger.critical(msg)


def logp(msg):
    log(msg)
    print(msg)
