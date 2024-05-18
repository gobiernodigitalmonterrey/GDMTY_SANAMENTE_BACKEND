import os
import ast
import logging

recaptcha_logger = logging.getLogger(__name__)
recaptcha_logger.info("Mostrando log de security settings")

CSRF_TRUSTED_ORIGINS = ast.literal_eval(os.getenv("CSRF_TRUSTED_ORIGINS", "[]"))
CORS_ALLOWED_ORIGINS = ast.literal_eval(os.getenv("CORS_ALLOWED_ORIGINS", "[]"))

SECURE_PROXY_SSL_HEADER = ast.literal_eval(os.getenv("SECURE_PROXY_SSL_HEADER", "('HTTP_X_FORWARDED_PROTO', 'https')"))
SECURE_SSL_REDIRECT = ast.literal_eval(os.getenv("SECURE_SSL_REDIRECT", "True"))

SESSION_COOKIE_SECURE = ast.literal_eval(os.getenv("SESSION_COOKIE_SECURE", "True"))
SESSION_COOKIE_HTTPONLY = ast.literal_eval(os.getenv("SESSION_COOKIE_HTTPONLY", "True"))
SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Strict")
CSRF_COOKIE_SECURE = ast.literal_eval(os.getenv("CSRF_COOKIE_SECURE", "True"))
CSRF_COOKIE_SAMESITE = os.getenv("CSRF_COOKIE_SAMESITE", "Strict")

DEFENDER_LOCK_OUT_BY_IP_AND_USERNAME = ast.literal_eval(os.getenv("DEFENDER_LOCK_OUT_BY_IP_AND_USERNAME", "True"))
DEFENDER_BEHIND_REVERSE_PROXY = ast.literal_eval(os.getenv("DEFENDER_BEHIND_REVERSE_PROXY", "True"))

SESSION_EXPIRE_SECONDS = 600
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_TIMEOUT_REDIRECT = '/'
