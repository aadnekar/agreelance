from django import forms
from django.contrib.auth.models import User
from projects.models import ProjectCategory
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    company = forms.CharField(
        max_length=30, required=False, help_text="Here you can add your company."
    )

    email = forms.EmailField(max_length=254, help_text="Inform a valid email address.")
    email_confirmation = forms.EmailField(
        max_length=254, help_text="Enter the same email as before, for verification."
    )

    phone_number = forms.CharField(max_length=50)
    country = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    postal_code = forms.CharField(max_length=50)
    street_address = forms.CharField(max_length=50)

    categories = forms.ModelMultipleChoiceField(
        queryset=ProjectCategory.objects.all(),
        help_text='Hold down "Control", or "Command" on a Mac, to select more than one.',
    )

    def clean(self):
        """ Verifies that the fields are correct"""
        cleaned_data = super(SignUpForm, self).clean()
        email = cleaned_data.get('email')
        email_confirmation = cleaned_data.get('email_confirmation')

        if email and email_confirmation and email != email_confirmation:
            self._errors['email_confirmation'] = self.error_class([
                'Emails do not match.'
            ])
            del self.cleaned_data['email_confirmation']
        return cleaned_data

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "categories",
            "company",
            "email",
            "email_confirmation",
            "password1",
            "password2",
            "phone_number",
            "country",
            "state",
            "city",
            "postal_code",
            "street_address",
        )
