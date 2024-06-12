from wagtail.admin.views.account import LoginView as WagtailLoginView
from gdmty_django_recaptcha_enterprise.decorators import requires_recaptcha_token


class LoginView(WagtailLoginView):

    @requires_recaptcha_token('verify')
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return super(LoginView, self).post(request, *args, **kwargs)
