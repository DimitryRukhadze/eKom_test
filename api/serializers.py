from rest_framework import serializers
from dateutil import parser as dateparse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from phonenumbers import parse, is_valid_number
from phonenumbers.phonenumberutil import NumberParseException


class DataSerializer(serializers.Serializer):
    data = serializers.CharField()

    def validate_data(self, value):
        if self.is_valid_date(value):
            return "date"
        elif self.is_valid_phone_number(value):
            return "phone"
        elif self.is_valid_email(value):
            return "email"
        else:
            return "text"

    def is_valid_date(self, value):
        try:
            dateparse.parse(value)
            return True
        except (ValueError, OverflowError):
            return False

    def is_valid_phone_number(self, value):
        try:
            parsed_number = parse(value)
            return is_valid_number(parsed_number)
        except NumberParseException:
            return False

    def is_valid_email(self, value):
        try:
            validate_email(value)
            return True
        except ValidationError:
            return False
