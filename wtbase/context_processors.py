from django.conf import settings


def recaptcha(request):
    return {
        'RECAPTCHA_ENTERPRISE_SITE_KEY_VERIFY': settings.RECAPTCHA_ENTERPRISE_SITE_KEY_VERIFY,
        'RECAPTCHA_ENTERPRISE_SITE_KEY_CHALLENGE': settings.RECAPTCHA_ENTERPRISE_SITE_KEY_CHALLENGE
    }
