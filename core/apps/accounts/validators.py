from django.core.validators import RegexValidator

phone_number_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
