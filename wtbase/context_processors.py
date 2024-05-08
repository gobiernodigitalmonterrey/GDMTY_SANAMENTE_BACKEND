import os

def recaptcha_sitekey(request):
    return {'RECAPTCHA_SITEKEY': os.environ.get('RECAPTCHA_SITEKEY', '')}
