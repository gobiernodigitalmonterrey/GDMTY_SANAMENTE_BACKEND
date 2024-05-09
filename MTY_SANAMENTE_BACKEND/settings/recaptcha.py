import os
import ast
import firebase_admin
import logging

recaptcha_logger = logging.getLogger(__name__)

recaptcha_logger.info("Mostrando log de recaptcha settings")

RECAPTCHA_ENTERPRISE_PROJECT_ID = os.getenv("RECAPTCHA_ENTERPRISE_PROJECT_ID")
RECAPTCHA_ENTERPRISE_SITE_KEY_VERIFY = os.getenv("RECAPTCHA_ENTERPRISE_SITE_KEY_VERIFY")
RECAPTCHA_ENTERPRISE_SITE_KEY_CHALLENGE = os.getenv("RECAPTCHA_ENTERPRISE_SITE_KEY_CHALLENGE")
RECAPTCHA_ENTERPRISE_BYPASS_TOKEN = ast.literal_eval(os.getenv("RECAPTCHA_ENTERPRISE_BYPASS_TOKEN", "False"))
RECAPTCHA_ENTERPRISE_SERVICE_ACCOUNT_CREDENTIALS = firebase_admin.credentials.Certificate(ast.literal_eval(os.getenv("RECAPTCHA_ENTERPRISE_CREDENTIALS", "None")))