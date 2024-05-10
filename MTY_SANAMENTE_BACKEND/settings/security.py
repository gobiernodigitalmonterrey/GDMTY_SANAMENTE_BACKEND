import os
import ast
import logging

recaptcha_logger = logging.getLogger(__name__)
recaptcha_logger.info("Mostrando log de security settings")

CSRF_TRUSTED_ORIGINS = ast.literal_eval(os.getenv("CSRF_TRUSTED_ORIGINS", "[]"))