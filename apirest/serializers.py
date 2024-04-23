from rest_framework import serializers
from wagtail.contrib.forms.models import FormSubmission
# from rest_framework_recaptcha.fields import ReCaptchaField

#

class FormSubmissionSerializer(serializers.ModelSerializer):
    # recaptcha = ReCaptchaField()

    class Meta:
        model = FormSubmission
        fields = '__all__'
