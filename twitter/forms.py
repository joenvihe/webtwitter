# appname/forms.py

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser
"""If you plan to edit users in the admin, you'll most likely also need to supply custom forms
for your new user model. In this case, rather than copying and pasting the complete forms from Django,
you can extend Django's built-in UserCreationForm and UserChangeForm to remove the username field
(and optionally add any others that are required) like so:"""
class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)

    class Meta:
        model = CustomUser
        fields = ("email",)

class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)

    class Meta:
        model = CustomUser
        fields = ("email",) # se adicioname el campo
