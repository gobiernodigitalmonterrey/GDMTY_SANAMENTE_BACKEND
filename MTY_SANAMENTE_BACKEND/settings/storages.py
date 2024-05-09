import os
import ast
import logging
import json
from google.oauth2 import service_account

storages_logger = logging.getLogger(__name__)
storages_logger.info("Mostrando log de storages settings")

RUN_ENVIRONMENT = os.getenv("RUN_ENVIRONMENT", "dev")

# Default storage settings, with the staticfiles storage updated.
# See https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-STORAGES
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    # ManifestStaticFilesStorage is recommended in production, to prevent
    # outdated JavaScript / CSS assets being served from cache
    # (e.g. after a Wagtail upgrade).
    # See https://docs.djangoproject.com/en/5.0/ref/contrib/staticfiles/#manifeststaticfilesstorage
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}

DJANGO_STORAGE_BACKEND = os.getenv("DJANGO_STORAGE_BACKEND", "local")

if RUN_ENVIRONMENT == "dev":
    STORAGES['staticfiles']['BACKEND'] = "whitenoise.storage.CompressedStaticFilesStorage"

if RUN_ENVIRONMENT == "production":
    STORAGES['staticfiles']['BACKEND'] = "whitenoise.storage.CompressedManifestStaticFilesStorage"

if DJANGO_STORAGE_BACKEND == "google":
    credentials = service_account.Credentials.from_service_account_info(json.loads(os.getenv("GS_CREDENTIALS")))
    STORAGES_DEFAULT_BACKEND = "storages.backends.gcloud.GoogleCloudStorage"
    STORAGES_DEFAULT_OPTIONS = {
        "bucket_name": os.getenv("GS_BUCKET_NAME", ""),
        "project_id": os.getenv("GS_PROJECT_ID", ""),
        "gzip": ast.literal_eval(os.getenv("GS_IS_GZIPPED", "False")),
        "gzip_content_types": os.getenv("GS_IS_GZIPPED", "(text/css,text/javascript,application/javascript,application/x-javascript,image/svg+xml)"),
        "credentials": credentials,
        "default_acl": ast.literal_eval(os.getenv("GS_DEFAULT_ACL", "None")),
        "querystring_auth": ast.literal_eval(os.getenv("GS_QUERYSTRING_AUTH", "True")),
        "file_overwrite": ast.literal_eval(os.getenv("GS_FILE_OVERWRITE", "True")),
        "max_memory_size": int(os.getenv("GS_MAX_MEMORY_SIZE", 0)),
        "blob_chunk_size": int(os.getenv("GS_BLOB_CHUNK_SIZE")) if os.getenv("GS_BLOB_CHUNK_SIZE") is not None else None,
        "object_parameters": ast.literal_eval(os.getenv("GS_OBJECT_PARAMETERS", "{}")),
        "custom_endpoint": os.getenv("GS_CUSTOM_ENDPOINT", None),
        "location": os.getenv("GS_LOCATION", ""),
    }
