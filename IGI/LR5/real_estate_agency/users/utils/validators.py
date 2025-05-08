from datetime import date

from django.core.validators import BaseValidator


class RestrictedAgeValidator(BaseValidator):
    message = "Ensure that date is older than %(limit_value)s."
    code = "restricted_age"

    def compare(self, birth_date, limit_value):
        today = date.today()
        age = (
            today.year
            - birth_date.year
            - ((today.month, today.day) < (birth_date.month, birth_date.day))
        )
        return age < limit_value
