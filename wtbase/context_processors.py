import os
from django.conf import settings


def recaptcha_sitekey(request):
    # TODO: Willy, hay que considerar dos tipos de sitekey, una con challenge y otra sin eso
    # en los settings de https://github.com/gobiernodigitalmonterrey/gdmty-django-recaptcha-enterprise/ vienen:
    # RECAPTCHA_ENTERPRISE_SITE_KEY_VERIFY
    # RECAPTCHA_ENTERPRISE_SITE_KEY_CHALLENGE

    return {
        'RECAPTCHA_ENTERPRISE_SITE_KEY_VERIFY': settings.RECAPTCHA_ENTERPRISE_SITE_KEY_VERIFY,
        'RECAPTCHA_ENTERPRISE_SITE_KEY_CHALLENGE': settings.RECAPTCHA_ENTERPRISE_SITE_KEY_CHALLENGE
    }
