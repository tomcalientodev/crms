import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def validate_phone_number(value):
    # Check if the value is a 10-digit number with optional dashes
    if not re.match(r'^(\d{10}|\d{3}-\d{3}-\d{4})$', value):
        raise ValidationError(_('Phone number must be a 10-digit number (e.g., 1234567890), or a 10-digit number with dashes (e.g., 123-456-7890).'))

class CustomPasswordValidator:
    def validate(self, password, user=None):

        if not any(char.isdigit() for char in password):
            raise ValidationError(_('Password must contain at least one digit.'))
        elif not any(char.isalpha() for char in password):
            raise ValidationError(_('Password must contain at least one letter.'))
        elif not any(char in '!@#$%^&*()_+[]{}|;:,.<>?/' for char in password):
            raise ValidationError(_('Password must contain at least one special character.'))

    def get_help_text(self):
        return _("Your password must contain at least 8 characters, including at least one letter, one number, and one special character.")
